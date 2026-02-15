'use client'

import { useEffect, useState } from 'react'
import axios from 'axios'

interface Stats {
  total_evaluations: number
  total_violations: number
  agent_count: number
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/statistics`,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }
      )
      setStats(response.data)
    } catch (err) {
      setError('Failed to fetch statistics')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            COVENANT.AI Enterprise v6.0
          </h1>
          <p className="text-xl text-gray-300">
            Constitutional AI Enforcement Platform
          </p>
        </div>

        {/* Stats Grid */}
        {isLoading ? (
          <div className="text-white text-center">Loading...</div>
        ) : error ? (
          <div className="text-red-400 text-center">{error}</div>
        ) : stats ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h3 className="text-gray-300 text-sm font-medium mb-2">
                Total Evaluations
              </h3>
              <p className="text-4xl font-bold text-white">
                {stats.total_evaluations.toLocaleString()}
              </p>
            </div>

            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h3 className="text-gray-300 text-sm font-medium mb-2">
                Violations Detected
              </h3>
              <p className="text-4xl font-bold text-red-400">
                {stats.total_violations.toLocaleString()}
              </p>
            </div>

            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h3 className="text-gray-300 text-sm font-medium mb-2">
                Active Agents
              </h3>
              <p className="text-4xl font-bold text-green-400">
                {stats.agent_count}
              </p>
            </div>
          </div>
        ) : null}

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <FeatureCard
            title="Multi-Agent System"
            description="10+ specialized AI agents working in swarm coordination"
            icon="🤖"
          />
          <FeatureCard
            title="6-Level Verification"
            description="From probabilistic to certified with formal proofs"
            icon="✅"
          />
          <FeatureCard
            title="LLM Integration"
            description="GPT-4, Claude, Llama 2/3, and custom models"
            icon="🧠"
          />
          <FeatureCard
            title="Real-time Analytics"
            description="Live dashboards with Prometheus and Grafana"
            icon="📊"
          />
          <FeatureCard
            title="Blockchain Audit"
            description="Immutable compliance records on-chain"
            icon="⛓️"
          />
          <FeatureCard
            title="Zero-Trust Security"
            description="Military-grade encryption and privacy"
            icon="🔐"
          />
        </div>

        {/* Quick Actions */}
        <div className="mt-12 bg-white/10 backdrop-blur-lg rounded-xl p-8 border border-white/20">
          <h2 className="text-2xl font-bold text-white mb-6">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors">
              New Evaluation
            </button>
            <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors">
              View Reports
            </button>
            <button className="bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors">
              Configure Agents
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

function FeatureCard({ title, description, icon }: { title: string; description: string; icon: string }) {
  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 hover:bg-white/20 transition-all cursor-pointer">
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
      <p className="text-gray-300 text-sm">{description}</p>
    </div>
  )
}