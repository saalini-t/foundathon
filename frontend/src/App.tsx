import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import MapView, { type LayerName } from './components/Map/MapView'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import NDVITrendChart from './components/NDVITrendChart'
import TimeMachineSlider from './components/TimeMachineSlider'
import { fetchPlatformStats, fetchRegions, type EHICell, type NDVICell, type Region } from './services/api'

const LAYERS: { id: LayerName; label: string; icon: string; desc: string }[] = [
  { id: 'ehi', label: 'EHI', icon: '🌿', desc: 'Ecosystem Health Index' },
  { id: 'fires', label: 'Fires', icon: '🔥', desc: 'Active fire detections' },
  { id: 'fire-risk', label: 'Fire Risk', icon: '🎯', desc: 'AI fire predictions' },
  { id: 'species', label: 'Species', icon: '🦎', desc: 'Biodiversity heatmap' },
  { id: 'ndvi', label: 'NDVI', icon: '🌳', desc: 'Vegetation index' },
  { id: 'anomalies', label: 'Anomalies', icon: '⚠️', desc: 'Ecosystem anomalies' },
]

export default function App() {
  const [activeLayer, setActiveLayer] = useState<LayerName>('ehi')
  const [selectedCell, setSelectedCell] = useState<EHICell | null>(null)
  const [ndviCellId, setNdviCellId] = useState<string | null>(null)
  const [regionId, setRegionId] = useState<string>('western_ghats')
  const [showTimeMachine, setShowTimeMachine] = useState(false)
  const [alertLocation, setAlertLocation] = useState<{ lat: number; lon: number; alertId?: number } | null>(null)

  const { data: regionsData } = useQuery({
    queryKey: ['regions'],
    queryFn: fetchRegions,
    staleTime: Infinity,
  })

  const regions = regionsData?.regions ?? []
  const currentRegion = regions.find(r => r.id === regionId)

  const { data: stats } = useQuery({
    queryKey: ['stats', regionId],
    queryFn: () => fetchPlatformStats(regionId),
  })

  const handleRegionChange = (id: string) => {
    setRegionId(id)
    setSelectedCell(null)
    setNdviCellId(null)
    setAlertLocation(null)
  }

  const handleCellSelect = (cell: EHICell | NDVICell | null) => {
    if (!cell) {
      setSelectedCell(null)
      setNdviCellId(null)
      return
    }
    // If it has ehi_score, it's an EHICell
    if ('ehi_score' in cell) {
      setSelectedCell(cell as EHICell)
    }
    // Always set NDVI cell for chart
    setNdviCellId(cell.cell_id)
  }

  return (
    <div className="h-screen flex flex-col bg-gray-900 text-white">
      <Header
        stats={stats}
        regions={regions}
        regionId={regionId}
        onRegionChange={handleRegionChange}
      />
      <div className="flex-1 flex overflow-hidden">
        {/* Map Area */}
        <div className="flex-1 flex flex-col">
          <div className="flex-1 relative">
            {/* Layer Controls */}
            <div className="absolute top-3 left-3 z-[1000] flex flex-wrap gap-1.5">
              {LAYERS.map(({ id, label, icon, desc }) => (
                <button
                  key={id}
                  onClick={() => {
                    setActiveLayer(id)
                    setSelectedCell(null)
                    setNdviCellId(null)
                    setAlertLocation(null)
                  }}
                  title={desc}
                  className={`px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 shadow-md ${
                    activeLayer === id
                      ? 'bg-green-600 text-white ring-2 ring-green-400/50 scale-105'
                      : 'bg-gray-800/90 text-gray-300 hover:bg-gray-700 hover:text-white backdrop-blur-sm'
                  }`}
                >
                  {icon} {label}
                </button>
              ))}
              <button
                onClick={() => setShowTimeMachine(!showTimeMachine)}
                title="Ecosystem Time Machine"
                className={`px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 shadow-md ${
                  showTimeMachine
                    ? 'bg-blue-600 text-white ring-2 ring-blue-400/50 scale-105'
                    : 'bg-gray-800/90 text-gray-300 hover:bg-gray-700 hover:text-white backdrop-blur-sm'
                }`}
              >
                ⏳ Timeline
              </button>
            </div>

            {/* Legend */}
            <div className="absolute bottom-3 left-3 z-[1000] bg-gray-800/90 backdrop-blur-sm rounded-lg p-2.5 text-[10px]">
              {activeLayer === 'ehi' && (
                <div className="flex gap-2 items-center">
                  <span className="text-gray-400">EHI:</span>
                  {[
                    { color: '#15803d', label: '80+' },
                    { color: '#22c55e', label: '60-79' },
                    { color: '#facc15', label: '40-59' },
                    { color: '#f97316', label: '20-39' },
                    { color: '#ef4444', label: '<20' },
                  ].map((l) => (
                    <span key={l.label} className="flex items-center gap-0.5">
                      <span className="w-2.5 h-2.5 rounded" style={{ backgroundColor: l.color }} />
                      {l.label}
                    </span>
                  ))}
                </div>
              )}
              {activeLayer === 'ndvi' && (
                <div className="flex gap-2 items-center">
                  <span className="text-gray-400">NDVI:</span>
                  {[
                    { color: '#14532d', label: '>0.7' },
                    { color: '#15803d', label: '0.6' },
                    { color: '#22c55e', label: '0.5' },
                    { color: '#86efac', label: '0.4' },
                    { color: '#fde047', label: '0.3' },
                    { color: '#f97316', label: '0.2' },
                    { color: '#dc2626', label: '<0.2' },
                  ].map((l) => (
                    <span key={l.label} className="flex items-center gap-0.5">
                      <span className="w-2.5 h-2.5 rounded" style={{ backgroundColor: l.color }} />
                      {l.label}
                    </span>
                  ))}
                </div>
              )}
              {(activeLayer === 'fire-risk') && (
                <div className="flex gap-2 items-center">
                  <span className="text-gray-400">Risk:</span>
                  {[
                    { color: '#22c55e', label: 'Low' },
                    { color: '#f97316', label: 'Moderate' },
                    { color: '#ef4444', label: 'High' },
                    { color: '#7f1d1d', label: 'Extreme' },
                  ].map((l) => (
                    <span key={l.label} className="flex items-center gap-0.5">
                      <span className="w-2.5 h-2.5 rounded" style={{ backgroundColor: l.color }} />
                      {l.label}
                    </span>
                  ))}
                </div>
              )}
              {activeLayer === 'anomalies' && (
                <div className="flex gap-2 items-center">
                  <span className="text-gray-400">Anomaly:</span>
                  {[
                    { color: '#facc15', label: 'Moderate' },
                    { color: '#f97316', label: 'High' },
                    { color: '#ef4444', label: 'Critical' },
                  ].map((l) => (
                    <span key={l.label} className="flex items-center gap-0.5">
                      <span className="w-2.5 h-2.5 rounded" style={{ backgroundColor: l.color }} />
                      {l.label}
                    </span>
                  ))}
                </div>
              )}
              {activeLayer === 'species' && (
                <div className="flex gap-2 items-center">
                  <span className="text-gray-400">Density:</span>
                  {[
                    { color: '#2563eb', label: 'Low' },
                    { color: '#06b6d4', label: '' },
                    { color: '#22c55e', label: 'Medium' },
                    { color: '#eab308', label: '' },
                    { color: '#ef4444', label: 'High' },
                  ].map((l, i) => (
                    <span key={i} className="flex items-center gap-0.5">
                      <span className="w-2.5 h-2.5 rounded" style={{ backgroundColor: l.color }} />
                      {l.label}
                    </span>
                  ))}
                </div>
              )}
              {activeLayer === 'fires' && (
                <div className="flex gap-2 items-center">
                  <span className="text-gray-400">Confidence:</span>
                  {[
                    { color: '#ef4444', label: 'High' },
                    { color: '#f97316', label: 'Nominal' },
                    { color: '#facc15', label: 'Low' },
                  ].map((l) => (
                    <span key={l.label} className="flex items-center gap-0.5">
                      <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: l.color }} />
                      {l.label}
                    </span>
                  ))}
                </div>
              )}
            </div>

            <MapView
              activeLayer={activeLayer}
              onCellSelect={handleCellSelect}
              onFireClick={(lat: number, lon: number, alertId?: number) =>
                setAlertLocation({ lat, lon, alertId })
              }
              region={regionId}
              center={currentRegion ? [currentRegion.center[0], currentRegion.center[1]] : undefined}
              zoom={currentRegion?.zoom}
            />
          </div>

          {/* Time Machine Slider */}
          {showTimeMachine && (
            <TimeMachineSlider
              region={regionId}
              onMonthChange={(month) => console.log('Time Machine month:', month)}
              onClose={() => setShowTimeMachine(false)}
            />
          )}

          {/* NDVI Trend Chart (bottom panel) */}
          {ndviCellId && (
            <NDVITrendChart
              cellId={ndviCellId}
              onClose={() => setNdviCellId(null)}
              region={regionId}
            />
          )}
        </div>

        {/* Sidebar */}
        <Sidebar
          selectedCell={selectedCell}
          region={regionId}
          alertLocation={alertLocation}
          onAlertLocationClear={() => setAlertLocation(null)}
        />
      </div>
    </div>
  )
}
