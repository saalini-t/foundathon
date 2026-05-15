import { useEffect } from 'react'
import { MapContainer, TileLayer, GeoJSON, Rectangle, Tooltip, useMap } from 'react-leaflet'
import { useQuery } from '@tanstack/react-query'
import {
  fetchBoundary,
  fetchFireAlerts,
  fetchSpeciesHeatmap,
  fetchEHI,
  fetchFireRisk,
  fetchNDVILatest,
  fetchAnomalies,
  type EHICell,
  type NDVICell,
} from '../../services/api'
import type { LatLngExpression } from 'leaflet'

import EHIChoropleth from './EHIChoropleth'
import FireMarkers from './FireMarkers'
import SpeciesHeatmap from './SpeciesHeatmap'
import FireRiskLayer from './FireRiskLayer'
import DeforestationLayer from './DeforestationLayer'

const DEFAULT_CENTER: LatLngExpression = [13.5, 75.8]
const DEFAULT_ZOOM = 6

export type LayerName = 'ehi' | 'fires' | 'fire-risk' | 'species' | 'ndvi' | 'anomalies'

interface MapViewProps {
  activeLayer: LayerName
  onCellSelect?: (cell: EHICell | NDVICell | null) => void
  onFireClick?: (lat: number, lon: number, alertId?: number) => void
  region?: string
  center?: [number, number]
  zoom?: number
}

function FlyToRegion({ center, zoom }: { center: LatLngExpression; zoom: number }) {
  const map = useMap()
  useEffect(() => {
    map.flyTo(center, zoom, { duration: 1.2 })
  }, [map, center, zoom])
  return null
}

export default function MapView({ activeLayer, onCellSelect, onFireClick, region, center, zoom }: MapViewProps) {
  const mapCenter: LatLngExpression = center ?? DEFAULT_CENTER
  const mapZoom = zoom ?? DEFAULT_ZOOM

  const { data: boundary } = useQuery({
    queryKey: ['boundary', region],
    queryFn: () => fetchBoundary(region),
  })

  const { data: ehiData, isLoading: ehiLoading } = useQuery({
    queryKey: ['ehi', region],
    queryFn: () => fetchEHI(region),
    enabled: activeLayer === 'ehi',
    staleTime: 5 * 60_000,
  })

  const { data: firesData, isLoading: firesLoading } = useQuery({
    queryKey: ['fires-map', region],
    queryFn: () => fetchFireAlerts(30, region),
    enabled: activeLayer === 'fires',
  })

  const { data: fireRiskData, isLoading: fireRiskLoading } = useQuery({
    queryKey: ['fire-risk', region],
    queryFn: () => fetchFireRisk(region),
    enabled: activeLayer === 'fire-risk',
    staleTime: 5 * 60_000,
  })

  const { data: heatmapData, isLoading: speciesLoading } = useQuery({
    queryKey: ['species-heatmap', region],
    queryFn: () => fetchSpeciesHeatmap(region),
    enabled: activeLayer === 'species',
  })

  const { data: ndviData, isLoading: ndviLoading } = useQuery({
    queryKey: ['ndvi-latest', region],
    queryFn: () => fetchNDVILatest(region),
    enabled: activeLayer === 'ndvi',
    staleTime: 5 * 60_000,
  })

  const { data: anomalyData, isLoading: anomalyLoading } = useQuery({
    queryKey: ['anomalies', region],
    queryFn: () => fetchAnomalies(region),
    enabled: activeLayer === 'anomalies',
    staleTime: 5 * 60_000,
  })

  const isLoading =
    (activeLayer === 'ehi' && ehiLoading) ||
    (activeLayer === 'fires' && firesLoading) ||
    (activeLayer === 'fire-risk' && fireRiskLoading) ||
    (activeLayer === 'species' && speciesLoading) ||
    (activeLayer === 'ndvi' && ndviLoading) ||
    (activeLayer === 'anomalies' && anomalyLoading)

  return (
    <div className="relative h-full w-full">
      {isLoading && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[1001] bg-gray-900/70 backdrop-blur-sm rounded-xl px-5 py-3 flex items-center gap-3">
          <svg className="animate-spin h-5 w-5 text-green-400" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <span className="text-sm text-gray-300">Loading layer data...</span>
        </div>
      )}
      <MapContainer
        center={mapCenter}
        zoom={mapZoom}
        className="h-full w-full"
        zoomControl={true}
      >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
      />
      <FlyToRegion center={mapCenter} zoom={mapZoom} />

      {/* Western Ghats boundary */}
      {boundary && (
        <GeoJSON
          key={`boundary-${region}`}
          data={boundary as GeoJSON.FeatureCollection}
          style={{
            color: '#22c55e',
            weight: 2,
            fillOpacity: 0.03,
            fillColor: '#22c55e',
          }}
          filter={(feature) => feature.geometry.type === 'Polygon'}
        />
      )}

      {/* EHI Choropleth */}
      {activeLayer === 'ehi' && ehiData?.cells && (
        <EHIChoropleth
          cells={ehiData.cells}
          onCellClick={(c) => onCellSelect?.(c)}
        />
      )}

      {/* Fire Alert Markers */}
      {activeLayer === 'fires' && firesData?.alerts && (
        <FireMarkers fires={firesData.alerts} onFireClick={onFireClick} />
      )}

      {/* Fire Risk Grid */}
      {activeLayer === 'fire-risk' && fireRiskData?.predictions && (
        <FireRiskLayer cells={fireRiskData.predictions} />
      )}

      {/* Species Heatmap */}
      {activeLayer === 'species' && heatmapData?.points && (
        <SpeciesHeatmap points={heatmapData.points} />
      )}

      {/* NDVI / Deforestation */}
      {activeLayer === 'ndvi' && ndviData?.cells && (
        <DeforestationLayer
          cells={ndviData.cells}
          onCellClick={(c) => onCellSelect?.(c)}
        />
      )}

      {/* Anomalies — highlight anomalous cells */}
      {activeLayer === 'anomalies' && anomalyData?.anomalies?.map((a) => {
        const half = 0.05
        const bounds: [[number, number], [number, number]] = [
          [a.center_lat - half, a.center_lon - half],
          [a.center_lat + half, a.center_lon + half],
        ]
        const color = a.severity_label === 'critical' ? '#ef4444'
                    : a.severity_label === 'high' ? '#f97316'
                    : '#facc15'
        return (
          <Rectangle
            key={`anomaly-${a.cell_id}`}
            bounds={bounds}
            pathOptions={{
              color,
              fillColor: '#ef4444',
              fillOpacity: 0.4 + a.severity * 0.4,
              weight: 2,
              dashArray: '4',
            }}
          >
            <Tooltip sticky>
              <div className="text-xs">
                <strong className="text-red-600">⚠ Anomaly: {a.severity_label}</strong>
                <br />Score: {a.anomaly_score.toFixed(3)}
                {a.factors?.map((f, i) => (
                  <div key={i}>• {f}</div>
                ))}
              </div>
            </Tooltip>
          </Rectangle>
        )
      })}
    </MapContainer>
    </div>
  )
}
