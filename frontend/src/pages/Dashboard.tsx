export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">COVENANT.AI Enterprise v3.0</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-2">Total Evaluations</h2>
            <p className="text-3xl font-bold text-blue-600">1,500,000</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-2">Compliance Score</h2>
            <p className="text-3xl font-bold text-green-600">98.5%</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-2">Avg Latency</h2>
            <p className="text-3xl font-bold text-purple-600">12.3ms</p>
          </div>
        </div>
      </div>
    </div>
  )
}
