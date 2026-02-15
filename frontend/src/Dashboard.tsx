import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { Activity, Users, Shield, Zap } from 'lucide-react'

const StatCard = ({ title, value, icon: Icon, color }: any) => (
  <div className="bg-white rounded-xl shadow-lg p-6 border-l-4" style={{ borderColor: color }}>
    <div className="flex items-center justify-between">
      <div>
        <p className="text-gray-500 text-sm mb-1">{title}</p>
        <p className="text-3xl font-bold text-gray-900">{value}</p>
      </div>
      <Icon className="w-12 h-12 opacity-20" style={{ color }} />
    </div>
  </div>
)

export default function Dashboard() {
  const { data: metrics } = useQuery({
    queryKey: ['metrics'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/v1/metrics')
      return res.json()
    },
    refetchInterval: 5000
  })

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-5xl font-bold text-gray-900 mb-2">
            COVENANT.AI <span className="text-blue-600">v5.0</span>
          </h1>
          <p className="text-xl text-gray-600">
            Ultimate Constitutional AI Platform
          </p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard 
            title="Total Evaluations" 
            value={metrics?.total_evaluations?.toLocaleString() || '0'}
            icon={Activity} 
            color="#3b82f6" 
          />
          <StatCard 
            title="Active Agents" 
            value={metrics?.active_agents || '6'}
            icon={Users} 
            color="#10b981" 
          />
          <StatCard 
            title="Approval Rate" 
            value={`${metrics?.approval_rate?.toFixed(1) || '0'}%`}
            icon={Shield} 
            color="#8b5cf6" 
          />
          <StatCard 
            title="Avg Latency" 
            value={`${metrics?.average_latency_ms?.toFixed(1) || '0'}ms`}
            icon={Zap} 
            color="#f59e0b" 
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">System Status</h2>
            <div className="space-y-3">
              <StatusItem label="API Server" status="Operational" />
              <StatusItem label="Swarm Agents" status="Active" />
              <StatusItem label="Database" status="Connected" />
              <StatusItem label="Blockchain" status="Synced" />
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Quick Actions</h2>
            <div className="space-y-3">
              <button className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition">
                Evaluate New Action
              </button>
              <button className="w-full bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 transition">
                View Audit Trail
              </button>
              <button className="w-full bg-purple-600 text-white py-3 px-4 rounded-lg hover:bg-purple-700 transition">
                Generate Report
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

const StatusItem = ({ label, status }: { label: string, status: string }) => (
  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
    <span className="font-medium text-gray-700">{label}</span>
    <span className="flex items-center">
      <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
      <span className="text-green-700 font-medium">{status}</span>
    </span>
  </div>
)