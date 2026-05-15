import { Rectangle, Tooltip } from 'react-leaflet'
import type { FireRiskCell } from '../../services/api'

function riskColor(level: string): string {
  switch (level) {
    case 'extreme': return '#7f1d1d'
    case 'high':    return '#ef4444'
    case 'moderate': return '#f97316'
    default:        return '#22c55e'
  }
}

function riskOpacity(prob: number): number {
  return 0.15 + prob * 0.55
}

interface Props {
  cells: FireRiskCell[]
}

export default function FireRiskLayer({ cells }: Props) {
  const half = 0.05

  return (
    <>
      {cells.map((cell) => {
        const bounds: [[number, number], [number, number]] = [
          [cell.center_lat - half, cell.center_lon - half],
          [cell.center_lat + half, cell.center_lon + half],
        ]
        return (
          <Rectangle
            key={cell.cell_id}
            bounds={bounds}
            pathOptions={{
              color: riskColor(cell.risk_level),
              fillColor: riskColor(cell.risk_level),
              fillOpacity: riskOpacity(cell.risk_probability),
              weight: 0.3,
            }}
          >
            <Tooltip sticky>
              <div className="text-xs">
                <strong>Fire Risk: {(cell.risk_probability * 100).toFixed(1)}%</strong>
                <br />
                Level: <span className="capitalize">{cell.risk_level}</span>
              </div>
            </Tooltip>
          </Rectangle>
        )
      })}
    </>
  )
}
