import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './stores/authStore'
import { useEffect } from 'react'
import Layout from './components/Layout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Schools from './pages/Schools'
import Users from './pages/Users'
import Students from './pages/Students'
import Staff from './pages/Staff'
import Classes from './pages/Classes'
import Courses from './pages/Courses'
import Timetable from './pages/Timetable'
import Marks from './pages/Marks'
import Fees from './pages/Fees'
import Inventory from './pages/Inventory'
import Communication from './pages/Communication'
import AI from './pages/AI'

function App() {
  const { user, checkAuth } = useAuthStore()

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  if (!user) {
    return <Login />
  }

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/schools" element={<Schools />} />
        <Route path="/users" element={<Users />} />
        <Route path="/students" element={<Students />} />
        <Route path="/staff" element={<Staff />} />
        <Route path="/classes" element={<Classes />} />
        <Route path="/courses" element={<Courses />} />
        <Route path="/timetable" element={<Timetable />} />
        <Route path="/marks" element={<Marks />} />
        <Route path="/fees" element={<Fees />} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/communication" element={<Communication />} />
        <Route path="/ai" element={<AI />} />
      </Routes>
    </Layout>
  )
}

export default App