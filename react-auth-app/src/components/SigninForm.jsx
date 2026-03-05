import { useState } from 'react'
import { validateEmail } from '../utils/validation'
import { useAuth } from '../hooks/useAuth'
import LoadingSpinner from './LoadingSpinner'

const SigninForm = ({ onSuccess, onSwitchToSignup }) => {
  const { login } = useAuth()
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }))
    }
  }

  const validateForm = () => {
    const newErrors = {}

    if (!validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email address'
    }

    if (!formData.password) {
      newErrors.password = 'Password is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) return

    setIsLoading(true)

    // Simulate API call
    setTimeout(() => {
      const credentials = {
        email: formData.email.trim().toLowerCase(),
        password: formData.password
      }

      const user = login(credentials)
      
      if (user) {
        onSuccess(user)
        setFormData({ email: '', password: '' })
      } else {
        setErrors({ password: 'Invalid email or password' })
      }
      
      setIsLoading(false)
    }, 1500)
  }

  return (
    <div className="glass-card p-8 relative overflow-hidden">
      {/* Shimmer effect */}
      <div className="absolute inset-0 -translate-x-full bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
      
      <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">Welcome Back</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Email */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Email Address
          </label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className="input-field"
            required
          />
          <div className={`error-message ${errors.email ? 'show' : ''}`}>
            {errors.email}
          </div>
        </div>

        {/* Password */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Password
          </label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className="input-field"
            required
          />
          <div className={`error-message ${errors.password ? 'show' : ''}`}>
            {errors.password}
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className="btn-primary relative"
        >
          {isLoading ? (
            <LoadingSpinner />
          ) : (
            'Sign In'
          )}
        </button>

        {/* Switch to Signup */}
        <div className="text-center">
          <button
            type="button"
            onClick={onSwitchToSignup}
            className="btn-link"
          >
            Don't have an account? Sign Up
          </button>
        </div>
      </form>
    </div>
  )
}

export default SigninForm