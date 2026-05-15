import { useQuery } from '@tanstack/react-query'
import { fetchFireAlerts, fetchAnomalies, type FireAlert, type AnomalyCell } from '../services/api'

interface AlertFeedProps {
  region?: string
}

export default function AlertFeed({ region }: AlertFeedProps) {
  const { data: fireData } = useQuery({
    queryKey: ['fires-feed', region],
    queryFn: () => fetchFireAlerts(7, region),
    refetchInterval: 60_000,
  })

  const { data: anomalyData } = useQuery({
    queryKey: ['anomalies-feed', region],
    queryFn: () => fetchAnomalies(region),
    staleTime: 5 * 60_000,
  })

  const fires = fireData?.alerts ?? []
  const anomalies = anomalyData?.anomalies ?? []

  // Merge into a single feed, sorted by severity
  type FeedItem =
    | { type: 'fire'; data: FireAlert }
    | { type: 'anomaly'; data: AnomalyCell }

  const feed: FeedItem[] = [
    ...fires.slice(0, 8).map((f): FeedItem => ({ type: 'fire', data: f })),
    ...anomalies.slice(0, 5).map((a): FeedItem => ({ type: 'anomaly', data: a })),
  ]

  return (
    <div className="p-4 border-b border-gray-700">
      <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">
        ⚡ Live Alert Feed
      </h2>

      {feed.length === 0 ? (
        <p className="text-xs text-gray-500">No active alerts</p>
      ) : (
        <ul className="space-y-2 max-h-64 overflow-y-auto">
          {feed.map((item, i) => {
            if (item.type === 'fire') {
              const f = item.data
              return (
                <li key={`fire-${i}`} className="bg-gray-800 rounded-lg p-2.5 border-l-2 border-red-500">
                  <div className="flex items-start gap-2">
                    <span className="text-base">🔥</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-medium text-red-400">Fire Detection</span>
                        <span className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${
                          f.confidence === 'high'
                            ? 'bg-red-900/60 text-red-300'
                            : 'bg-orange-900/60 text-orange-300'
                        }`}>
                          {f.confidence}
                        </span>
                      </div>
                      <p className="text-[11px] text-gray-400 mt-0.5">
                        {f.latitude.toFixed(3)}°N, {f.longitude.toFixed(3)}°E
                      </p>
                      <p className="text-[10px] text-gray-500">
                        {f.acq_date} • FRP: {f.frp} MW • {f.satellite}
                      </p>
                    </div>
                  </div>
                </li>
              )
            } else {
              const a = item.data
              return (
                <li key={`anom-${i}`} className="bg-gray-800 rounded-lg p-2.5 border-l-2 border-yellow-500">
                  <div className="flex items-start gap-2">
                    <span className="text-base">⚠️</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-medium text-yellow-400">Anomaly</span>
                        <span className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${
                          a.severity_label === 'critical'
                            ? 'bg-red-900/60 text-red-300'
                            : a.severity_label === 'high'
                            ? 'bg-orange-900/60 text-orange-300'
                            : 'bg-yellow-900/60 text-yellow-300'
                        }`}>
                          {a.severity_label}
                        </span>
                      </div>
                      <p className="text-[11px] text-gray-400 mt-0.5">
                        Cell {a.cell_id} ({a.center_lat.toFixed(2)}°N, {a.center_lon.toFixed(2)}°E)
                      </p>
                      {a.factors && a.factors.length > 0 && (
                        <p className="text-[10px] text-gray-500 truncate">
                          {a.factors[0]}
                        </p>
                      )}
                    </div>
                  </div>
                </li>
              )
            }
          })}
        </ul>
      )}
    </div>
  )
}
