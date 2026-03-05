import { motion } from 'framer-motion'
import { useState, useEffect } from 'react'

const MetricCard = ({ 
  title, 
  value, 
  unit = '', 
  icon, 
  color = 'blue', 
  trend = null,
  description = '',
  animated = true,
  delay = 0,
  onClick = null
}) => {
  const [displayValue, setDisplayValue] = useState(animated ? 0 : value)

  const colorClasses = {
    blue: {
      bg: 'bg-blue-50 hover:bg-blue-100',
      text: 'text-blue-600',
      border: 'border-blue-200',
      gradient: 'from-blue-500 to-blue-600'
    },
    green: {
      bg: 'bg-green-50 hover:bg-green-100',
      text: 'text-green-600',
      border: 'border-green-200',
      gradient: 'from-green-500 to-green-600'
    },
    purple: {
      bg: 'bg-purple-50 hover:bg-purple-100',
      text: 'text-purple-600',
      border: 'border-purple-200',
      gradient: 'from-purple-500 to-purple-600'
    },
    yellow: {
      bg: 'bg-yellow-50 hover:bg-yellow-100',
      text: 'text-yellow-600',
      border: 'border-yellow-200',
      gradient: 'from-yellow-500 to-yellow-600'
    },
    red: {
      bg: 'bg-red-50 hover:bg-red-100',
      text: 'text-red-600',
      border: 'border-red-200',
      gradient: 'from-red-500 to-red-600'
    },
    indigo: {
      bg: 'bg-indigo-50 hover:bg-indigo-100',
      text: 'text-indigo-600',
      border: 'border-indigo-200',
      gradient: 'from-indigo-500 to-indigo-600'
    }
  }

  const colors = colorClasses[color] || colorClasses.blue

  // Animate number counting
  useEffect(() => {
    if (!animated) return

    const timer = setTimeout(() => {
      const duration = 1000
      const steps = 30
      const increment = value / steps
      let current = 0
      
      const counter = setInterval(() => {
        current += increment
        if (current >= value) {
          setDisplayValue(value)
          clearInterval(counter)
        } else {
          setDisplayValue(Math.floor(current))
        }
      }, duration / steps)

      return () => clearInterval(counter)
    }, delay)

    return () => clearTimeout(timer)
  }, [value, animated, delay])

  const getTrendIcon = () => {
    if (!trend) return null
    
    switch (trend.direction) {
      case 'up':
        return (
          <motion.div
            animate={{ y: [-2, 2, -2] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
            className="text-green-500"
          >
            📈
          </motion.div>
        )
      case 'down':
        return (
          <motion.div
            animate={{ y: [2, -2, 2] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
            className="text-red-500"
          >
            📉
          </motion.div>
        )
      default:
        return <span className="text-gray-500">➡️</span>
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ 
        duration: 0.6, 
        delay: delay,
        ease: "easeOut" 
      }}
      whileHover={onClick ? { 
        scale: 1.02, 
        y: -4,
        boxShadow: '0 10px 30px rgba(0, 0, 0, 0.1)'
      } : {
        y: -2,
        boxShadow: '0 8px 25px rgba(0, 0, 0, 0.08)'
      }}
      className={`
        p-6 rounded-xl border-2 transition-all duration-300
        ${colors.bg} ${colors.border}
        ${onClick ? 'cursor-pointer' : ''}
        relative overflow-hidden
      `}
      onClick={onClick}
    >
      {/* Background gradient overlay */}
      <div className={`absolute inset-0 bg-gradient-to-br ${colors.gradient} opacity-0 hover:opacity-5 transition-opacity duration-300`} />
      
      <div className="relative z-10">
        {/* Header with icon and trend */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            {icon && (
              <motion.div
                animate={{ 
                  rotate: [0, 10, -10, 0],
                  scale: [1, 1.1, 1]
                }}
                transition={{ 
                  duration: 3, 
                  repeat: Infinity, 
                  ease: "easeInOut" 
                }}
                className="text-2xl"
              >
                {icon}
              </motion.div>
            )}
            <h3 className="text-sm font-medium text-gray-600">{title}</h3>
          </div>
          
          {trend && (
            <div className="flex items-center gap-1">
              {getTrendIcon()}
              <span className={`text-xs font-medium ${
                trend.direction === 'up' ? 'text-green-600' : 
                trend.direction === 'down' ? 'text-red-600' : 'text-gray-600'
              }`}>
                {trend.value}
              </span>
            </div>
          )}
        </div>

        {/* Main value */}
        <div className="mb-2">
          <motion.span
            key={displayValue}
            initial={{ scale: 1.2, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className={`text-3xl font-bold ${colors.text}`}
          >
            {displayValue}
          </motion.span>
          {unit && (
            <span className="text-lg font-medium text-gray-500 ml-1">
              {unit}
            </span>
          )}
        </div>

        {/* Description */}
        {description && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: delay + 0.3 }}
            className="text-xs text-gray-500 leading-relaxed"
          >
            {description}
          </motion.p>
        )}
      </div>

      {/* Hover glow effect */}
      <motion.div
        className={`absolute inset-0 rounded-xl bg-gradient-to-r ${colors.gradient} opacity-0 blur-xl`}
        whileHover={{ opacity: 0.1 }}
        transition={{ duration: 0.3 }}
      />
    </motion.div>
  )
}

export default MetricCard