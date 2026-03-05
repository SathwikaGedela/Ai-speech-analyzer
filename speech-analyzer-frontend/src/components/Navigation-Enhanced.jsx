import { useState, useRef, useEffect } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const Navigation = () => {
  const { user, logout } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()
  const [showProfileDropdown, setShowProfileDropdown] = useState(false)
  const dropdownRef = useRef(null)

  const handleLogout = async () => {
    await logout()
    navigate('/')
  }

  const isActive = (path) => {
    return location.pathname === path
  }

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowProfileDropdown(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [])

  const toggleProfileDropdown = () => {
    setShowProfileDropdown(!showProfileDropdown)
  }

  return (
    <nav className="bg-white/95 backdrop-blur-xl sticky top-0 z-50 border-b border-slate-200/60 shadow-sm">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-10">
        <div className="flex justify-between items-center h-20">
          <div className="flex items-center space-x-10">
            <Link to="/dashboard" className="flex items-center space-x-3 group">
              <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
                <span className="text-white text-xl">🎤</span>
              </div>
              <span className="text-2xl font-bold text-slate-900 group-hover:text-indigo-600 transition-colors">
                SpeechAnalyzer Pro
              </span>
            </Link>
            
            <div className="hidden md:flex items-center space-x-2">
              <Link 
                to="/dashboard" 
                className={`px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 hover:scale-105 active:scale-95 focus:ring-4 focus:ring-slate-200 focus:outline-none ${
                  isActive('/dashboard') 
                    ? 'bg-indigo-100 text-indigo-700 shadow-sm' 
                    : 'text-slate-700 hover:bg-slate-100 hover:text-slate-900'
                }`}
              >
                Dashboard
              </Link>
              <Link 
                to="/analysis" 
                className={`px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 hover:scale-105 active:scale-95 focus:ring-4 focus:ring-slate-200 focus:outline-none ${
                  isActive('/analysis') 
                    ? 'bg-indigo-100 text-indigo-700 shadow-sm' 
                    : 'text-slate-700 hover:bg-slate-100 hover:text-slate-900'
                }`}
              >
                Analysis
              </Link>
              <Link 
                to="/interview" 
                className={`px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 hover:scale-105 active:scale-95 focus:ring-4 focus:ring-slate-200 focus:outline-none ${
                  isActive('/interview') 
                    ? 'bg-indigo-100 text-indigo-700 shadow-sm' 
                    : 'text-slate-700 hover:bg-slate-100 hover:text-slate-900'
                }`}
              >
                Interview
              </Link>
              <Link 
                to="/history" 
                className={`px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 hover:scale-105 active:scale-95 focus:ring-4 focus:ring-slate-200 focus:outline-none ${
                  isActive('/history') 
                    ? 'bg-indigo-100 text-indigo-700 shadow-sm' 
                    : 'text-slate-700 hover:bg-slate-100 hover:text-slate-900'
                }`}
              >
                History
              </Link>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            {/* Quick Action Button */}
            <Link
              to="/analysis"
              className="hidden sm:inline-flex items-center px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 focus:ring-4 focus:ring-indigo-200 focus:outline-none"
            >
              <span className="mr-2">🎤</span>
              Quick Analysis
            </Link>

            {/* Profile Dropdown */}
            <div className="relative" ref={dropdownRef}>
              <button
                onClick={toggleProfileDropdown}
                className="flex items-center space-x-3 p-2 rounded-xl hover:bg-slate-100 transition-all duration-200 focus:ring-4 focus:ring-slate-200 focus:outline-none group"
              >
                <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold text-sm shadow-md group-hover:scale-110 transition-transform">
                  {user?.first_name?.charAt(0)?.toUpperCase()}
                </div>
                <div className="hidden sm:block text-left">
                  <div className="text-sm font-semibold text-slate-900 group-hover:text-indigo-600 transition-colors">
                    {user?.first_name}
                  </div>
                  <div className="text-xs text-slate-500">
                    {user?.email}
                  </div>
                </div>
                <svg 
                  className={`w-4 h-4 text-slate-500 transition-transform duration-200 ${showProfileDropdown ? 'rotate-180' : ''}`} 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {/* Enhanced Profile Dropdown Menu */}
              {showProfileDropdown && (
                <div className="absolute right-0 mt-3 w-80 bg-white rounded-2xl shadow-xl border border-slate-200 py-2 z-50 animate-scale-in">
                  {/* Profile Header */}
                  <div className="px-6 py-4 border-b border-slate-100">
                    <div className="flex items-center space-x-4">
                      <div className="w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center text-white font-bold text-lg shadow-lg">
                        {user?.first_name?.charAt(0)?.toUpperCase()}
                      </div>
                      <div className="flex-1">
                        <div className="font-bold text-slate-900 text-lg">{user?.first_name} {user?.last_name}</div>
                        <div className="text-sm text-slate-500">{user?.email}</div>
                        <div className="inline-flex items-center px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium mt-1">
                          <div className="w-2 h-2 bg-green-500 rounded-full mr-1"></div>
                          Active
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Account Information */}
                  <div className="px-6 py-4">
                    <h3 className="text-sm font-bold text-slate-700 mb-4 uppercase tracking-wide">Account Information</h3>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between py-2 px-3 bg-slate-50 rounded-xl">
                        <div className="flex items-center space-x-3">
                          <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                            <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                            </svg>
                          </div>
                          <span className="text-sm text-slate-600">Phone</span>
                        </div>
                        <span className="text-sm font-semibold text-slate-900">{user?.phone}</span>
                      </div>
                      
                      <div className="flex items-center justify-between py-2 px-3 bg-slate-50 rounded-xl">
                        <div className="flex items-center space-x-3">
                          <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                            <svg className="w-4 h-4 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3a4 4 0 118 0v4m-4 6v6m-4-6h8m-8 0H4a2 2 0 00-2 2v6a2 2 0 002 2h16a2 2 0 002-2v-6a2 2 0 00-2-2h-4" />
                            </svg>
                          </div>
                          <span className="text-sm text-slate-600">Member Since</span>
                        </div>
                        <span className="text-sm font-semibold text-slate-900">{user?.created_at}</span>
                      </div>
                      
                      <div className="flex items-center justify-between py-2 px-3 bg-slate-50 rounded-xl">
                        <div className="flex items-center space-x-3">
                          <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                            <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                          </div>
                          <span className="text-sm text-slate-600">Status</span>
                        </div>
                        <span className="text-sm font-semibold text-green-600">Active</span>
                      </div>
                    </div>
                  </div>

                  {/* Quick Actions */}
                  <div className="px-6 py-4 border-t border-slate-100">
                    <h3 className="text-sm font-bold text-slate-700 mb-4 uppercase tracking-wide">Quick Actions</h3>
                    <div className="grid grid-cols-2 gap-3">
                      <Link
                        to="/analysis"
                        onClick={() => setShowProfileDropdown(false)}
                        className="flex items-center justify-center px-3 py-2 bg-indigo-50 text-indigo-700 rounded-xl hover:bg-indigo-100 transition-colors text-sm font-medium"
                      >
                        <span className="mr-2">🎤</span>
                        Analyze
                      </Link>
                      <Link
                        to="/history"
                        onClick={() => setShowProfileDropdown(false)}
                        className="flex items-center justify-center px-3 py-2 bg-green-50 text-green-700 rounded-xl hover:bg-green-100 transition-colors text-sm font-medium"
                      >
                        <span className="mr-2">📊</span>
                        History
                      </Link>
                    </div>
                  </div>

                  {/* Logout */}
                  <div className="border-t border-slate-100 px-6 py-4">
                    <button
                      onClick={handleLogout}
                      className="w-full flex items-center justify-center px-4 py-3 text-red-600 hover:bg-red-50 rounded-xl transition-all duration-200 font-semibold focus:ring-4 focus:ring-red-200 focus:outline-none group"
                    >
                      <svg className="w-5 h-5 mr-3 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      Sign Out
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navigation