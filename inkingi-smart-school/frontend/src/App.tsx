import React from 'react';
import { QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'sonner';

import { queryClient } from './lib/queryClient';
import { useAuthStore } from './stores/authStore';

// Components
import { Layout } from './components/Layout';
import { ConfirmModal } from './components/modals/ConfirmModal';
import { ClassModal } from './components/modals/ClassModal';
import { EnrollmentModal } from './components/modals/EnrollmentModal';

// Pages
import { Login } from './pages/Login';
import { Dashboard } from './pages/Dashboard';
import { Classes } from './pages/Classes';
import { Enrollments } from './pages/Enrollments';

// Protected Route Component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
};

// Placeholder components for other routes
const Staff = () => <div className="p-6">Staff Management - Coming Soon</div>;
const Fees = () => <div className="p-6">Fees Management - Coming Soon</div>;
const Inventory = () => <div className="p-6">Inventory Management - Coming Soon</div>;
const Communication = () => <div className="p-6">Communication - Coming Soon</div>;
const AIAssistant = () => <div className="p-6">AI Assistant - Coming Soon</div>;

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="App">
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            
            {/* Protected routes */}
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <Layout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="classes" element={<Classes />} />
              <Route path="enrollments" element={<Enrollments />} />
              <Route path="staff" element={<Staff />} />
              <Route path="fees" element={<Fees />} />
              <Route path="inventory" element={<Inventory />} />
              <Route path="communication" element={<Communication />} />
              <Route path="ai" element={<AIAssistant />} />
            </Route>
            
            {/* Catch all route */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>

          {/* Global Modals */}
          <ConfirmModal />
          <ClassModal />
          <EnrollmentModal />

          {/* Toast notifications */}
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: 'white',
                color: '#1f2937',
                border: '1px solid #e5e7eb',
              },
            }}
          />
        </div>
      </BrowserRouter>
      
      {/* React Query Devtools */}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default App;