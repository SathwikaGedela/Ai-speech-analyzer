import { useState } from 'react'
import { validateEmail, validatePhone, validatePassword, validateName } from '../utils/validation'
import LoadingSpinner from './LoadingSpinner'

const SignupForm = ({ onSuccess, onSwitchToSignin }) => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: ''
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

    if (!validateName(formData.firstName)) {
      newErrors.firstName = 'First name must be at least 2 characters'
    }

    if (!validateName(formData.lastName)) {
      newErrors.lastName = 'Last name must be at least 2 characters'
    }

    if (!validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email address'
    }

    if (!validatePhone(formData.phone)) {
      newErrors.phone = 'Please enter a valid phone number'
    }

    if (!validatePassword(formData.password)) {
      newErrors.password = 'Password must be at least 6 characters'
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match'
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
      
      if (result.success) {
        // Reset form
        setFormData({
          firstName: '',
          lastName: '',
          email: '',
          phone: '',
          password: '',
          confirmPassword: ''
        })
      } else {
        // Handle specific errors
        if (result.error.includes('email')) {
          setErrors({ email: result.error })
        } else {
          setErrors({ general: result.error })
        }
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
        <div className="text-center mb-4">
          <h2 className="text-2xl font-bold text-slate-800 mb-1">Create Account</h2>
          <p className="text-slate-600 text-sm">Start your professional development journey</p>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-3">
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

          {/* Name Row */}
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1">
                First Name
              </label>
              <input
                type="text"
                name="firstName"
                value={formData.firstName}
                onChange={handleChange}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
                placeholder="John"
                required
              />
              <div className={`error-message text-red-600 text-xs mt-1 transition-all duration-300 ${errors.firstName ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'}`}>
                {errors.firstName}
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1">
                Last Name
              </label>
              <input
                type="text"
                name="lastName"
                value={formData.lastName}
                onChange={handleChange}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
                placeholder="Doe"
                required
              />
              <div className={`error-message text-red-600 text-xs mt-1 transition-all duration-300 ${errors.lastName ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'}`}>
                {errors.lastName}
              </div>
            </div>
          </div>

          {/* Email */}
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">
              Email Address
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
              placeholder="your.email@company.com"
              required
            />
            <div className={`error-message text-red-600 text-xs mt-1 transition-all duration-300 ${errors.email ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'}`}>
              {errors.email}
            </div>
          </div>

          {/* Phone */}
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">
              Phone Number
            </label>
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
              placeholder="+1 (555) 123-4567"
              required
            />
            <div className={`error-message text-red-600 text-xs mt-1 transition-all duration-300 ${errors.phone ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'}`}>
              {errors.phone}
            </div>
          </div>

          {/* Password Row */}
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1">
                Password
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
                placeholder="Min 6 chars"
                required
              />
              <div className={`error-message text-red-600 text-xs mt-1 transition-all duration-300 ${errors.password ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'}`}>
                {errors.password}
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1">
                Confirm
              </label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
                placeholder="Confirm"
                required
              />
              <div className={`error-message text-red-600 text-xs mt-1 transition-all duration-300 ${errors.confirmPassword ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'}`}>
                {errors.confirmPassword}
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold py-3 px-4 rounded-lg transition-all duration-300 hover:scale-105 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 relative overflow-hidden mt-4"
          >
            {isLoading ? (
              <div className="flex items-center justify-center">
                <LoadingSpinner />
                <span className="ml-2">Creating Account...</span>
              </div>
            ) : (
              <div className="flex items-center justify-center">
                <span>Create Account</span>
                <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </div>
            )}
          </button>

          {/* Divider */}
          <div className="relative my-4">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-200"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-3 bg-white text-slate-500">Already have an account?</span>
            </div>
          </div>

          {/* Switch to Signin */}
          <div className="text-center">
            <button
              type="button"
              onClick={onSwitchToSignin}
              className="w-full bg-slate-100 border border-slate-200 text-slate-700 font-semibold py-3 px-4 rounded-lg hover:bg-slate-200 transition-all duration-300 hover:scale-105"
            >
              Sign In to Your Account
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default SignupForm