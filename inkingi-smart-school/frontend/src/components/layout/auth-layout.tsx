import { Outlet } from 'react-router-dom'
import { GraduationCap } from 'lucide-react'

export function AuthLayout() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-full mb-4">
            <GraduationCap className="w-8 h-8 text-primary-foreground" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Inkingi Smart School
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Comprehensive School Management Platform
          </p>
        </div>
        <div className="bg-white dark:bg-gray-900 rounded-lg shadow-xl p-8">
          <Outlet />
        </div>
      </div>
    </div>
  )
}