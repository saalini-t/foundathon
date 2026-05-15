import type { PlatformStats, Region } from '../services/api'

interface HeaderProps {
  stats?: PlatformStats
  regions: Region[]
  regionId: string
  onRegionChange: (id: string) => void
}

export default function Header({ stats, regions, regionId, onRegionChange }: HeaderProps) {
  const current = regions.find(r => r.id === regionId)
  const displayName = current?.name ?? 'Ecosystem Monitor'

  return (
    <header className="bg-gray-800 border-b border-gray-700 px-4 py-2.5 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <span className="text-2xl">🌿</span>
        <div>
          <h1 className="text-lg font-bold text-green-400 tracking-tight">
            {displayName}
          </h1>
          <p className="text-xs text-gray-400">
            AI-Powered Biodiversity & Environmental Intelligence
          </p>
        </div>
        {/* Region Selector */}
        {regions.length > 1 && (
          <select
            value={regionId}
            onChange={(e) => onRegionChange(e.target.value)}
            className="ml-4 bg-gray-700 text-gray-200 text-sm rounded-lg px-3 py-1.5 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500/50"
          >
            {regions.map((r) => (
              <option key={r.id} value={r.id}>
                {r.name}
              </option>
            ))}
          </select>
        )}
      </div>

      <div className="flex items-center gap-4">
        {stats && (
          <div className="flex gap-6 text-sm">
            <StatBadge label="Fire Alerts" value={stats.fire_detections} color="text-red-400" icon="🔥" />
            <StatBadge label="Species" value={stats.unique_species} color="text-green-400" icon="🧬" />
            <StatBadge label="Weather Obs." value={stats.weather_observations} color="text-blue-400" icon="🌤️" />
            <StatBadge label="Stations" value={stats.weather_stations} color="text-yellow-400" icon="📡" />
          </div>
        )}
        <div className="flex items-center gap-1.5 bg-green-900/30 border border-green-800/50 rounded-full px-3 py-1">
          <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
          <span className="text-xs text-green-400 font-medium">Live</span>
        </div>
      </div>
    </header>
  )
}

function StatBadge({ label, value, color, icon }: { label: string; value: number; color: string; icon: string }) {
  return (
    <div className="text-center">
      <div className={`font-bold ${color}`}>{icon} {value.toLocaleString()}</div>
      <div className="text-gray-500 text-xs">{label}</div>
    </div>
  )
}
