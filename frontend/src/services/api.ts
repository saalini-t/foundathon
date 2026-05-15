import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

export interface Region {
  id: string
  name: string
  description: string
  center: [number, number]
  zoom: number
  bbox: [number, number, number, number]
  country_codes: string[]
}

export interface FireAlert {
  id: number
  latitude: number
  longitude: number
  brightness: number
  acq_date: string
  acq_time: string
  satellite: string
  confidence: string
  frp: number
  daynight: string
}

export interface WeatherStation {
  name: string
  latitude: number
  longitude: number
  latest_date: string
  record_count: number
}

export interface WeatherRecord {
  date: string
  temperature_max: number
  temperature_min: number
  temperature_mean: number
  precipitation_sum: number
  humidity_mean: number
  windspeed_max: number
}

export interface CurrentWeather {
  station_name: string
  latitude: number
  longitude: number
  state: string
  temperature: number
  humidity: number
  precipitation: number
  wind_speed: number
  wind_direction: number
  time: string
}

export interface SpeciesSummary {
  species: string
  family: string
  kingdom: string
  occurrence_count: number
}

export interface PlatformStats {
  fire_detections: number
  weather_observations: number
  weather_stations: number
  species_occurrences: number
  unique_species: number
}

export interface GeoJSONFeatureCollection {
  type: 'FeatureCollection'
  features: Array<{
    type: 'Feature'
    geometry: {
      type: string
      coordinates: number[] | number[][] | number[][][]
    }
    properties: Record<string, unknown>
  }>
  metadata?: Record<string, unknown>
}

// Region endpoint
export const fetchRegions = () =>
  api.get<{ regions: Region[] }>('/regions').then(r => r.data)

// Map endpoints
export const fetchBoundary = (region?: string) =>
  api.get<GeoJSONFeatureCollection>('/map/boundary', { params: { region } }).then(r => r.data)

export const fetchFireLayer = (days = 7, region?: string) =>
  api.get<GeoJSONFeatureCollection>('/map/fire-layer', { params: { days, region } }).then(r => r.data)

export const fetchSpeciesLayer = (limit = 500, region?: string) =>
  api.get<GeoJSONFeatureCollection>('/map/species-layer', { params: { limit, region } }).then(r => r.data)

export const fetchSpeciesHeatmap = (region?: string) =>
  api.get<{ points: Array<{ lat: number; lon: number; species_count: number; occurrence_count: number }> }>('/map/species-heatmap', { params: { region } }).then(r => r.data)

// Alert endpoints
export const fetchFireAlerts = (days = 7, region?: string) =>
  api.get<{ alerts: FireAlert[]; count: number }>('/alerts/fires', { params: { days, region } }).then(r => r.data)

export const fetchFireStats = (days = 30, region?: string) =>
  api.get<{ total_fires: number; high_confidence: number; daily_breakdown: Array<{ date: string; count: number }> }>('/alerts/fires/stats', { params: { days, region } }).then(r => r.data)

// Data endpoints
export const fetchWeatherStations = (region?: string) =>
  api.get<{ stations: WeatherStation[] }>('/data/weather/stations', { params: { region } }).then(r => r.data)

export const fetchWeatherHistory = (station: string, days = 30) =>
  api.get<{ station: string; records: WeatherRecord[]; count: number }>('/data/weather/history', { params: { station, days } }).then(r => r.data)

export const fetchCurrentWeather = (region?: string) =>
  api.get<{ stations: CurrentWeather[] }>('/data/weather/current', { params: { region } }).then(r => r.data)

export const fetchSpeciesSummary = (limit = 50, region?: string) =>
  api.get<{ species: SpeciesSummary[]; total_species: number }>('/data/species/summary', { params: { limit, region } }).then(r => r.data)

export const fetchPlatformStats = (region?: string) =>
  api.get<PlatformStats>('/data/stats', { params: { region } }).then(r => r.data)

// ── Phase 2: Prediction / ML endpoints ──────────────

export interface EHICell {
  cell_id: string
  center_lat: number
  center_lon: number
  ehi_score: number
  status: string
  sub_indices: {
    vegetation_health: number
    forest_integrity: number
    biodiversity_richness: number
    climate_stability: number
    air_quality: number
    fire_disturbance: number
  }
}

export interface EHIResponse {
  count: number
  average_ehi: number
  status_distribution: Record<string, number>
  cells: EHICell[]
}

export interface FireRiskCell {
  cell_id: string
  center_lat: number
  center_lon: number
  risk_probability: number
  risk_level: string
}

export interface FireRiskResponse {
  count: number
  predictions: FireRiskCell[]
}

export interface AnomalyCell {
  cell_id: string
  center_lat: number
  center_lon: number
  is_anomaly: boolean
  anomaly_score: number
  severity: number
  severity_label: string
  factors?: string[]
  features: Record<string, number>
}

export interface AnomalyResponse {
  count: number
  anomaly_count: number
  anomaly_rate: number
  anomalies: AnomalyCell[]
  all_cells: AnomalyCell[]
}

export interface NDVICell {
  cell_id: string
  center_lat: number
  center_lon: number
  year: number
  month: number
  date: string
  ndvi_mean: number
  ndvi_std: number
  ndvi_min: number
  ndvi_max: number
}

export interface NDVITimeseries {
  cell_id: string
  count: number
  timeseries: NDVICell[]
}

export const fetchEHI = (region?: string) =>
  api.get<EHIResponse>('/predict/ehi', { params: { region } }).then(r => r.data)

export const fetchFireRisk = (region?: string) =>
  api.get<FireRiskResponse>('/predict/fire-risk', { params: { region } }).then(r => r.data)

export const fetchAnomalies = (region?: string) =>
  api.get<AnomalyResponse>('/predict/anomalies', { params: { region } }).then(r => r.data)

export const fetchNDVILatest = (region?: string) =>
  api.get<{ count: number; cells: NDVICell[] }>('/ndvi/latest', { params: { region } }).then(r => r.data)

export const fetchNDVITimeseries = (cellId: string, region?: string) =>
  api.get<NDVITimeseries>(`/ndvi/timeseries/${cellId}`, { params: { region } }).then(r => r.data)

// Sync endpoints
export const syncAllData = () =>
  api.post('/sync/all').then(r => r.data)

// ── Feature 1: Contextual Alerts & Playbook ──────────────

export interface AlertContext {
  location: { latitude: number; longitude: number }
  context: {
    nearest_village: { name: string; distance_km: number }
    nearest_road: { name: string; distance_km: number }
    nearest_protected_area: { name: string; distance_km: number }
    vegetation_density: string
    ndvi_value: number
    inside_protected_area: boolean
    estimated_fire_risk: string
  }
  playbook: {
    title: string
    recommended_actions: string[]
  }
}

export const fetchAlertContext = (lat: number, lon: number, region?: string) =>
  api.get<AlertContext>(`/context/alert/${lat}/${lon}`, { params: { region } }).then(r => r.data)

// ── Feature 2: Ground Truth Verification Loop ────────────

export interface VerificationReport {
  id: number
  alert_id: number | null
  alert_type: string
  latitude: number
  longitude: number
  message: string
  photo_path: string | null
  status: string
  reporter_name: string | null
  created_at: string | null
}

export const submitVerification = (data: FormData) =>
  api.post<{ id: number; message: string; status: string }>('/verify/report', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }).then(r => r.data)

export const fetchVerifications = (region?: string, limit = 50) =>
  api.get<{ reports: VerificationReport[]; count: number }>('/verify/reports', { params: { region, limit } }).then(r => r.data)

export const fetchAlertVerificationStatus = (alertId: number, alertType = 'fire') =>
  api.get<{ alert_id: number; verified: boolean; latest_status?: string; report_count?: number }>(`/verify/status/${alertId}`, { params: { alert_type: alertType } }).then(r => r.data)

// ── Feature 3: Temporal Ecosystem Time Machine ───────────

export interface TimeMachineSnapshot {
  month_key: string
  cell_count: number
  average_ndvi: number
  cells: Array<{
    cell_id: string
    center_lat: number
    center_lon: number
    ndvi_mean: number
    ndvi_min: number
    ndvi_max: number
  }>
}

export interface EHITimelinePoint {
  month_key: string
  average_ndvi: number
  ehi_score: number
  status: string
  cell_count: number
}

export const fetchTimeMachineNDVI = (region?: string, month?: number) =>
  api.get<{ region: string; snapshot_count: number; snapshots: TimeMachineSnapshot[] }>('/timemachine/ndvi', { params: { region, month } }).then(r => r.data)

export const fetchTimeMachineEHI = (region?: string) =>
  api.get<{ region: string; months: number; timeline: EHITimelinePoint[] }>('/timemachine/ehi', { params: { region } }).then(r => r.data)

// ── Feature 4: AI Narrative Summary ──────────────────────

export interface NarrativeResponse {
  cell_id: string
  narrative: string
  data: {
    ehi_score: number
    ehi_status: string
    ndvi_current: number
    ndvi_trend: string
    fire_risk_probability: number
    is_anomaly: boolean
    species_count: number
  }
}

export const fetchNarrative = (cellId: string, region?: string) =>
  api.get<NarrativeResponse>(`/narrative/${cellId}`, { params: { region } }).then(r => r.data)

export default api
