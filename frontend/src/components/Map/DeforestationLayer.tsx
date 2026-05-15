import { Rectangle, Tooltip } from 'react-leaflet'
import type { NDVICell } from '../../services/api'

function ndviColor(ndvi: number): string {
  if (ndvi >= 0.7) return '#14532d'
  if (ndvi >= 0.6) return '#15803d'
  if (ndvi >= 0.5) return '#22c55e'
  if (ndvi >= 0.4) return '#86efac'
  if (ndvi >= 0.3) return '#fde047'
  if (ndvi >= 0.2) return '#f97316'
  return '#dc2626'
}

interface Props {
  cells: NDVICell[]
  onCellClick?: (cell: NDVICell) => void
}

export default function DeforestationLayer({ cells, onCellClick }: Props) {
  const half = 0.05

  return (
    <>
      {cells.map((cell) => {
        const bounds: [[number, number], [number, number]] = [
          [cell.center_lat - half, cell.center_lon - half],
          [cell.center_lat + half, cell.center_lon + half],
        ]
        // Low NDVI areas are highlighted more intensely (potential deforestation)
        const opacity = cell.ndvi_mean < 0.4 ? 0.7 : 0.4
        return (
          <Rectangle
            key={cell.cell_id}
            bounds={bounds}
            pathOptions={{
              color: ndviColor(cell.ndvi_mean),
              fillColor: ndviColor(cell.ndvi_mean),
              fillOpacity: opacity,
              weight: 0.3,
            }}
            eventHandlers={{
              click: () => onCellClick?.(cell),
            }}
          >
            <Tooltip sticky>
              <div className="text-xs">
                <strong>NDVI: {cell.ndvi_mean.toFixed(3)}</strong>
                <br />
                Range: {cell.ndvi_min.toFixed(2)} – {cell.ndvi_max.toFixed(2)}
                {cell.ndvi_mean < 0.35 && (
                  <>
                    <br />
                    <span className="text-red-600 font-bold">⚠ Low vegetation</span>
                  </>
                )}
              </div>
            </Tooltip>
          </Rectangle>
        )
      })}
    </>
  )
}
