import { motion } from 'framer-motion'

/**
 * SectionWrapper - Staggered animations for page sections
 * 
 * Use this for individual sections within a page to create
 * a subtle staggered entrance effect
 * 
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Section content
 * @param {string} props.className - Additional CSS classes
 * @param {number} props.index - Section index for stagger delay (default: 0)
 * @param {number} props.staggerDelay - Delay between sections in seconds (default: 0.1)
 */
const SectionWrapper = ({ 
  children, 
  className = '', 
  index = 0,
  staggerDelay = 0.1 
}) => {
  const sectionVariants = {
    initial: {
      opacity: 0,
      y: 6, // Even more subtle motion for sections
      scale: 0.99
    },
    animate: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: {
        duration: 0.5,
        delay: index * staggerDelay,
        ease: [0.25, 0.46, 0.45, 0.94],
        opacity: {
          duration: 0.4,
          ease: "easeOut"
        }
      }
    }
  }

  return (
    <motion.div
      className={className}
      variants={sectionVariants}
      initial="initial"
      animate="animate"
      style={{
        willChange: 'transform, opacity'
      }}
    >
      {children}
    </motion.div>
  )
}

export default SectionWrapper