import { useQuery } from '@tanstack/react-query'
import {
  fetchFireAlerts,
  fetchCurrentWeather,
  fetchSpeciesSummary,
  fetchEHI,
  type FireAlert,
  type CurrentWeather,
  type SpeciesSummary,
  type EHICell,
} from '../services/api'
import AlertFeed from './AlertFeed'
import ContextPanel from './ContextPanel'
import NarrativePanel from './NarrativePanel'
import VerificationPanel from './VerificationPanel'
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
} from 'recharts'

interface SidebarProps {
  selectedCell?: EHICell | null
  region?: string
  alertLocation?: { lat: number; lon: number; alertId?: number } | null
  onAlertLocationClear?: () => void
}

function MiniBar({ label, value, max = 100, color }: { label: string; value: number; max?: number; color: string }) {
  const pct = Math.min(100, (value / max) * 100)
  return (
    <div className="flex items-center gap-2 text-xs">
      <span className="w-24 text-gray-400 truncate">{label}</span>
      <div className="flex-1 bg-gray-700 rounded-full h-1.5">
        <div className="h-1.5 rounded-full" style={{ width: `${pct}%`, backgroundColor: color }} />
      </div>
      <span className="w-8 text-right font-mono text-gray-300">{value.toFixed(0)}</span>
    </div>
  )
}

function ehiStatusColor(status: string) {
  switch (status) {
    case 'excellent': return 'text-emerald-400'
    case 'good': return 'text-green-400'
    case 'fair': return 'text-yellow-400'
    case 'poor': return 'text-orange-400'
    case 'critical': return 'text-red-400'
    default: return 'text-gray-400'
  }
}

function ehiRingColor(score: number) {
  if (score >= 80) return 'from-emerald-500 to-green-600'
  if (score >= 60) return 'from-green-500 to-lime-500'
  if (score >= 40) return 'from-yellow-500 to-amber-500'
  if (score >= 20) return 'from-orange-500 to-red-500'
  return 'from-red-600 to-red-800'
}

export default function Sidebar({ selectedCell, region, alertLocation, onAlertLocationClear }: SidebarProps) {
  const { data: ehiData } = useQuery({
    queryKey: ['ehi-sidebar', region],
    queryFn: () => fetchEHI(region),
    staleTime: 5 * 60_000,
  })

  const { data: weatherData, isLoading: weatherLoading, isError: weatherError } = useQuery({
    queryKey: ['weather-current', region],
    queryFn: () => fetchCurrentWeather(region),
    refetchInterval: 120_000,
    retry: 1,
  })

  const { data: speciesData, isLoading: speciesLoading } = useQuery({
    queryKey: ['species-summary', region],
    queryFn: () => fetchSpeciesSummary(50, region),
    retry: 1,
  })

  const weather = weatherData?.stations
  const species = speciesData?.species

  // Use selected cell or platform average
  const displayCell = selectedCell
  const avgEHI = ehiData?.average_ehi ?? 0
  const statusDist = ehiData?.status_distribution ?? {}

  const barData = Object.entries(statusDist).map(([status, count]) => ({
    status: status.charAt(0).toUpperCase() + status.slice(1),
    count,
    fill: status === 'excellent' ? '#10b981'
        : status === 'good' ? '#22c55e'
        : status === 'fair' ? '#eab308'
        : status === 'poor' ? '#f97316'
        : '#ef4444',
  }))

  return (
    <aside className="w-80 bg-gray-900 text-gray-100 overflow-y-auto flex flex-col border-l border-gray-700">
      {/* EHI Summary */}
      <div className="p-4 border-b border-gray-700">
        <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
          Ecosystem Health Index
        </h2>

        {displayCell ? (
          // Selected cell detail
          <div>
            <div className="flex items-center gap-3 mb-3">
              <div className={`w-14 h-14 rounded-full bg-gradient-to-br ${ehiRingColor(displayCell.ehi_score)} flex items-center justify-center shadow-lg`}>
                <span className="text-xl font-bold text-white">{displayCell.ehi_score.toFixed(0)}</span>
              </div>
              <div>
                <p className={`text-lg font-semibold capitalize ${ehiStatusColor(displayCell.status)}`}>
                  {displayCell.status}
                </p>
                <p className="text-[10px] text-gray-500">Cell {displayCell.cell_id}</p>
              </div>
            </div>
            <div className="space-y-1.5">
              <MiniBar label="Vegetation" value={displayCell.sub_indices.vegetation_health} color="#22c55e" />
              <MiniBar label="Forest" value={displayCell.sub_indices.forest_integrity} color="#15803d" />
              <MiniBar label="Biodiversity" value={displayCell.sub_indices.biodiversity_richness} color="#06b6d4" />
              <MiniBar label="Climate" value={displayCell.sub_indices.climate_stability} color="#8b5cf6" />
              <MiniBar label="Air Quality" value={displayCell.sub_indices.air_quality} color="#64748b" />
              <MiniBar label="Fire Risk" value={displayCell.sub_indices.fire_disturbance} color="#ef4444" />
            </div>
          </div>
        ) : (
          // Platform average
          <div>
            <div className="flex items-center gap-3 mb-3">
              <div className={`w-14 h-14 rounded-full bg-gradient-to-br ${ehiRingColor(avgEHI)} flex items-center justify-center shadow-lg`}>
                <span className="text-xl font-bold text-white">{avgEHI.toFixed(0)}</span>
              </div>
              <div>
                <p className="text-sm font-semibold text-green-400">Platform Average</p>
                <p className="text-[10px] text-gray-500">
                  {ehiData?.count ?? 0} grid cells monitored
                </p>
              </div>
            </div>
            {barData.length > 0 && (
              <ResponsiveContainer width="100%" height={80}>
                <BarChart data={barData} margin={{ top: 0, right: 0, bottom: 0, left: 0 }}>
                  <XAxis dataKey="status" tick={{ fill: '#9ca3af', fontSize: 9 }} axisLine={false} tickLine={false} />
                  <YAxis hide />
                  <Tooltip
                    contentStyle={{ background: '#1f2937', border: '1px solid #374151', borderRadius: 6, fontSize: 11, color: '#e5e7eb' }}
                  />
                  <Bar dataKey="count" radius={[3, 3, 0, 0]}>
                    {barData.map((d, i) => (
                      <Cell key={i} fill={d.fill} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        )}
      </div>

      {/* AI Narrative for selected cell */}
      {selectedCell && (
        <div className="border-b border-gray-700">
          <NarrativePanel cellId={selectedCell.cell_id} region={region ?? 'western_ghats'} />
        </div>
      )}

      {/* Contextual Alert Panel */}
      {alertLocation && (
        <div className="border-b border-gray-700">
          <ContextPanel
            lat={alertLocation.lat}
            lon={alertLocation.lon}
            region={region ?? 'western_ghats'}
            onClose={() => onAlertLocationClear?.()}
          />
        </div>
      )}

      {/* Ground Truth Verification */}
      {alertLocation && (
        <div className="border-b border-gray-700">
          <VerificationPanel
            region={region ?? 'western_ghats'}
            alertId={alertLocation.alertId}
            alertLat={alertLocation.lat}
            alertLon={alertLocation.lon}
          />
        </div>
      )}

      {/* Alert Feed */}
      <AlertFeed region={region} />

      {/* Weather Stations */}
      <div className="p-4 border-b border-gray-700">
        <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
          🌤️ Weather Stations
        </h2>
        {weatherLoading ? (
          <div className="flex items-center gap-2 text-xs text-gray-500">
            <svg className="animate-spin h-3 w-3" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" /><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
            Loading weather...
          </div>
        ) : weatherError ? (
          <p className="text-xs text-gray-500">Weather data unavailable</p>
        ) : weather && weather.length > 0 ? (
          <ul className="space-y-1.5 max-h-40 overflow-y-auto">
            {weather.slice(0, 6).map((w: CurrentWeather, i: number) => (
              <li key={`w-${i}`} className="text-xs bg-gray-800 rounded p-2 flex items-center justify-between">
                <span className="font-medium text-blue-300 truncate max-w-[100px]">{w.station_name}</span>
                <div className="flex gap-2 text-gray-400">
                  <span>{w.temperature !== null ? `${w.temperature}°` : '—'}</span>
                  <span>💧{w.humidity ?? '—'}%</span>
                  <span>🌧{w.precipitation ?? 0}mm</span>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-xs text-gray-500">No weather data</p>
        )}
      </div>

      {/* Species */}
      <div className="p-4">
        <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
          🦎 Top Species
        </h2>
        {speciesLoading ? (
          <div className="flex items-center gap-2 text-xs text-gray-500">
            <svg className="animate-spin h-3 w-3" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" /><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" /></svg>
            Loading species...
          </div>
        ) : species && species.length > 0 ? (
          <ul className="space-y-1 max-h-36 overflow-y-auto">
            {species.slice(0, 10).map((s: SpeciesSummary, i: number) => (
              <li key={`sp-${i}`} className="text-xs flex justify-between items-center bg-gray-800 rounded px-2 py-1">
                <span className="text-green-300 italic truncate max-w-[160px]">{s.species}</span>
                <span className="text-gray-500 font-mono text-[10px]">{s.occurrence_count}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-xs text-gray-500">No species data</p>
        )}
      </div>
    </aside>
  )
}
