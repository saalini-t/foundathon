import { useQuery } from '@tanstack/react-query'
import { fetchAlertContext, type AlertContext } from '../services/api'

interface ContextPanelProps {
  lat: number
  lon: number
  region?: string
  onClose: () => void
}

function RiskBadge({ level }: { level: string }) {
  const colors: Record<string, string> = {
    high: 'bg-red-900/70 text-red-300',
    extreme: 'bg-red-900/90 text-red-200',
    moderate: 'bg-orange-900/70 text-orange-300',
    low: 'bg-green-900/70 text-green-300',
  }
  return (
    <span className={`text-[10px] px-2 py-0.5 rounded-full font-semibold uppercase ${colors[level] ?? colors.moderate}`}>
      {level}
    </span>
  )
}

export default function ContextPanel({ lat, lon, region, onClose }: ContextPanelProps) {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['alert-context', lat, lon, region],
    queryFn: () => fetchAlertContext(lat, lon, region),
    staleTime: 60_000,
  })

  return (
    <div className="bg-gray-850 border border-gray-700 rounded-xl p-4 space-y-3 animate-in fade-in">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-bold text-white flex items-center gap-1.5">
          📋 Alert Context & Playbook
        </h3>
        <button onClick={onClose} className="text-gray-500 hover:text-gray-300 text-xs">✕</button>
      </div>

      {isLoading && (
        <div className="flex items-center gap-2 text-xs text-gray-400 py-4">
          <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          Analyzing environment...
        </div>
      )}

      {isError && <p className="text-xs text-red-400">Failed to load context data.</p>}

      {data && (
        <>
          {/* Risk badge */}
          <div className="flex items-center gap-2">
            <span className="text-xs text-gray-400">
              {lat.toFixed(3)}°, {lon.toFixed(3)}°
            </span>
            <RiskBadge level={data.context.estimated_fire_risk} />
          </div>

          {/* Environmental Context */}
          <div className="bg-gray-800 rounded-lg p-3 space-y-2">
            <h4 className="text-[11px] text-gray-500 font-semibold uppercase tracking-wider">Environment</h4>
            <div className="grid grid-cols-1 gap-1.5 text-xs">
              <div className="flex justify-between">
                <span className="text-gray-400">🏘️ Nearest Village</span>
                <span className="text-white font-medium">{data.context.nearest_village.name} — {data.context.nearest_village.distance_km} km</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">🛣️ Nearest Road</span>
                <span className="text-white font-medium">{data.context.nearest_road.distance_km} km</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">🌲 Protected Area</span>
                <span className="text-white font-medium">
                  {data.context.nearest_protected_area.name} — {data.context.nearest_protected_area.distance_km} km
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">🌿 Vegetation</span>
                <span className={`font-medium ${
                  data.context.vegetation_density === 'Very High' || data.context.vegetation_density === 'High'
                    ? 'text-green-400'
                    : data.context.vegetation_density === 'Moderate'
                    ? 'text-yellow-400'
                    : 'text-orange-400'
                }`}>
                  {data.context.vegetation_density} (NDVI {data.context.ndvi_value})
                </span>
              </div>
              {data.context.inside_protected_area && (
                <div className="bg-yellow-900/30 border border-yellow-700/50 rounded px-2 py-1 text-yellow-300 text-[10px]">
                  ⚠️ Inside or adjacent to a Protected Area
                </div>
              )}
            </div>
          </div>

          {/* Playbook */}
          <div className="bg-gray-800 rounded-lg p-3 space-y-2">
            <h4 className="text-[11px] text-gray-500 font-semibold uppercase tracking-wider">
              {data.playbook.title}
            </h4>
            <ul className="space-y-1.5">
              {data.playbook.recommended_actions.map((action, i) => (
                <li key={i} className="flex items-start gap-2 text-xs text-gray-300">
                  <span className="text-green-500 mt-0.5 flex-shrink-0">▸</span>
                  {action}
                </li>
              ))}
            </ul>
          </div>
        </>
      )}
    </div>
  )
}
