import { motion, AnimatePresence } from 'framer-motion'
import { useEffect } from 'react'

const AnimatedModal = ({ 
  isOpen, 
  onClose, 
  children, 
  title = '',
  size = 'medium',
  closeOnBackdrop = true,
  showCloseButton = true
}) => {
  const sizeClasses = {
    small: 'max-w-md',
    medium: 'max-w-2xl',
    large: 'max-w-4xl',
    full: 'max-w-6xl'
  }

  // Handle escape key
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose()
      }
    }

    document.addEventListener('keydown', handleEscape)
    return () => document.removeEventListener('keydown', handleEscape)
  }, [isOpen, onClose])

  // Prevent body scroll when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'unset'
    }

    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [isOpen])

  const backdropVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { duration: 0.3, ease: "easeOut" }
    },
    exit: { 
      opacity: 0,
      transition: { duration: 0.2, ease: "easeIn" }
    }
  }

  const modalVariants = {
    hidden: { 
      opacity: 0, 
      scale: 0.9, 
      y: 0,
      rotateX: 0
    },
    visible: { 
      opacity: 1, 
      scale: 1, 
      y: 0,
      rotateX: 0,
      transition: { 
        duration: 0.4, 
        ease: "easeOut",
        type: "spring",
        stiffness: 300,
        damping: 30
      }
    },
    exit: { 
      opacity: 0, 
      scale: 0.95, 
      y: 0,
      rotateX: 0,
      transition: { 
        duration: 0.2, 
        ease: "easeIn" 
      }
    }
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 min-h-screen"
          variants={backdropVariants}
          initial="hidden"
          animate="visible"
          exit="exit"
          style={{ alignItems: 'center', justifyContent: 'center' }}
        >
          {/* Backdrop */}
          <motion.div
            className="absolute inset-0 bg-black/50 backdrop-blur-sm"
            onClick={closeOnBackdrop ? onClose : undefined}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          />

          {/* Modal */}
          <motion.div
            className={`
              relative w-full ${sizeClasses[size]} max-h-[85vh] 
              bg-white rounded-3xl shadow-2xl overflow-hidden
              border border-gray-200 mx-auto my-auto
            `}
            variants={modalVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
            style={{ perspective: 1000, margin: 'auto' }}
          >
            {/* Header */}
            {(title || showCloseButton) && (
              <motion.div
                className="flex items-center justify-between p-6 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-white"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
              >
                {title && (
                  <h2 className="text-2xl font-bold text-gray-800">{title}</h2>
                )}
                
                {showCloseButton && (
                  <motion.button
                    onClick={onClose}
                    className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition-all duration-200"
                    whileHover={{ scale: 1.1, rotate: 90 }}
                    whileTap={{ scale: 0.9 }}
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </motion.button>
                )}
              </motion.div>
            )}

            {/* Content */}
            <motion.div
              className="overflow-y-auto max-h-[calc(85vh-80px)]"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              {children}
            </motion.div>

            {/* Decorative elements */}
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-purple-500 via-pink-500 to-purple-500" />
            
            {/* Floating particles */}
            <div className="absolute inset-0 pointer-events-none overflow-hidden">
              {[...Array(3)].map((_, i) => (
                <motion.div
                  key={i}
                  className="absolute w-2 h-2 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full opacity-20"
                  style={{
                    left: `${20 + (i * 30)}%`,
                    top: `${10 + (i * 20)}%`,
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
        </motion.div>
      )}
    </AnimatePresence>
  )
}

export default AnimatedModal