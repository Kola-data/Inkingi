import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/auth-store'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { AuthLayout } from '@/components/layout/auth-layout'

// Pages
import LoginPage from '@/pages/auth/login'
import RegisterPage from '@/pages/auth/register'
import DashboardPage from '@/pages/dashboard'
import ClassesPage from '@/pages/classes'
import StudentsPage from '@/pages/students'
import TeachersPage from '@/pages/teachers'
import CoursesPage from '@/pages/courses'
import TimetablePage from '@/pages/timetable'
import FeesPage from '@/pages/fees'
import InventoryPage from '@/pages/inventory'
import CommunicationPage from '@/pages/communication'
import SettingsPage from '@/pages/settings'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />
}

function App() {
  return (
    <Routes>
      {/* Auth routes */}
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Route>

      {/* Protected routes */}
      <Route
        element={
          <PrivateRoute>
            <DashboardLayout />
          </PrivateRoute>
        }
      >
        <Route path="/" element={<Navigate to="/dashboard" />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/classes" element={<ClassesPage />} />
        <Route path="/students" element={<StudentsPage />} />
        <Route path="/teachers" element={<TeachersPage />} />
        <Route path="/courses" element={<CoursesPage />} />
        <Route path="/timetable" element={<TimetablePage />} />
        <Route path="/fees" element={<FeesPage />} />
        <Route path="/inventory" element={<InventoryPage />} />
        <Route path="/communication" element={<CommunicationPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Route>

      {/* 404 */}
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  )
}

export default App