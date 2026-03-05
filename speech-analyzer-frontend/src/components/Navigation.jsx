import { useState, useRef, useEffect } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { useAuth } from '../contexts/AuthContext'

const Navigation = () => {
  const { user, logout } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()
  const [showProfileDropdown, setShowProfileDropdown] = useState(false)
  const dropdownRef = useRef(null)

  const handleLogout = async () => {
    await logout()
    // Redirect to landing page after logout
    navigate('/')
  }

  const isActive = (path) => {
    return location.pathname === path
  }

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '🏠' },
    { path: '/analysis', label: 'Analysis', icon: '🎤' },
    { path: '/interview', label: 'Interview', icon: '💼' },
    { path: '/history', label: 'History', icon: '📊' }
  ]

  // Close dropdown when clicking outside
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
    <motion.nav 
      className="glass-card sticky top-0 z-50"
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-8">
            <Link to="/dashboard" className="flex items-center space-x-2 group">
              <motion.span
                animate={{ rotate: [0, 10, -10, 0] }}
                transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                className="text-2xl"
              >
                🎤
              </motion.span>
              <span className="text-2xl font-bold text-gray-800 group-hover:text-purple-600 transition-colors duration-300">
                SpeechAnalyzer Pro
              </span>
            </Link>
            
            <div className="hidden md:flex space-x-1 relative">
              {navItems.map((item, index) => (
                <motion.div
                  key={item.path}
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 + 0.3 }}
                  className="relative"
                >
                  <Link 
                    to={item.path} 
                    className={`
                      flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium 
                      transition-all duration-300 relative overflow-hidden group
                      ${isActive(item.path) 
                        ? 'bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 shadow-md' 
                        : 'text-gray-700 hover:text-purple-600 hover:bg-purple-50'
                      }
                    `}
                  >
                    {/* Background animation */}
                    {!isActive(item.path) && (
                      <motion.div
                        className="absolute inset-0 bg-gradient-to-r from-purple-100 to-pink-100 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                        layoutId="navHover"
                      />
                    )}
                    
                    {/* Active indicator */}
                    {isActive(item.path) && (
                      <motion.div
                        className="absolute inset-0 bg-gradient-to-r from-purple-100 to-pink-100 rounded-xl"
                        layoutId="activeNav"
                        transition={{ type: "spring", stiffness: 300, damping: 30 }}
                      />
                    )}
                    
                    <span className="relative z-10 text-lg">{item.icon}</span>
                    <span className="relative z-10">{item.label}</span>
                    
                    {/* Active dot */}
                    {isActive(item.path) && (
                      <motion.div
                        className="absolute -bottom-1 left-1/2 w-1 h-1 bg-purple-500 rounded-full"
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        style={{ x: '-50%' }}
                      />
                    )}
                  </Link>
                </motion.div>
              ))}
            </div>
          </div>
          
          <motion.div 
            className="flex items-center space-x-4"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            {/* Profile Dropdown */}
            <div className="relative" ref={dropdownRef}>
              <motion.button
                onClick={toggleProfileDropdown}
                className="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 transition-colors group"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <motion.div 
                  className="w-8 h-8 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold text-sm"
                  animate={{ 
                    boxShadow: showProfileDropdown 
                      ? '0 0 20px rgba(168, 85, 247, 0.4)' 
                      : '0 0 0px rgba(168, 85, 247, 0)'
                  }}
                  transition={{ duration: 0.3 }}
                >
                  {user?.first_name?.charAt(0)?.toUpperCase()}
                </motion.div>
                <span className="hidden sm:block text-gray-700 text-sm font-medium group-hover:text-purple-600 transition-colors">
                  {user?.first_name}
                </span>
                <motion.svg 
                  className="w-4 h-4 text-gray-500 group-hover:text-purple-600 transition-colors" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                  animate={{ rotate: showProfileDropdown ? 180 : 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </motion.svg>
              </motion.button>

              {/* Profile Dropdown Menu */}
              <AnimatePresence>
                {showProfileDropdown && (
                  <motion.div
                    className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50 overflow-hidden"
                    initial={{ opacity: 0, scale: 0.95, y: -10 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.95, y: -10 }}
                    transition={{ duration: 0.2, ease: "easeOut" }}
                  >
                    {/* Profile Header */}
                    <motion.div 
                      className="px-4 py-3 border-b border-gray-100 bg-gradient-to-r from-purple-50 to-pink-50"
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.1 }}
                    >
                      <div className="flex items-center space-x-3">
                        <motion.div 
                          className="w-12 h-12 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg"
                          whileHover={{ scale: 1.1, rotate: 5 }}
                        >
                          {user?.first_name?.charAt(0)?.toUpperCase()}
                        </motion.div>
                        <div>
                          <div className="font-semibold text-gray-800">{user?.first_name} {user?.last_name}</div>
                          <div className="text-sm text-gray-500">{user?.email}</div>
                        </div>
                      </div>
                    </motion.div>

                    {/* Account Information */}
                    <motion.div 
                      className="px-4 py-3"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.2 }}
                    >
                      <h3 className="text-sm font-semibold text-gray-700 mb-3">Account Information</h3>
                      <div className="space-y-2">
                        <motion.div 
                          className="flex justify-between items-center py-2 hover:bg-gray-50 rounded-lg px-2 transition-colors"
                          whileHover={{ x: 2 }}
                        >
                          <span className="text-sm text-gray-600">Phone:</span>
                          <span className="text-sm font-medium text-gray-800">{user?.phone}</span>
                        </motion.div>
                        <motion.div 
                          className="flex justify-between items-center py-2 hover:bg-gray-50 rounded-lg px-2 transition-colors"
                          whileHover={{ x: 2 }}
                        >
                          <span className="text-sm text-gray-600">Member Since:</span>
                          <span className="text-sm font-medium text-gray-800">{user?.created_at}</span>
                        </motion.div>
                        <motion.div 
                          className="flex justify-between items-center py-2 hover:bg-gray-50 rounded-lg px-2 transition-colors"
                          whileHover={{ x: 2 }}
                        >
                          <span className="text-sm text-gray-600">Status:</span>
                          <span className="text-sm font-medium text-green-600 flex items-center gap-1">
                            <motion.div
                              className="w-2 h-2 bg-green-500 rounded-full"
                              animate={{ scale: [1, 1.2, 1] }}
                              transition={{ duration: 2, repeat: Infinity }}
                            />
                            Active
                          </span>
                        </motion.div>
                      </div>
                    </motion.div>

                    {/* Actions */}
                    <motion.div 
                      className="border-t border-gray-100 px-4 py-2"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.3 }}
                    >
                      <motion.button
                        onClick={handleLogout}
                        className="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors flex items-center space-x-2 group"
                        whileHover={{ x: 2 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        <motion.svg 
                          className="w-4 h-4 group-hover:rotate-12 transition-transform" 
                          fill="none" 
                          stroke="currentColor" 
                          viewBox="0 0 24 24"
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </motion.svg>
                        <span>Sign Out</span>
                      </motion.button>
                    </motion.div>

                    {/* Decorative gradient */}
                    <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-purple-500 via-pink-500 to-purple-500" />
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        </div>
      </div>
    </motion.nav>
  )
}

export default Navigation