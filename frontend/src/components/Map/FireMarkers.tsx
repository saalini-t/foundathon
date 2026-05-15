import { CircleMarker, Popup } from 'react-leaflet'
import type { FireAlert } from '../../services/api'

interface Props {
  fires: FireAlert[]
  onFireClick?: (lat: number, lon: number, alertId?: number) => void
}

function fireColor(confidence: string): string {
  switch (confidence) {
    case 'high': return '#ef4444'
    case 'nominal': return '#f97316'
    default: return '#facc15'
  }
}

function fireRadius(frp: number): number {
  if (frp > 50) return 10
  if (frp > 20) return 8
  if (frp > 5) return 6
  return 5
}

export default function FireMarkers({ fires, onFireClick }: Props) {
  return (
    <>
      {fires.map((f, i) => (
        <CircleMarker
          key={`fire-${f.id ?? i}`}
          center={[f.latitude, f.longitude]}
          radius={fireRadius(f.frp)}
          pathOptions={{
            color: fireColor(f.confidence),
            fillColor: fireColor(f.confidence),
            fillOpacity: 0.85,
            weight: 1.5,
          }}
          eventHandlers={{
            click: () => onFireClick?.(f.latitude, f.longitude, f.id),
          }}
        >
          <Popup>
            <div className="text-sm min-w-[200px]">
              <p className="font-bold text-red-400 text-base mb-2">🔥 Fire Detection</p>
              <table className="text-xs w-full">
                <tbody>
                  <tr><td className="font-medium pr-3 py-0.5 text-gray-400">Date</td><td className="text-gray-200">{f.acq_date}</td></tr>
                  <tr><td className="font-medium pr-3 py-0.5 text-gray-400">Time</td><td className="text-gray-200">{f.acq_time}</td></tr>
                  <tr><td className="font-medium pr-3 py-0.5 text-gray-400">Confidence</td><td className="text-gray-200 capitalize">{f.confidence}</td></tr>
                  <tr><td className="font-medium pr-3 py-0.5 text-gray-400">FRP</td><td className="text-gray-200">{f.frp} MW</td></tr>
                  <tr><td className="font-medium pr-3 py-0.5 text-gray-400">Brightness</td><td className="text-gray-200">{f.brightness?.toFixed(1)} K</td></tr>
                  <tr><td className="font-medium pr-3 py-0.5 text-gray-400">Satellite</td><td className="text-gray-200">{f.satellite === 'N' ? 'Suomi NPP' : 'NOAA-20'}</td></tr>
                  <tr>
                    <td className="font-medium pr-3 py-0.5 text-gray-400">Location</td>
                    <td className="text-gray-200">{f.latitude.toFixed(4)}°N, {f.longitude.toFixed(4)}°E</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </Popup>
        </CircleMarker>
      ))}
    </>
  )
}
