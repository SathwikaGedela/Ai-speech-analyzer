import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const API_BASE_URL = 'http://localhost:5000'

  // Retry mechanism for API calls
  const makeApiCall = async (url, options = {}, retries = 3) => {
    for (let i = 0; i < retries; i++) {
      try {
        const response = await fetch(url, {
          ...options,
          credentials: 'include'
        })
        return response
      } catch (error) {
        console.warn(`API call attempt ${i + 1} failed:`, error)
        if (i === retries - 1) throw error
        // Wait before retry (exponential backoff)
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, i) * 1000))
      }
    }
  }

  // Check if user is authenticated on app load
  useEffect(() => {
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    try {
      const response = await makeApiCall(`${API_BASE_URL}/api/user`)
      
      if (response.ok) {
        const data = await response.json()
        setUser(data.user)
      } else {
        setUser(null)
      }
    } catch (error) {
      console.error('Auth check failed:', error)
      setUser(null)
    } finally {
      setLoading(false)
    }
  }

  const signup = async (userData) => {
    try {
      const response = await makeApiCall(`${API_BASE_URL}/api/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
      })

      const data = await response.json()

      if (response.ok) {
        return { success: true, user: data.user }
      } else {
        return { success: false, error: data.error }
      }
    } catch (error) {
      console.error('Signup error:', error)
      return { success: false, error: 'Network error. Please check if the backend is running and try again.' }
    }
  }

  const signin = async (credentials) => {
    try {
      const response = await makeApiCall(`${API_BASE_URL}/api/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials)
      })

      const data = await response.json()

      if (response.ok) {
        setUser(data.user)
        return { success: true, user: data.user }
      } else {
        return { success: false, error: data.error }
      }
    } catch (error) {
      console.error('Signin error:', error)
      return { success: false, error: 'Network error. Please check if the backend is running and try again.' }
    }
  }

  const logout = async () => {
    try {
      await makeApiCall(`${API_BASE_URL}/api/logout`, {
        method: 'POST'
      })
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      setUser(null)
    }
  }

  const analyzeAudio = async (formData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        body: formData,
        credentials: 'include'
      })

      const data = await response.json()
      return { success: response.ok, data: response.ok ? data : null, error: response.ok ? null : data.error }
    } catch (error) {
      return { success: false, error: 'Network error. Please try again.' }
    }
  }

  const analyzeInterview = async (formData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/interview/analyze`, {
        method: 'POST',
        body: formData,
        credentials: 'include'
      })

      const data = await response.json()
      return { success: response.ok, data: response.ok ? data : null, error: response.ok ? null : data.error }
    } catch (error) {
      return { success: false, error: 'Network error. Please try again.' }
    }
  }

  const getHistory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/history`, {
        credentials: 'include'
      })

      if (response.ok) {
        const data = await response.json()
        return { success: true, data: data }
      } else {
        return { success: false, error: 'Failed to fetch history' }
      }
    } catch (error) {
      return { success: false, error: 'Network error. Please try again.' }
    }
  }

  const value = {
    user,
    loading,
    isAuthenticated: !!user,
    signup,
    signin,
    logout,
    analyzeAudio,
    analyzeInterview,
    getHistory,
    checkAuthStatus
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}