import { useState, useEffect } from 'react'
import { validateEmail } from '../utils/validation'
import LoadingSpinner from './LoadingSpinner'

const SigninForm = ({ onSuccess, onSwitchToSignup, prefillEmail = '' }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)

  // Update email when prefillEmail changes
  useEffect(() => {
    if (prefillEmail) {
      setFormData(prev => ({
        ...prev,
        email: prefillEmail
      }))
    }
  }, [prefillEmail])

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

    try {
      const result = await onSuccess(formData)
      
      if (!result.success) {
        setErrors({ general: result.error })
      }
    } catch (error) {
      setErrors({ general: 'An unexpected error occurred' })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="bg-white/95 backdrop-blur-xl border border-white/30 rounded-2xl p-6 shadow-2xl relative overflow-hidden">
      {/* Decorative Elements */}
      <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-br from-purple-500/10 to-pink-500/10 rounded-full blur-2xl transform translate-x-12 -translate-y-12"></div>
      <div className="absolute bottom-0 left-0 w-20 h-20 bg-gradient-to-tr from-pink-500/10 to-purple-500/10 rounded-full blur-2xl transform -translate-x-10 translate-y-10"></div>
      
      <div className="relative z-10">
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-slate-800 mb-1">Welcome Back</h2>
          <p className="text-slate-600 text-sm">Sign in to continue your professional development</p>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* General Error */}
          {errors.general && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-3 py-2 rounded-lg text-sm">
              <div className="flex items-center">
                <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                {errors.general}
              </div>
            </div>
          )}

          {/* Email */}
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">
              Email Address
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg className="h-4 w-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                </svg>
              </div>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="w-full pl-10 pr-3 py-3 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
                placeholder="your.email@company.com"
                required
              />
            </div>
            <div className={`error-message text-red-600 text-sm mt-1 transition-all duration-300 ${errors.email ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'}`}>
              {errors.email}
            </div>
          </div>

          {/* Password */}
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">
              Password
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg className="h-4 w-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="w-full pl-10 pr-3 py-3 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
                placeholder={prefillEmail ? "Enter your password" : "Your secure password"}
                required
              />
            </div>
            <div className={`error-message text-red-600 text-sm mt-1 transition-all duration-300 ${errors.password ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'}`}>
              {errors.password}
            </div>
          </div>

          {/* Forgot Password Link */}
          <div className="text-right">
            <button
              type="button"
              className="text-purple-600 hover:text-purple-700 text-sm font-medium transition-colors duration-300"
            >
              Forgot your password?
            </button>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold py-3 px-4 rounded-lg transition-all duration-300 hover:scale-105 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 relative overflow-hidden"
          >
            {isLoading ? (
              <div className="flex items-center justify-center">
                <LoadingSpinner />
                <span className="ml-2">Signing In...</span>
              </div>
            ) : (
              <div className="flex items-center justify-center">
                <span>Access Your Dashboard</span>
                <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </div>
            )}
          </button>

          {/* Divider */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-200"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-3 bg-white text-slate-500">New to SpeechAnalyzer Pro?</span>
            </div>
          </div>

          {/* Switch to Signup */}
          <div className="text-center">
            <button
              type="button"
              onClick={onSwitchToSignup}
              className="w-full bg-slate-100 border border-slate-200 text-slate-700 font-semibold py-3 px-4 rounded-lg hover:bg-slate-200 transition-all duration-300 hover:scale-105"
            >
              Create New Account
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default SigninForm