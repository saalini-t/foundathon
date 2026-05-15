import { GeoJSON } from 'react-leaflet'
import L from 'leaflet'
import type { EHICell } from '../../services/api'

function ehiColor(score: number): string {
  if (score >= 80) return '#15803d'
  if (score >= 60) return '#22c55e'
  if (score >= 40) return '#facc15'
  if (score >= 20) return '#f97316'
  return '#ef4444'
}

interface Props {
  cells: EHICell[]
  onCellClick?: (cell: EHICell) => void
}

export default function EHIChoropleth({ cells, onCellClick }: Props) {
  const geoJSON = {
    type: 'FeatureCollection' as const,
    features: cells.map(cell => ({
      type: 'Feature' as const,
      properties: {
        ehi_score: cell.ehi_score,
        status: cell.status,
        cell_id: cell.cell_id,
      },
      geometry: {
        type: 'Polygon' as const,
        coordinates: [[
          [cell.center_lon - 0.05, cell.center_lat - 0.05],
          [cell.center_lon + 0.05, cell.center_lat - 0.05],
          [cell.center_lon + 0.05, cell.center_lat + 0.05],
          [cell.center_lon - 0.05, cell.center_lat + 0.05],
          [cell.center_lon - 0.05, cell.center_lat - 0.05],
        ]],
      },
    })),
  }

  const onEachFeature = (feature: any, layer: L.Layer) => {
    const props = feature.properties
    layer.bindPopup(`<div class="text-xs"><strong>EHI: ${props.ehi_score}</strong> — ${props.status}</div>`)
    
    if (onCellClick) {
      layer.on('click', () => {
        const cell = cells.find(c => c.cell_id === props.cell_id)
        if (cell) onCellClick(cell)
      })
    }
  }

  const style = (feature: any) => ({
    color: ehiColor(feature.properties.ehi_score),
    fillColor: ehiColor(feature.properties.ehi_score),
    fillOpacity: 0.55,
    weight: 0.3,
  })

  return <GeoJSON data={geoJSON} style={style} onEachFeature={onEachFeature} />
}
