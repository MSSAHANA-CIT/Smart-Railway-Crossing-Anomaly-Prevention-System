import { Routes, Route } from 'react-router-dom'
import { DashboardPage } from '../pages/DashboardPage'
import { PlaceholderPage } from '../pages/PlaceholderPage'

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/monitoring" element={<PlaceholderPage titleKey="nav.liveMonitoring" />} />
      <Route path="/risk" element={<PlaceholderPage titleKey="nav.riskLevel" />} />
      <Route path="/sensors" element={<PlaceholderPage titleKey="nav.sensorStatus" />} />
      <Route path="/alerts" element={<PlaceholderPage titleKey="nav.alerts" />} />
      <Route path="/reports" element={<PlaceholderPage titleKey="nav.reports" />} />
      <Route path="/settings" element={<PlaceholderPage titleKey="nav.settings" />} />
    </Routes>
  )
}
