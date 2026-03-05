import { useState } from 'react'
import { validateEmail, validatePhone, validatePassword, validateName } from '../utils/validation'
import { useAuth } from '../hooks/useAuth'
import LoadingSpinner from './LoadingSpinner'

const SignupForm = ({ onSuccess, onSwitchToSignin }) => {
  const { isEmailTaken } = useAuth()
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
    } else if (isEmailTaken(formData.email)) {
      newErrors.email = 'Email already registered'
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

    // Simulate API call
    setTimeout(() => {
      const userData = {
        firstName: formData.firstName.trim(),
        lastName: formData.lastName.trim(),
        email: formData.email.trim().toLowerCase(),
        phone: formData.phone.trim(),
        password: formData.password
      }

      onSuccess(userData)
      setIsLoading(false)
      
      // Reset form
      setFormData({
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        password: '',
        confirmPassword: ''
      })
    }, 1500)
  }

  return (
    <div className="glass-card p-8 relative overflow-hidden">
      {/* Shimmer effect */}
      <div className="absolute inset-0 -translate-x-full bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
      
      <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">Create Account</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Name Row */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              First Name
            </label>
            <input
              type="text"
              name="firstName"
              value={formData.firstName}
              onChange={handleChange}
              className="input-field"
              required
            />
            <div className={`error-message ${errors.firstName ? 'show' : ''}`}>
              {errors.firstName}
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Last Name
            </label>
            <input
              type="text"
              name="lastName"
              value={formData.lastName}
              onChange={handleChange}
              className="input-field"
              required
            />
            <div className={`error-message ${errors.lastName ? 'show' : ''}`}>
              {errors.lastName}
            </div>
          </div>
        </div>

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

        {/* Phone */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Phone Number
          </label>
          <input
            type="tel"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            className="input-field"
            required
          />
          <div className={`error-message ${errors.phone ? 'show' : ''}`}>
            {errors.phone}
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

        {/* Confirm Password */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Confirm Password
          </label>
          <input
            type="password"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            className="input-field"
            required
          />
          <div className={`error-message ${errors.confirmPassword ? 'show' : ''}`}>
            {errors.confirmPassword}
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
            'Create Account'
          )}
        </button>

        {/* Switch to Signin */}
        <div className="text-center">
          <button
            type="button"
            onClick={onSwitchToSignin}
            className="btn-link"
          >
            Already have an account? Sign In
          </button>
        </div>
      </form>
    </div>
  )
}

export default SignupForm