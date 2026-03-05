import { motion } from 'framer-motion'

/**
 * PageWrapper - Subtle page entrance animations for SaaS UX
 * 
 * Features:
 * - Fade-in with slight upward motion (≤ 8px)
 * - Runs once per page load
 * - Professional, non-distracting animation
 * - Optimized for performance
 * 
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Page content to animate
 * @param {string} props.className - Additional CSS classes
 * @param {number} props.delay - Animation delay in seconds (default: 0)
 * @param {number} props.duration - Animation duration in seconds (default: 0.6)
 */
const PageWrapper = ({ 
  children, 
  className = '', 
  delay = 0,
  duration = 0.6 
}) => {
  // Animation variants for consistent behavior
  const pageVariants = {
    initial: {
      opacity: 0,
      y: 8, // Subtle 8px upward motion
      scale: 0.98 // Very subtle scale for depth
    },
    animate: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: {
        duration: duration,
        delay: delay,
        ease: [0.25, 0.46, 0.45, 0.94], // Custom easing for professional feel
        opacity: {
          duration: duration * 0.8, // Opacity animates slightly faster
          ease: "easeOut"
        },
        y: {
          duration: duration,
          ease: [0.25, 0.46, 0.45, 0.94]
        },
        scale: {
          duration: duration * 1.2, // Scale animates slightly slower
          ease: "easeOut"
        }
      }
    },
    exit: {
      opacity: 0,
      y: -4, // Subtle exit motion
      scale: 0.99,
      transition: {
        duration: 0.3,
        ease: "easeIn"
      }
    }
  }

  return (
    <motion.div
      className={className}
      variants={pageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      // Performance optimizations
      style={{
        willChange: 'transform, opacity',
        backfaceVisibility: 'hidden',
        perspective: 1000
      }}
    >
      {children}
    </motion.div>
  )
}

export default PageWrapper