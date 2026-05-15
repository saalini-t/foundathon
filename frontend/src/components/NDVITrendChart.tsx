import { useQuery } from '@tanstack/react-query'
import { fetchNDVITimeseries } from '../services/api'
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
} from 'recharts'

interface Props {
  cellId: string | null
  onClose: () => void
  region?: string
}

export default function NDVITrendChart({ cellId, onClose, region }: Props) {
  const { data, isLoading } = useQuery({
    queryKey: ['ndvi-timeseries', cellId, region],
    queryFn: () => fetchNDVITimeseries(cellId!, region),
    enabled: !!cellId,
  })

  if (!cellId) return null

  return (
    <div className="bg-gray-800 border-t border-gray-700 p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-gray-300">
          📈 NDVI Trend — Cell {cellId}
        </h3>
        <button
          onClick={onClose}
          className="text-gray-500 hover:text-gray-300 text-lg leading-none"
          title="Close"
        >
          ×
        </button>
      </div>

      {isLoading ? (
        <div className="h-40 flex items-center justify-center text-gray-500 text-sm">
          Loading NDVI data...
        </div>
      ) : data?.timeseries ? (
        <ResponsiveContainer width="100%" height={180}>
          <AreaChart
            data={data.timeseries.map((d) => ({
              date: d.date,
              ndvi: Number(d.ndvi_mean.toFixed(3)),
              min: Number(d.ndvi_min.toFixed(3)),
              max: Number(d.ndvi_max.toFixed(3)),
            }))}
            margin={{ top: 5, right: 10, bottom: 5, left: 0 }}
          >
            <defs>
              <linearGradient id="ndviGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#22c55e" stopOpacity={0.6} />
                <stop offset="95%" stopColor="#22c55e" stopOpacity={0.05} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis
              dataKey="date"
              tick={{ fill: '#9ca3af', fontSize: 10 }}
              tickFormatter={(v: string) => v.slice(5)} // MM-DD
            />
            <YAxis
              domain={[0.1, 0.9]}
              tick={{ fill: '#9ca3af', fontSize: 10 }}
              tickFormatter={(v: number) => v.toFixed(1)}
            />
            <Tooltip
              contentStyle={{
                background: '#1f2937',
                border: '1px solid #374151',
                borderRadius: 8,
                fontSize: 12,
                color: '#e5e7eb',
              }}
            />
            <ReferenceLine
              y={0.4}
              stroke="#ef4444"
              strokeDasharray="3 3"
              label={{ value: 'Stress', fill: '#ef4444', fontSize: 10 }}
            />
            <Area
              type="monotone"
              dataKey="ndvi"
              stroke="#22c55e"
              fillOpacity={1}
              fill="url(#ndviGrad)"
              strokeWidth={2}
              dot={{ r: 3, fill: '#22c55e' }}
            />
          </AreaChart>
        </ResponsiveContainer>
      ) : (
        <div className="h-40 flex items-center justify-center text-gray-500 text-sm">
          No data for this cell
        </div>
      )}
    </div>
  )
}
