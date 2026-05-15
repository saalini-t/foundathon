import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { submitVerification, fetchVerifications, type VerificationReport } from '../services/api'

interface VerificationPanelProps {
  region?: string
  alertId?: number | null
  alertLat?: number
  alertLon?: number
}

function StatusBadge({ status }: { status: string }) {
  const map: Record<string, { bg: string; text: string; label: string }> = {
    verified: { bg: 'bg-green-900/60', text: 'text-green-300', label: '✓ Verified' },
    resolved: { bg: 'bg-blue-900/60', text: 'text-blue-300', label: '✓ Resolved' },
    false_alarm: { bg: 'bg-gray-700', text: 'text-gray-300', label: '✕ False Alarm' },
  }
  const s = map[status] ?? map.verified
  return <span className={`text-[10px] px-1.5 py-0.5 rounded ${s.bg} ${s.text} font-medium`}>{s.label}</span>
}

export default function VerificationPanel({ region, alertId, alertLat, alertLon }: VerificationPanelProps) {
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [message, setMessage] = useState('')
  const [status, setStatus] = useState('verified')
  const [reporter, setReporter] = useState('')

  const { data: reportsData } = useQuery({
    queryKey: ['verifications', region],
    queryFn: () => fetchVerifications(region, 20),
    staleTime: 30_000,
  })

  const mutation = useMutation({
    mutationFn: (form: FormData) => submitVerification(form),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['verifications'] })
      setShowForm(false)
      setMessage('')
      setReporter('')
    },
  })

  const handleSubmit = () => {
    if (!message.trim()) return
    const fd = new FormData()
    fd.append('latitude', String(alertLat ?? 0))
    fd.append('longitude', String(alertLon ?? 0))
    fd.append('message', message)
    fd.append('status', status)
    if (alertId) {
      fd.append('alert_id', String(alertId))
    }
    fd.append('alert_type', 'fire')
    if (reporter.trim()) fd.append('reporter_name', reporter)
    mutation.mutate(fd)
  }

  const reports = reportsData?.reports ?? []

  return (
    <div className="p-4 border-b border-gray-700">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
          📍 Field Verifications
        </h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="text-[10px] px-2 py-1 rounded bg-green-700/60 text-green-300 hover:bg-green-700 transition"
        >
          {showForm ? 'Cancel' : '+ Report'}
        </button>
      </div>

      {/* Submit Form */}
      {showForm && (
        <div className="bg-gray-800 rounded-lg p-3 mb-3 space-y-2">
          <input
            value={reporter}
            onChange={e => setReporter(e.target.value)}
            placeholder="Your name (optional)"
            className="w-full bg-gray-700 border border-gray-600 rounded px-2 py-1 text-xs text-gray-200 placeholder-gray-500"
          />
          <textarea
            value={message}
            onChange={e => setMessage(e.target.value)}
            placeholder="e.g. Controlled burn observed — safe."
            rows={2}
            className="w-full bg-gray-700 border border-gray-600 rounded px-2 py-1 text-xs text-gray-200 placeholder-gray-500 resize-none"
          />
          <div className="flex items-center gap-2">
            <select
              value={status}
              onChange={e => setStatus(e.target.value)}
              className="bg-gray-700 border border-gray-600 rounded px-2 py-1 text-xs text-gray-200"
            >
              <option value="verified">Verified</option>
              <option value="resolved">Resolved</option>
              <option value="false_alarm">False Alarm</option>
            </select>
            <button
              onClick={handleSubmit}
              disabled={mutation.isPending || !message.trim()}
              className="flex-1 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white text-xs py-1 rounded transition"
            >
              {mutation.isPending ? 'Sending...' : 'Submit Report'}
            </button>
          </div>
          {mutation.isError && (
            <p className="text-[10px] text-red-400">Failed to submit. Try again.</p>
          )}
        </div>
      )}

      {/* Recent Reports */}
      {reports.length === 0 ? (
        <p className="text-xs text-gray-500">No field reports yet.</p>
      ) : (
        <ul className="space-y-1.5 max-h-40 overflow-y-auto">
          {reports.slice(0, 8).map(rpt => (
            <li key={rpt.id} className="bg-gray-800 rounded-lg p-2 text-xs">
              <div className="flex items-center justify-between mb-0.5">
                <span className="text-gray-400 font-medium">
                  {rpt.reporter_name || 'Field Agent'}
                </span>
                <StatusBadge status={rpt.status} />
              </div>
              <p className="text-gray-300 text-[11px]">{rpt.message}</p>
              <p className="text-[9px] text-gray-600 mt-0.5">
                {rpt.latitude.toFixed(3)}°, {rpt.longitude.toFixed(3)}°
                {rpt.created_at && ` • ${new Date(rpt.created_at).toLocaleDateString()}`}
              </p>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
