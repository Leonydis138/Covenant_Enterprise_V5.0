import { useEffect, useState } from 'react'
import { Activity, Shield, Brain, GitBranch, Eye, TrendingUp } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { fetchJson } from '@/lib/api'

const AXIOMS = [
  { id: 'observer_rights', label: 'Observer Rights', desc: "No action may remove an observer's ability to observe or act.", roman: 'I' },
  { id: 'reversibility', label: 'Reversibility', desc: 'Prefer reversible actions. Irreversible = max scrutiny.', roman: 'II' },
  { id: 'transparency', label: 'Transparency', desc: 'All reasoning must be fully explainable and auditable.', roman: 'III' },
  { id: 'non_domination', label: 'Non-Domination', desc: 'No entity may gain disproportionate systemic control.', roman: 'IV' },
  { id: 'truth_preservation', label: 'Truth Preservation', desc: 'Never create, amplify, or propagate false information.', roman: 'V' },
]

const AGENTS = [
  { id: 'observer_protector', label: 'Observer Protector', icon: Eye, color: 'text-blue-400' },
  { id: 'quantum_risk', label: 'Quantum Risk Matrix', icon: GitBranch, color: 'text-yellow-400' },
  { id: 'constitutional_engine', label: 'Constitutional Engine', icon: Shield, color: 'text-green-400' },
  { id: 'strategic_nexus', label: 'Strategic Nexus', icon: Brain, color: 'text-purple-400' },
]

const EXAMPLE_QUERIES = [
  '"Deploy untested code to production"',
  '"Share private user data with a third party"',
  '"Revert the database to last good checkpoint"',
]

export default function Dashboard() {
  const [tick, setTick] = useState(0)
  useEffect(() => {
    const t = setInterval(() => setTick(n => n + 1), 1500)
    return () => clearInterval(t)
  }, [])

  const { data: health } = useQuery({
    queryKey: ['health'],
    queryFn: () => fetchJson<Record<string, unknown>>('/health', { method: 'GET' }),
    refetchInterval: 10000,
  })

  const { data: agentInfo } = useQuery({
    queryKey: ['agents'],
    queryFn: () => fetchJson<Record<string, unknown>>('/api/agents', { method: 'GET' }),
    refetchInterval: 30000,
  })

  const isLive = agentInfo?.live === true

  return (
    <div className="p-8 space-y-8">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">COVENANT NEXUS v8.0</h1>
          <p className="text-gray-400 text-sm mt-1">Constitutional Quantum Ethical Superintelligence</p>
        </div>
        <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border ${
          health ? 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10' : 'text-gray-500 border-gray-700 bg-gray-800'
        }`}>
          <span className={`w-1.5 h-1.5 rounded-full ${health ? 'bg-emerald-400 animate-pulse' : 'bg-gray-600'}`} />
          {health ? 'FULLY OPERATIONAL' : 'Connecting...'}
        </div>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'AI Agents', value: '4', icon: Brain, color: 'text-purple-400', sub: isLive ? 'Claude Sonnet 4 LIVE' : 'Demo mode' },
          { label: 'Futures / Query', value: '10,000', icon: GitBranch, color: 'text-cyan-400', sub: 'Monte-Carlo multiverse' },
          { label: 'Constitutional Axioms', value: '5', icon: Shield, color: 'text-green-400', sub: 'Inviolable constraints' },
          { label: 'API Status', value: health ? 'Online' : '...', icon: Activity, color: 'text-emerald-400', sub: 'FastAPI + NEXUS v8' },
        ].map(({ label, value, icon: Icon, color, sub }) => (
          <div key={label} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs text-gray-500 font-medium uppercase tracking-wider">{label}</span>
              <Icon className={`w-4 h-4 ${color}`} />
            </div>
            <p className={`text-2xl font-bold ${color}`}>{value}</p>
            <p className="text-xs text-gray-600 mt-1">{sub}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h2 className="text-sm font-semibold text-gray-300 mb-4 flex items-center gap-2">
            <Brain className="w-4 h-4 text-purple-400" /> Multi-Agent Architecture
          </h2>
          <div className="space-y-3">
            {AGENTS.map(({ id, label, icon: Icon, color }, idx) => (
              <div key={id} className="flex items-center gap-3 bg-gray-800/50 rounded-lg px-4 py-3">
                <Icon className={`w-4 h-4 ${color}`} />
                <span className="text-sm text-gray-300 flex-1">{label}</span>
                <span className="flex items-center gap-1.5">
                  <span className={`w-2 h-2 rounded-full ${color.replace('text-', 'bg-')} ${
                    tick % 4 === idx ? 'opacity-100' : 'opacity-30'
                  } transition-opacity duration-300`} />
                  <span className="text-xs text-gray-500">Active</span>
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h2 className="text-sm font-semibold text-gray-300 mb-4 flex items-center gap-2">
            <Shield className="w-4 h-4 text-green-400" /> Constitutional Axioms
          </h2>
          <div className="space-y-0">
            {AXIOMS.map(a => (
              <div key={a.id} className="flex items-start gap-3 py-2.5 border-b border-gray-800 last:border-0">
                <span className="text-xs font-mono text-cyan-500 mt-0.5 w-5 shrink-0">{a.roman}</span>
                <div>
                  <p className="text-sm font-medium text-gray-200">{a.label}</p>
                  <p className="text-xs text-gray-500 mt-0.5 leading-relaxed">{a.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-sm font-semibold text-gray-300 mb-3 flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-cyan-400" /> Quick Start — Try the Evaluator
        </h2>
        <p className="text-sm text-gray-400 mb-4">
          Go to <span className="text-cyan-400 font-medium">Evaluator</span> to run any action through the 4-agent constitutional pipeline.
          Each evaluation simulates 10,000 alternative futures and returns a structured verdict:{' '}
          <span className="text-green-400 font-mono text-xs">EXECUTE</span>,{' '}
          <span className="text-yellow-400 font-mono text-xs">REVIEW</span>, or{' '}
          <span className="text-red-400 font-mono text-xs">BLOCK</span>.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {EXAMPLE_QUERIES.map(q => (
            <div key={q} className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-xs font-mono text-gray-400 italic">
              {q}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
