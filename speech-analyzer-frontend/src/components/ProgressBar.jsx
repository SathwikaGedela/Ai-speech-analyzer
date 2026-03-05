import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'

const ProgressBar = ({ 
  value, 
  max = 100, 
  color = 'purple', 
  size = 'medium',
  showValue = true,
  animated = true,
  label = '',
  className = ''
}) => {
  const [displayValue, setDisplayValue] = useState(0)
  const percentage = Math.min((value / max) * 100, 100)

  const colorClasses = {
    purple: {
      bg: 'bg-purple-100',
      fill: 'from-purple-500 to-purple-600',
      text: 'text-purple-600'
    },
    blue: {
      bg: 'bg-blue-100',
      fill: 'from-blue-500 to-blue-600',
      text: 'text-blue-600'
    },
    green: {
      bg: 'bg-green-100',
      fill: 'from-green-500 to-green-600',
      text: 'text-green-600'
    },
    yellow: {
      bg: 'bg-yellow-100',
      fill: 'from-yellow-500 to-yellow-600',
      text: 'text-yellow-600'
    },
    red: {
      bg: 'bg-red-100',
      fill: 'from-red-500 to-red-600',
      text: 'text-red-600'
    }
  }

  const sizeClasses = {
    small: 'h-2',
    medium: 'h-3',
    large: 'h-4'
  }

  const colors = colorClasses[color] || colorClasses.purple

  // Animate progress
  useEffect(() => {
    if (!animated) {
      setDisplayValue(percentage)
      return
    }

    const duration = 1500
    const steps = 60
    const increment = percentage / steps
    let current = 0
    
    const timer = setInterval(() => {
      current += increment
      if (current >= percentage) {
        setDisplayValue(percentage)
        clearInterval(timer)
      } else {
        setDisplayValue(current)
      }
    }, duration / steps)

    return () => clearInterval(timer)
  }, [percentage, animated])

  return (
    <div className={`w-full ${className}`}>
      {/* Label and value */}
      {(label || showValue) && (
        <div className="flex justify-between items-center mb-2">
          {label && (
            <span className="text-sm font-medium text-gray-700">{label}</span>
          )}
          {showValue && (
            <motion.span
              key={Math.floor(displayValue)}
              initial={{ scale: 1.2, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className={`text-sm font-semibold ${colors.text}`}
            >
              {Math.floor(displayValue)}%
            </motion.span>
          )}
        </div>
      )}

      {/* Progress bar container */}
      <div className={`
        relative w-full ${sizeClasses[size]} ${colors.bg} rounded-full overflow-hidden
        shadow-inner
      `}>
        {/* Progress fill */}
        <motion.div
          className={`
            h-full bg-gradient-to-r ${colors.fill} rounded-full
            relative overflow-hidden
          `}
          initial={{ width: 0 }}
          animate={{ width: `${displayValue}%` }}
          transition={{ 
            duration: animated ? 1.5 : 0, 
            ease: "easeOut" 
          }}
        >
          {/* Shimmer effect */}
          <motion.div
            className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-30"
            animate={{ x: ['-100%', '100%'] }}
            transition={{ 
              duration: 2, 
              repeat: Infinity, 
              ease: "linear",
              delay: 1.5 
            }}
            style={{ width: '50%' }}
          />
        </motion.div>

        {/* Pulse effect for active progress */}
        {displayValue > 0 && displayValue < 100 && (
          <motion.div
            className={`absolute right-0 top-0 h-full w-1 bg-white opacity-60`}
            animate={{ opacity: [0.6, 1, 0.6] }}
            transition={{ duration: 1, repeat: Infinity, ease: "easeInOut" }}
            style={{ right: `${100 - displayValue}%` }}
          />
        )}
      </div>

      {/* Success indicator */}
      {displayValue >= 100 && (
        <motion.div
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
          className="flex items-center justify-center mt-2"
        >
          <span className="text-green-500 text-sm font-medium flex items-center gap-1">
            ✅ Complete
          </span>
        </motion.div>
      )}
    </div>
  )
}

export default ProgressBar