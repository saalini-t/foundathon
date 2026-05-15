import { useEffect } from 'react'
import { useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet.heat'

interface HeatPoint {
  lat: number
  lon: number
  species_count: number
  occurrence_count: number
}

interface Props {
  points: HeatPoint[]
}

export default function SpeciesHeatmap({ points }: Props) {
  const map = useMap()

  useEffect(() => {
    if (!points || points.length === 0) return

    const maxCount = Math.max(...points.map(p => p.species_count))
    const heatData: [number, number, number][] = points.map(p => [
      p.lat,
      p.lon,
      p.species_count / Math.max(maxCount, 1),
    ])

    const heatLayer = (L as any).heatLayer(heatData, {
      radius: 20,
      blur: 15,
      maxZoom: 12,
      max: 1.0,
      gradient: {
        0.2: '#2563eb',
        0.4: '#06b6d4',
        0.6: '#22c55e',
        0.8: '#eab308',
        1.0: '#ef4444',
      },
    })

    heatLayer.addTo(map)

    return () => {
      map.removeLayer(heatLayer)
    }
  }, [map, points])

  return null
}
