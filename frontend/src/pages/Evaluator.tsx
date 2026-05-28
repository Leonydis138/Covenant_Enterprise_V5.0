import { useState, useRef, useEffect } from 'react'
import { Zap, Eye, GitBranch, Shield, Brain, CheckCircle, XCircle, AlertTriangle, Loader2, Send } from 'lucide-react'
import { fetchJson } from '@/lib/api'

interface AgentResult {
  agent_id: string
  agent_name: string
  result: Record<string, unknown>
  latency_ms: number
}

interface EvalResult {
  evaluation_id: string
  composite_verdict: string
  composite_score: number
  risk_level: string
  axioms_violated: string[]
  agent_results: AgentResult[]
  multiverse_compliance: number
  futures_simulated: number
  superintelligence_reflection: string
  latency_ms: number
}

type StreamMsg =
  | { type: 'start'; agents: string[] }
  | { type: 'agent_result'; agent_id: string; agent_name: string; result: Record<string, unknown>; latency_ms: number }
  | { type: 'agent_error'; agent_id: string; error: string }
  | { type: 'complete' }

const AGENT_META: Record<string, { icon: typeof Eye; color: string }> = {
  observer_protector: { icon: Eye, color: 'text-blue-400' },
  quantum_risk: { icon: GitBranch, color: 'text-yellow-400' },
  constitutional_engine: { icon: Shield, color: 'text-green-400' },
  strategic_nexus: { icon: Brain, color: 'text-purple-400' },
}

const PRESETS = [
  'Deploy untested code directly to production',
  'Share private user data with a third party for revenue',
  'Delete all user accounts permanently',
  'Revert the database to last known good checkpoint',
  'Is blocking a user from observing system state ethical?',
]

function VerdictBadge({ verdict }: { verdict: string }) {
  if (verdict === 'EXECUTE' || verdict === 'COMPLIANT')
    return <span className="flex items-center gap-1 text-green-400 font-bold text-sm"><CheckCircle className="w-4 h-4" /> {verdict}</span>
  if (verdict === 'BLOCK' || verdict === 'VIOLATION' || verdict === 'CRITICAL')
    return <span className="flex items-center gap-1 text-red-400 font-bold text-sm"><XCircle className="w-4 h-4" /> {verdict}</span>
  return <span className="flex items-center gap-1 text-yellow-400 font-bold text-sm"><AlertTriangle className="w-4 h-4" /> {verdict}</span>
}

function ScoreBar({ score }: { score: number }) {
  const pct = Math.round(score * 100)
  const color = pct >= 90 ? 'bg-green-500' : pct >= 70 ? 'bg-yellow-500' : 'bg-red-500'
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 bg-gray-700 rounded-full overflow-hidden">
        <div className={`h-full ${color} transition-all duration-700`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-xs font-mono text-gray-400">{pct}%</span>
    </div>
  )
}

function resultText(result: Record<string, unknown> | undefined, key: string): string | null {
  const value = result?.[key]
  if (value === undefined || value === null || value === '') return null
  return typeof value === 'string' ? value : JSON.stringify(value)
}

export default function Evaluator() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [streamAgents, setStreamAgents] = useState<Record<string, { result?: Record<string, unknown>; latency_ms?: number; error?: string }>>({})
  const [finalResult, setFinalResult] = useState<EvalResult | null>(null)
  const [mode, setMode] = useState<'http' | 'ws'>('http')
  const [error, setError] = useState<string | null>(null)
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => () => { wsRef.current?.close() }, [])

  const runHttp = async () => {
    setLoading(true)
    setStreamAgents({})
    setFinalResult(null)
    setError(null)
    try {
      const data = await fetchJson<EvalResult>('/api/quantum_evaluate', {
        method: 'POST',
        body: JSON.stringify({ text: query, strictness: 'ultimate' }),
      })
      setFinalResult(data)
      const agentMap: Record<string, { result: Record<string, unknown>; latency_ms: number }> = {}
      data.agent_results.forEach(a => { agentMap[a.agent_id] = { result: a.result, latency_ms: a.latency_ms } })
      setStreamAgents(agentMap)
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setLoading(false)
    }
  }

  const runWs = () => {
    if (!query.trim()) return
    setLoading(true)
    setStreamAgents({})
    setFinalResult(null)
    setError(null)
    const proto = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const ws = new WebSocket(`${proto}://${window.location.host}/api/ws/evaluate`)
    wsRef.current = ws
    ws.onopen = () => ws.send(JSON.stringify({ text: query }))
    ws.onmessage = evt => {
      const msg: StreamMsg = JSON.parse(evt.data)
      if (msg.type === 'agent_result') {
        setStreamAgents(prev => ({ ...prev, [msg.agent_id]: { result: msg.result, latency_ms: msg.latency_ms } }))
      } else if (msg.type === 'agent_error') {
        setStreamAgents(prev => ({ ...prev, [msg.agent_id]: { error: msg.error } }))
      } else if (msg.type === 'complete') {
        setLoading(false)
        ws.close()
      }
    }
    ws.onerror = () => { setError('WebSocket connection failed. Try HTTP mode.'); setLoading(false) }
    ws.onclose = () => setLoading(false)
  }

  const run = () => {
    if (!query.trim()) return
    if (mode === 'http') {
      runHttp()
    } else {
      runWs()
    }
  }

  const verdictColor = finalResult?.composite_verdict === 'EXECUTE' ? 'border-green-500/40 bg-green-500/5'
    : finalResult?.composite_verdict === 'BLOCK' ? 'border-red-500/40 bg-red-500/5'
    : 'border-yellow-500/40 bg-yellow-500/5'

  return (
    <div className="p-8 space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold text-white">Constitutional Evaluator</h1>
        <p className="text-gray-400 text-sm mt-1">4-Agent parallel evaluation — 10,000 futures per query</p>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 space-y-4">
        <div className="flex items-center gap-3">
          <span className="text-xs text-gray-500">Mode:</span>
          {(['http', 'ws'] as const).map(m => (
            <button key={m} onClick={() => setMode(m)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                mode === m ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'text-gray-500 hover:text-gray-300'
              }`}>
              {m === 'http' ? 'HTTP (batch)' : 'WebSocket (stream)'}
            </button>
          ))}
        </div>

        <div>
          <label className="text-xs text-gray-500 block mb-2">Presets</label>
          <div className="flex flex-wrap gap-2">
            {PRESETS.map(p => (
              <button key={p} onClick={() => setQuery(p)}
                className="text-xs px-3 py-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-700 rounded-lg text-gray-400 hover:text-gray-200 transition-colors">
                {p.length > 40 ? p.slice(0, 40) + '…' : p}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="text-xs text-gray-500 block mb-2">Action to Evaluate</label>
          <div className="flex gap-3">
            <textarea
              value={query}
              onChange={e => setQuery(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) run() }}
              placeholder="Describe the action you want to evaluate ethically…"
              rows={3}
              className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-sm text-gray-200 placeholder-gray-600 resize-none focus:outline-none focus:border-cyan-500/50"
            />
          </div>
        </div>

        <button onClick={run} disabled={loading || !query.trim()}
          className="flex items-center gap-2 px-5 py-2.5 bg-cyan-600 hover:bg-cyan-500 disabled:bg-gray-700 disabled:text-gray-500 text-white text-sm font-medium rounded-lg transition-colors">
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
          {loading ? 'Evaluating across 10,000 futures…' : 'Run Evaluation'}
        </button>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-sm text-red-400">{error}</div>
      )}

      {Object.keys(streamAgents).length > 0 && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h2 className="text-sm font-semibold text-gray-300 mb-4 flex items-center gap-2">
            <Zap className="w-4 h-4 text-cyan-400" /> Agent Results
            {loading && <Loader2 className="w-3 h-3 animate-spin text-gray-500 ml-1" />}
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {Object.entries(AGENT_META).map(([aid, { icon: Icon, color }]) => {
              const data = streamAgents[aid]
              if (!data) return (
                <div key={aid} className="bg-gray-800/40 border border-gray-700/50 rounded-lg p-4 animate-pulse">
                  <div className="h-4 w-32 bg-gray-700 rounded" />
                </div>
              )
              const verdict = data.result
                ? String(data.result.verdict ?? data.result.status ?? data.result.final_verdict ?? data.result.risk_level ?? '')
                : ''
              const reasoning = resultText(data.result, 'reasoning')
              const rationale = resultText(data.result, 'rationale')
              const mitigation = resultText(data.result, 'mitigation')
              const recommendation = resultText(data.result, 'recommendation')
              return (
                <div key={aid} className="bg-gray-800/60 border border-gray-700 rounded-lg p-4 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className={`flex items-center gap-2 text-sm font-medium ${color}`}>
                      <Icon className="w-3.5 h-3.5" />
                      {data.result ? Object.keys(AGENT_META).map(() => '').join('') || aid.replace(/_/g, ' ') : aid}
                    </span>
                    <span className="text-xs text-gray-600">{data.latency_ms?.toFixed(0)}ms</span>
                  </div>
                  {verdict && <VerdictBadge verdict={verdict.toUpperCase()} />}
                  {data.error && <p className="text-xs text-red-400">{data.error}</p>}
                  {reasoning && <p className="text-xs text-gray-400 leading-relaxed">{reasoning}</p>}
                  {rationale && <p className="text-xs text-gray-400 leading-relaxed">{rationale}</p>}
                  {mitigation && <p className="text-xs text-gray-400 leading-relaxed">{mitigation}</p>}
                  {recommendation && <p className="text-xs text-gray-400 leading-relaxed">{recommendation}</p>}
                  {data.result?.protection_score !== undefined && (
                    <ScoreBar score={Number(data.result.protection_score)} />
                  )}
                  {data.result?.composite !== undefined && (
                    <ScoreBar score={Number(data.result.composite)} />
                  )}
                  {data.result?.confidence !== undefined && (
                    <ScoreBar score={Number(data.result.confidence)} />
                  )}
                </div>
              )
            })}
          </div>
        </div>
      )}

      {finalResult && (
        <div className={`border rounded-xl p-6 space-y-4 ${verdictColor}`}>
          <div className="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h2 className="text-sm font-semibold text-gray-300 mb-1">Final Constitutional Verdict</h2>
              <VerdictBadge verdict={finalResult.composite_verdict} />
            </div>
            <div className="text-right">
              <p className="text-xs text-gray-500">ID: <span className="font-mono text-gray-400">{finalResult.evaluation_id}</span></p>
              <p className="text-xs text-gray-500">{finalResult.latency_ms.toFixed(0)}ms total</p>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: 'Compliance Score', value: `${(finalResult.composite_score * 100).toFixed(1)}%` },
              { label: 'Risk Level', value: finalResult.risk_level },
              { label: 'Multiverse Compliance', value: `${finalResult.multiverse_compliance.toFixed(1)}%` },
              { label: 'Futures Simulated', value: finalResult.futures_simulated.toLocaleString() },
            ].map(({ label, value }) => (
              <div key={label} className="bg-gray-900/60 rounded-lg p-3">
                <p className="text-xs text-gray-500 mb-1">{label}</p>
                <p className="text-sm font-semibold text-gray-200">{value}</p>
              </div>
            ))}
          </div>

          {finalResult.axioms_violated.length > 0 && (
            <div className="bg-red-500/10 border border-red-500/20 rounded-lg px-4 py-3">
              <p className="text-xs text-red-400 font-medium mb-1">Axioms Violated</p>
              <p className="text-xs text-red-300">{finalResult.axioms_violated.join(', ')}</p>
            </div>
          )}

          <div className="bg-gray-900/60 rounded-lg px-4 py-3">
            <p className="text-xs text-gray-500 mb-1 font-medium">Superintelligence Reflection</p>
            <p className="text-xs text-gray-300 leading-relaxed">{finalResult.superintelligence_reflection}</p>
          </div>
        </div>
      )}
    </div>
  )
}
