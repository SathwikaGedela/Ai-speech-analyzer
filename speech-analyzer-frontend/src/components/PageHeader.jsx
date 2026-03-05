import { motion } from 'framer-motion'

/**
 * Enhanced Page Header Component for SaaS Dashboard
 * 
 * Features:
 * - Improved typography hierarchy
 * - Subtle gradient backgrounds
 * - Soft entrance animations
 * - Professional tone
 * - Flexible content support
 * 
 * @param {Object} props - Component props
 * @param {string} props.title - Main page title
 * @param {string} props.subtitle - Optional subtitle/description
 * @param {React.ReactNode} props.badge - Optional badge/status indicator
 * @param {React.ReactNode} props.actions - Optional action buttons/elements
 * @param {string} props.variant - Color variant: 'primary', 'secondary', 'accent', 'neutral'
 * @param {string} props.size - Size variant: 'sm', 'md', 'lg'
 * @param {string} props.className - Additional CSS classes
 */
const PageHeader = ({
  title,
  subtitle,
  badge,
  actions,
  variant = 'primary',
  size = 'md',
  className = ''
}) => {
  
  // Variant configurations
  const variants = {
    primary: {
      gradient: 'from-indigo-500 via-purple-500 to-pink-500',
      overlay: 'from-indigo-600/90 via-purple-600/90 to-pink-600/90',
      accent: 'text-indigo-100',
      border: 'border-indigo-200/20'
    },
    secondary: {
      gradient: 'from-slate-600 via-slate-700 to-slate-800',
      overlay: 'from-slate-700/90 via-slate-800/90 to-slate-900/90',
      accent: 'text-slate-200',
      border: 'border-slate-300/20'
    },
    accent: {
      gradient: 'from-emerald-500 via-teal-500 to-cyan-500',
      overlay: 'from-emerald-600/90 via-teal-600/90 to-cyan-600/90',
      accent: 'text-emerald-100',
      border: 'border-emerald-200/20'
    },
    neutral: {
      gradient: 'from-gray-50 via-white to-gray-50',
      overlay: 'from-gray-100/95 via-white/95 to-gray-100/95',
      accent: 'text-gray-600',
      border: 'border-gray-200/40'
    }
  }

  // Size configurations
  const sizes = {
    sm: {
      container: 'px-6 py-4',
      title: 'text-xl md:text-2xl',
      subtitle: 'text-sm',
      spacing: 'space-y-1'
    },
    md: {
      container: 'px-8 py-6',
      title: 'text-2xl md:text-3xl lg:text-4xl',
      subtitle: 'text-base md:text-lg',
      spacing: 'space-y-2'
    },
    lg: {
      container: 'px-10 py-8',
      title: 'text-3xl md:text-4xl lg:text-5xl',
      subtitle: 'text-lg md:text-xl',
      spacing: 'space-y-3'
    }
  }

  const currentVariant = variants[variant]
  const currentSize = sizes[size]

  // Animation variants
  const containerVariants = {
    initial: { opacity: 0, y: 12 },
    animate: { 
      opacity: 1, 
      y: 0,
      transition: {
        duration: 0.7,
        ease: [0.25, 0.46, 0.45, 0.94],
        staggerChildren: 0.15
      }
    }
  }

  const itemVariants = {
    initial: { opacity: 0, y: 8, scale: 0.98 },
    animate: { 
      opacity: 1, 
      y: 0, 
      scale: 1,
      transition: {
        duration: 0.6,
        ease: [0.25, 0.46, 0.45, 0.94]
      }
    }
  }

  const titleVariants = {
    initial: { opacity: 0, y: 12, scale: 0.95 },
    animate: { 
      opacity: 1, 
      y: 0, 
      scale: 1,
      transition: {
        duration: 0.8,
        ease: [0.25, 0.46, 0.45, 0.94],
        delay: 0.1
      }
    }
  }

  const subtitleVariants = {
    initial: { opacity: 0, y: 8 },
    animate: { 
      opacity: 1, 
      y: 0,
      transition: {
        duration: 0.6,
        ease: "easeOut",
        delay: 0.3
      }
    }
  }

  return (
    <motion.div
      className={`
        relative overflow-hidden rounded-3xl
        ${variant === 'neutral' ? 'border' : ''}
        ${currentVariant.border}
        ${className}
      `}
      variants={containerVariants}
      initial="initial"
      animate="animate"
    >
      {/* Background Gradient */}
      <div className={`
        absolute inset-0 bg-gradient-to-br ${currentVariant.gradient}
      `} />
      
      {/* Subtle Pattern Overlay */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-transparent to-black/20" />
        <div 
          className="absolute inset-0 opacity-30"
          style={{
            backgroundImage: `radial-gradient(circle at 25% 25%, rgba(255,255,255,0.1) 0%, transparent 50%),
                             radial-gradient(circle at 75% 75%, rgba(255,255,255,0.05) 0%, transparent 50%)`
          }}
        />
      </div>

      {/* Content Container */}
      <div className={`
        relative z-10 ${currentSize.container}
        ${variant === 'neutral' ? 'text-gray-900' : 'text-white'}
      `}>
        <div className="flex items-start justify-between">
          {/* Main Content */}
          <div className={`flex-1 ${currentSize.spacing}`}>
            {/* Badge */}
            {badge && (
              <motion.div variants={itemVariants}>
                {badge}
              </motion.div>
            )}

            {/* Title */}
            <motion.h1 
              className={`
                font-bold tracking-tight leading-tight
                ${currentSize.title}
                ${variant === 'neutral' ? 'text-gray-900' : 'text-white'}
              `}
              variants={titleVariants}
            >
              {title}
            </motion.h1>

            {/* Subtitle */}
            {subtitle && (
              <motion.p 
                className={`
                  ${currentSize.subtitle} leading-relaxed
                  ${variant === 'neutral' ? 'text-gray-600' : currentVariant.accent}
                `}
                variants={subtitleVariants}
              >
                {subtitle}
              </motion.p>
            )}
          </div>

          {/* Actions */}
          {actions && (
            <motion.div 
              className="flex-shrink-0 ml-6"
              variants={itemVariants}
            >
              {actions}
            </motion.div>
          )}
        </div>
      </div>

      {/* Bottom Highlight */}
      <div className={`
        absolute bottom-0 left-0 right-0 h-px
        bg-gradient-to-r from-transparent via-white/30 to-transparent
      `} />
    </motion.div>
  )
}

export default PageHeader