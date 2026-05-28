import { BarChart3, Activity } from 'lucide-react'
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer, Tooltip } from 'recharts'

const AXIOM_SCORES = [
  { subject: 'Observer Rights', score: 97 },
  { subject: 'Reversibility', score: 95 },
  { subject: 'Transparency', score: 98 },
  { subject: 'Non-Domination', score: 96 },
  { subject: 'Truth Preservation', score: 99 },
]

const VERDICTS = [
  { label: 'EXECUTE', value: 72, color: 'bg-green-500' },
  { label: 'REVIEW', value: 21, color: 'bg-yellow-500' },
  { label: 'BLOCK', value: 7, color: 'bg-red-500' },
]

const RISK_BREAKDOWN = [
  { level: 'LOW', pct: 68, color: 'bg-green-500/70' },
  { level: 'MEDIUM', pct: 24, color: 'bg-yellow-500/70' },
  { level: 'HIGH', pct: 6, color: 'bg-orange-500/70' },
  { level: 'CRITICAL', pct: 2, color: 'bg-red-500/70' },
]

const AGENT_PERF = [
  { name: 'Observer Protector', avg_ms: 820, score: 97, color: 'text-blue-400' },
  { name: 'Quantum Risk Matrix', avg_ms: 910, score: 94, color: 'text-yellow-400' },
  { name: 'Constitutional Engine', avg_ms: 870, score: 97, color: 'text-green-400' },
  { name: 'Strategic Nexus', avg_ms: 760, score: 96, color: 'text-purple-400' },
]

export default function Analytics() {
  return (
    <div className="p-8 space-y-8 max-w-5xl">
      <div>
        <h1 className="text-2xl font-bold text-white">Analytics</h1>
        <p className="text-gray-400 text-sm mt-1">Performance metrics and constitutional compliance analytics — sample data</p>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {[
          { label: 'Total Evaluations', value: '1,500,000', color: 'text-cyan-400' },
          { label: 'Avg Compliance Score', value: '97.1%', color: 'text-green-400' },
          { label: 'Avg Latency', value: '840ms', color: 'text-yellow-400' },
          { label: 'Futures Simulated', value: '15B+', color: 'text-purple-400' },
        ].map(({ label, value, color }) => (
          <div key={label} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <p className="text-xs text-gray-500 mb-2">{label}</p>
            <p className={`text-xl font-bold ${color}`}>{value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h2 className="text-sm font-semibold text-gray-300 mb-4 flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-cyan-400" /> Verdict Distribution
          </h2>
          <div className="space-y-3">
            {VERDICTS.map(({ label, value, color }) => (
              <div key={label} className="space-y-1">
                <div className="flex justify-between text-xs text-gray-400">
                  <span className="font-mono">{label}</span>
                  <span>{value}%</span>
                </div>
                <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                  <div className={`h-full ${color} rounded-full`} style={{ width: `${value}%` }} />
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6">
            <h3 className="text-xs text-gray-500 mb-3 uppercase tracking-wider">Risk Level Breakdown</h3>
            <div className="space-y-2">
              {RISK_BREAKDOWN.map(({ level, pct, color }) => (
                <div key={level} className="flex items-center gap-3">
                  <span className="text-xs font-mono text-gray-400 w-16">{level}</span>
                  <div className="flex-1 h-1.5 bg-gray-800 rounded-full overflow-hidden">
                    <div className={`h-full ${color} rounded-full`} style={{ width: `${pct}%` }} />
                  </div>
                  <span className="text-xs text-gray-500 w-8 text-right">{pct}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h2 className="text-sm font-semibold text-gray-300 mb-2 flex items-center gap-2">
            <Activity className="w-4 h-4 text-green-400" /> Axiom Compliance Radar
          </h2>
          <div className="h-52">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={AXIOM_SCORES}>
                <PolarGrid stroke="#374151" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#6b7280', fontSize: 10 }} />
                <Radar name="Score" dataKey="score" stroke="#06b6d4" fill="#06b6d4" fillOpacity={0.15} />
                <Tooltip contentStyle={{ background: '#111827', border: '1px solid #374151', borderRadius: 8, fontSize: 12 }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-sm font-semibold text-gray-300 mb-4 flex items-center gap-2">
          <Activity className="w-4 h-4 text-purple-400" /> Agent Performance
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-xs text-gray-500 border-b border-gray-800">
                <th className="text-left py-2 pr-4">Agent</th>
                <th className="text-right py-2 pr-4">Avg Latency</th>
                <th className="text-right py-2 pr-4">Compliance Score</th>
                <th className="text-left py-2">Performance</th>
              </tr>
            </thead>
            <tbody>
              {AGENT_PERF.map(({ name, avg_ms, score, color }) => (
                <tr key={name} className="border-b border-gray-800/50 last:border-0">
                  <td className={`py-3 pr-4 font-medium ${color}`}>{name}</td>
                  <td className="py-3 pr-4 text-right text-gray-400 font-mono">{avg_ms}ms</td>
                  <td className="py-3 pr-4 text-right text-gray-400 font-mono">{score}%</td>
                  <td className="py-3">
                    <div className="w-24 h-1.5 bg-gray-800 rounded-full overflow-hidden">
                      <div className={`h-full ${color.replace('text-', 'bg-')} rounded-full`} style={{ width: `${score}%` }} />
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
