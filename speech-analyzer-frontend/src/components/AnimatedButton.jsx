import { motion } from 'framer-motion'
import { useState } from 'react'

const AnimatedButton = ({ 
  children, 
  onClick, 
  variant = 'primary', 
  size = 'medium',
  disabled = false,
  loading = false,
  icon = null,
  className = '',
  ...props 
}) => {
  const [isPressed, setIsPressed] = useState(false)

  const variants = {
    primary: 'bg-gradient-to-r from-purple-500 to-pink-600 text-white shadow-lg hover:shadow-xl',
    secondary: 'bg-white text-gray-700 border-2 border-gray-200 hover:border-purple-300 hover:bg-purple-50',
    outline: 'border-2 border-purple-500 text-purple-600 hover:bg-purple-500 hover:text-white',
    ghost: 'text-purple-600 hover:bg-purple-100',
    danger: 'bg-gradient-to-r from-red-500 to-pink-600 text-white shadow-lg hover:shadow-xl'
  }

  const sizes = {
    small: 'px-4 py-2 text-sm',
    medium: 'px-6 py-3 text-base',
    large: 'px-8 py-4 text-lg'
  }

  const baseClasses = `
    inline-flex items-center justify-center gap-2 font-semibold rounded-xl
    transition-all duration-300 ease-out
    focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
    ${variants[variant]}
    ${sizes[size]}
    ${className}
  `

  const handleClick = (e) => {
    if (disabled || loading) return
    setIsPressed(true)
    setTimeout(() => setIsPressed(false), 150)
    onClick?.(e)
  }

  return (
    <motion.button
      className={baseClasses}
      onClick={handleClick}
      disabled={disabled || loading}
      whileHover={!disabled && !loading ? { 
        scale: 1.02, 
        y: -2,
        boxShadow: variant === 'primary' || variant === 'danger' 
          ? '0 20px 40px rgba(168, 85, 247, 0.3)' 
          : '0 8px 25px rgba(0, 0, 0, 0.1)'
      } : {}}
      whileTap={!disabled && !loading ? { 
        scale: 0.98, 
        y: 0 
      } : {}}
      animate={isPressed ? { 
        scale: 0.95,
        transition: { duration: 0.1 }
      } : {}}
      {...props}
    >
      {/* Loading spinner */}
      {loading && (
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="w-4 h-4 border-2 border-current border-t-transparent rounded-full"
        />
      )}
      
      {/* Icon */}
      {icon && !loading && (
        <motion.span
          animate={{ rotate: [0, 10, -10, 0] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        >
          {icon}
        </motion.span>
      )}
      
      {/* Button text */}
      <span>{children}</span>
      
      {/* Ripple effect */}
      {isPressed && (
        <motion.div
          className="absolute inset-0 bg-white rounded-xl opacity-20"
          initial={{ scale: 0, opacity: 0.3 }}
          animate={{ scale: 1.5, opacity: 0 }}
          transition={{ duration: 0.4, ease: "easeOut" }}
        />
      )}
    </motion.button>
  )
}

export default AnimatedButton