import { motion } from 'framer-motion'

const EnhancedLoadingSpinner = ({ size = 'medium', message = 'Loading...', showMessage = true }) => {
  const sizeClasses = {
    small: 'w-6 h-6',
    medium: 'w-12 h-12',
    large: 'w-16 h-16'
  }

  const dotSizes = {
    small: 'w-2 h-2',
    medium: 'w-3 h-3',
    large: 'w-4 h-4'
  }

  return (
    <div className="flex flex-col items-center justify-center space-y-4">
      {/* Animated Spinner */}
      <div className="relative">
        {/* Outer ring */}
        <motion.div
          className={`${sizeClasses[size]} border-4 border-gray-200 rounded-full`}
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
        />
        
        {/* Inner spinning gradient */}
        <motion.div
          className={`absolute inset-0 ${sizeClasses[size]} border-4 border-transparent border-t-purple-500 border-r-pink-500 rounded-full`}
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        />
        
        {/* Center pulse dot */}
        <motion.div
          className={`absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 ${dotSizes[size]} bg-gradient-to-r from-purple-500 to-pink-500 rounded-full`}
          animate={{ scale: [1, 1.2, 1] }}
          transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
        />
      </div>

      {/* Animated dots */}
      <div className="flex space-x-1">
        {[0, 1, 2].map((index) => (
          <motion.div
            key={index}
            className="w-2 h-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"
            animate={{ y: [0, -8, 0] }}
            transition={{
              duration: 0.8,
              repeat: Infinity,
              delay: index * 0.2,
              ease: "easeInOut"
            }}
          />
        ))}
      </div>

      {/* Loading message */}
      {showMessage && (
        <motion.p
          className="text-gray-600 text-sm font-medium"
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        >
          {message}
        </motion.p>
      )}
    </div>
  )
}

export default EnhancedLoadingSpinner