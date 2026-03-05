import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import LandingPage from './components/LandingPage'
import AuthPage from './components/AuthPage'
import Dashboard from './components/Dashboard'
import SpeechAnalysis from './components/SpeechAnalysis'
import InterviewMode from './components/InterviewMode'
import HistoryPage from './components/HistoryPage'
import { AuthProvider, useAuth } from './contexts/AuthContext'

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth()
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
        <div className="glass-card p-8">
          <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full mx-auto"></div>
          <p className="text-gray-600 mt-4 text-center">Loading...</p>
        </div>
      </div>
    )
  }
  
  return isAuthenticated ? children : <Navigate to="/auth" replace />
}

// Public Route Component (redirect to dashboard if authenticated)
const PublicRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth()
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
        <div className="glass-card p-8">
          <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full mx-auto"></div>
          <p className="text-gray-600 mt-4 text-center">Loading...</p>
        </div>
      </div>
    )
  }
  
  return isAuthenticated ? <Navigate to="/dashboard" replace /> : children
}

function AppRoutes() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={
          <PublicRoute>
            <LandingPage />
          </PublicRoute>
        } />
        <Route path="/auth" element={
          <PublicRoute>
            <AuthPage />
          </PublicRoute>
        } />
        
        {/* Protected Routes */}
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />
        <Route path="/analysis" element={
          <ProtectedRoute>
            <SpeechAnalysis />
          </ProtectedRoute>
        } />
        <Route path="/interview" element={
          <ProtectedRoute>
            <InterviewMode />
          </ProtectedRoute>
        } />
        <Route path="/history" element={
          <ProtectedRoute>
            <HistoryPage />
          </ProtectedRoute>
        } />
        
        {/* Catch all route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  )
}

export default App