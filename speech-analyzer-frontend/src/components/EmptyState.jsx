import { motion } from 'framer-motion'

const EmptyState = ({ 
  icon = '📊', 
  title = 'No Data Available', 
  description = 'Get started by creating your first item.',
  primaryAction = null,
  secondaryAction = null,
  illustration = null
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className="text-center py-12 px-6"
    >
      {/* Animated Icon/Illustration */}
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
        className="mb-6"
      >
        {illustration ? (
          <div className="w-32 h-32 mx-auto mb-4">
            {illustration}
          </div>
        ) : (
          <motion.div
            animate={{ 
              y: [0, -10, 0],
              rotate: [0, 5, -5, 0]
            }}
            transition={{ 
              duration: 4, 
              repeat: Infinity, 
              ease: "easeInOut" 
            }}
            className="text-8xl mb-4 inline-block"
          >
            {icon}
          </motion.div>
        )}
      </motion.div>

      {/* Title */}
      <motion.h3
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="text-2xl font-bold text-gray-800 mb-3"
      >
        {title}
      </motion.h3>

      {/* Description */}
      <motion.p
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.5 }}
        className="text-gray-600 mb-8 max-w-md mx-auto leading-relaxed"
      >
        {description}
      </motion.p>

      {/* Action Buttons */}
      {(primaryAction || secondaryAction) && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
        >
          {primaryAction && (
            <motion.button
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.95 }}
              className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-300"
              onClick={primaryAction.onClick}
            >
              {primaryAction.label}
            </motion.button>
          )}
          
          {secondaryAction && (
            <motion.button
              whileHover={{ scale: 1.02, y: -1 }}
              whileTap={{ scale: 0.98 }}
              className="px-6 py-3 bg-gray-100 text-gray-700 rounded-xl font-semibold hover:bg-gray-200 transition-all duration-300"
              onClick={secondaryAction.onClick}
            >
              {secondaryAction.label}
            </motion.button>
          )}
        </motion.div>
      )}

      {/* Floating particles for visual interest */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        {[...Array(6)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full opacity-20"
            style={{
              left: `${20 + (i * 15)}%`,
              top: `${30 + (i % 3) * 20}%`,
            }}
            animate={{
              y: [0, -20, 0],
              x: [0, 10, -10, 0],
              opacity: [0.2, 0.5, 0.2],
            }}
            transition={{
              duration: 4 + i,
              repeat: Infinity,
              delay: i * 0.5,
              ease: "easeInOut"
            }}
          />
        ))}
      </div>
    </motion.div>
  )
}

export default EmptyState