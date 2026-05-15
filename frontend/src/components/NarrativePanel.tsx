import { useQuery } from '@tanstack/react-query'
import { fetchNarrative } from '../services/api'
import { useEffect } from 'react'

interface NarrativePanelProps {
  cellId: string
  region?: string
}

function trendIcon(trend: string) {
  if (trend === 'improving') return '📈'
  if (trend === 'declining') return '📉'
  return '➡️'
}

export default function NarrativePanel({ cellId, region }: NarrativePanelProps) {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['narrative', cellId, region],
    queryFn: () => fetchNarrative(cellId, region),
    staleTime: 60_000,
    enabled: !!cellId,
    retry: 2,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 10000),
  })

  useEffect(() => {
    if (cellId) {
      console.log('[NarrativePanel] Cell selected:', cellId, 'region:', region)
    }
  }, [cellId, region])

  if (!cellId) return null

  return (
    <div className="bg-gray-800 rounded-lg p-3 space-y-2">
      <h4 className="text-[11px] text-gray-500 font-semibold uppercase tracking-wider flex items-center gap-1">
        🤖 AI Ecosystem Summary
      </h4>

      {isLoading && (
        <div className="flex items-center gap-2 text-xs text-gray-400 py-2">
          <svg className="animate-spin h-3 w-3" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          Generating summary...
        </div>
      )}

      {isError && !data && (
        <div className="text-[10px] space-y-1">
          <p className="text-red-400">Could not generate narrative.</p>
          <p className="text-gray-500 text-[9px]">{error instanceof Error ? error.message : 'Network error. Retrying...'}</p>
        </div>
      )}

      {data && (
        <>
          {/* Narrative text */}
          <p className="text-xs text-gray-300 leading-relaxed"
             dangerouslySetInnerHTML={{
               __html: data.narrative
                 .replace(/\*\*(.*?)\*\*/g, '<strong class="text-white">$1</strong>')
                 .replace(/⚠️/g, '<span class="text-yellow-400">⚠️</span>')
             }}
          />

          {/* Compact data chips */}
          <div className="flex flex-wrap gap-1.5 pt-1">
            <span className="text-[9px] px-1.5 py-0.5 rounded-full bg-gray-700 text-gray-300">
              EHI {data.data.ehi_score.toFixed(0)}
            </span>
            <span className="text-[9px] px-1.5 py-0.5 rounded-full bg-gray-700 text-gray-300">
              NDVI {data.data.ndvi_current.toFixed(2)} {trendIcon(data.data.ndvi_trend)}
            </span>
            <span className="text-[9px] px-1.5 py-0.5 rounded-full bg-gray-700 text-gray-300">
              🦎 {data.data.species_count} species
            </span>
            <span className={`text-[9px] px-1.5 py-0.5 rounded-full ${
              data.data.fire_risk_probability > 0.5
                ? 'bg-red-900/60 text-red-300'
                : 'bg-gray-700 text-gray-300'
            }`}>
              🔥 Risk {(data.data.fire_risk_probability * 100).toFixed(0)}%
            </span>
            {data.data.is_anomaly && (
              <span className="text-[9px] px-1.5 py-0.5 rounded-full bg-yellow-900/60 text-yellow-300">
                ⚠️ Anomaly
              </span>
            )}
          </div>
        </>
      )}
    </div>
  )
}
