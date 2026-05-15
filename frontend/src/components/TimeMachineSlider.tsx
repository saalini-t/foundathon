import { useState, useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import { fetchTimeMachineEHI, type EHITimelinePoint } from '../services/api'
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, ReferenceLine } from 'recharts'

interface TimeMachineSliderProps {
  region?: string
  onMonthChange?: (monthKey: string) => void
  onClose: () => void
}

function statusColor(status: string) {
  switch (status) {
    case 'excellent': return '#10b981'
    case 'good': return '#22c55e'
    case 'fair': return '#eab308'
    case 'poor': return '#f97316'
    case 'critical': return '#ef4444'
    default: return '#6b7280'
  }
}

export default function TimeMachineSlider({ region, onMonthChange, onClose }: TimeMachineSliderProps) {
  const { data, isLoading } = useQuery({
    queryKey: ['time-machine-ehi', region],
    queryFn: () => fetchTimeMachineEHI(region),
    staleTime: 5 * 60_000,
  })

  const timeline = data?.timeline ?? []
  const [sliderIndex, setSliderIndex] = useState<number>(timeline.length - 1)

  // Update slider default when data loads
  const maxIndex = Math.max(0, timeline.length - 1)
  const currentIndex = Math.min(sliderIndex, maxIndex)
  const current = timeline[currentIndex]

  const chartData = useMemo(() =>
    timeline.map((t, i) => ({
      label: t.month_key.slice(2), // "25-03" etc
      ehi: t.ehi_score,
      ndvi: +(t.average_ndvi * 100).toFixed(1),
      status: t.status,
      active: i === currentIndex,
    })),
    [timeline, currentIndex],
  )

  const handleSlider = (e: React.ChangeEvent<HTMLInputElement>) => {
    const idx = parseInt(e.target.value)
    setSliderIndex(idx)
    if (timeline[idx]) {
      onMonthChange?.(timeline[idx].month_key)
    }
  }

  return (
    <div className="bg-gray-900/95 backdrop-blur border-t border-gray-700 p-3">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-xs font-bold text-gray-300 flex items-center gap-1.5">
          ⏳ Ecosystem Time Machine
          {current && (
            <span className="text-[10px] font-normal px-2 py-0.5 rounded-full ml-2"
                  style={{ backgroundColor: statusColor(current.status) + '30', color: statusColor(current.status) }}>
              {current.month_key} — EHI {current.ehi_score} ({current.status})
            </span>
          )}
        </h3>
        <button onClick={onClose} className="text-gray-500 hover:text-gray-300 text-xs">✕</button>
      </div>

      {isLoading ? (
        <div className="flex items-center gap-2 text-xs text-gray-500 py-2">
          <svg className="animate-spin h-3 w-3" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          Loading timeline...
        </div>
      ) : timeline.length === 0 ? (
        <p className="text-xs text-gray-500 py-2">No historical data.</p>
      ) : (
        <div className="space-y-2">
          {/* Mini chart */}
          <ResponsiveContainer width="100%" height={80}>
            <AreaChart data={chartData} margin={{ top: 4, right: 4, bottom: 0, left: 4 }}>
              <defs>
                <linearGradient id="ehiGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#22c55e" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis
                dataKey="label"
                tick={{ fill: '#6b7280', fontSize: 9 }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis hide domain={[0, 100]} />
              <Tooltip
                contentStyle={{ background: '#1f2937', border: '1px solid #374151', borderRadius: 6, fontSize: 11, color: '#e5e7eb' }}
                formatter={(value: number, name: string) => [
                  name === 'ehi' ? `${value} / 100` : `${value}%`,
                  name === 'ehi' ? 'EHI Score' : 'NDVI ×100'
                ]}
              />
              <Area type="monotone" dataKey="ehi" stroke="#22c55e" fill="url(#ehiGrad)" strokeWidth={2} />
              {currentIndex < chartData.length && (
                <ReferenceLine x={chartData[currentIndex]?.label} stroke="#60a5fa" strokeDasharray="3 3" />
              )}
            </AreaChart>
          </ResponsiveContainer>

          {/* Slider */}
          <div className="flex items-center gap-3">
            <span className="text-[10px] text-gray-500 w-12">{timeline[0]?.month_key.slice(2)}</span>
            <input
              type="range"
              min={0}
              max={maxIndex}
              value={currentIndex}
              onChange={handleSlider}
              className="flex-1 h-1.5 accent-green-500 cursor-pointer"
            />
            <span className="text-[10px] text-gray-500 w-12 text-right">{timeline[maxIndex]?.month_key.slice(2)}</span>
          </div>
        </div>
      )}
    </div>
  )
}
