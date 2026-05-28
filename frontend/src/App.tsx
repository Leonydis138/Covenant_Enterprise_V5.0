import { Suspense, lazy } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Layout from './components/Layout'

const Dashboard = lazy(() => import('./pages/Dashboard'))
const Evaluator = lazy(() => import('./pages/Evaluator'))
const Compliance = lazy(() => import('./pages/Compliance'))
const Analytics = lazy(() => import('./pages/Analytics'))
const Settings = lazy(() => import('./pages/Settings'))

const queryClient = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Layout>
          <Suspense fallback={<div className="p-8 text-sm text-gray-400">Loading page...</div>}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/evaluate" element={<Evaluator />} />
              <Route path="/compliance" element={<Compliance />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </Suspense>
        </Layout>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
