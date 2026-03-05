import { motion } from 'framer-motion'
import PageHeader from './PageHeader'

/**
 * Pre-built Header Variants for Common SaaS Dashboard Pages
 */

// Welcome Header for Dashboard
export const WelcomeHeader = ({ user, className = '' }) => {
  const badge = (
    <motion.div 
      className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-white/20 text-white backdrop-blur-sm border border-white/30"
      whileHover={{ scale: 1.05 }}
      transition={{ duration: 0.2 }}
    >
      <span className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></span>
      Online
    </motion.div>
  )

  return (
    <PageHeader
      title={`Welcome back, ${user?.first_name || 'User'}!`}
      subtitle="Ready to analyze your speech and improve your communication skills?"
      badge={badge}
      variant="primary"
      size="md"
      className={className}
    />
  )
}

// Analysis Header
export const AnalysisHeader = ({ className = '' }) => {
  const badge = (
    <motion.div 
      className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 border border-blue-200"
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: 0.2, duration: 0.5 }}
    >
      🎤 Audio Analysis
    </motion.div>
  )

  return (
    <PageHeader
      title="Speech Analysis"
      subtitle="Upload your audio file to get detailed analysis of your speech patterns, pace, and delivery."
      badge={badge}
      variant="secondary"
      size="md"
      className={className}
    />
  )
}

// Interview Header
export const InterviewHeader = ({ selectedCategory, className = '' }) => {
  const badge = (
    <motion.div 
      className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800 border border-purple-200"
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.2, duration: 0.5 }}
    >
      💼 {selectedCategory ? selectedCategory.charAt(0).toUpperCase() + selectedCategory.slice(1) : 'Interview'} Mode
    </motion.div>
  )

  return (
    <PageHeader
      title="Interview Practice"
      subtitle="Practice with real interview questions and get AI-powered feedback on your answers, including relevance analysis."
      badge={badge}
      variant="accent"
      size="md"
      className={className}
    />
  )
}

// History Header with Stats
export const HistoryHeader = ({ totalSessions, className = '' }) => {
  const badge = totalSessions > 0 ? (
    <motion.div 
      className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800 border border-emerald-200"
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2, duration: 0.5 }}
    >
      📊 {totalSessions} Session{totalSessions !== 1 ? 's' : ''} Recorded
    </motion.div>
  ) : null

  const actions = totalSessions > 0 ? (
    <motion.div 
      className="flex gap-2"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.4, duration: 0.5 }}
    >
      <button className="px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg text-sm font-medium transition-all duration-200 backdrop-blur-sm border border-white/30">
        Export Data
      </button>
    </motion.div>
  ) : null

  return (
    <PageHeader
      title="Analysis History"
      subtitle="Track your progress over time with detailed analytics and performance charts."
      badge={badge}
      actions={actions}
      variant="primary"
      size="md"
      className={className}
    />
  )
}

// Loading Header
export const LoadingHeader = ({ title, subtitle, className = '' }) => {
  const badge = (
    <motion.div 
      className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 border border-blue-200"
      animate={{ opacity: [0.5, 1, 0.5] }}
      transition={{ duration: 2, repeat: Infinity }}
    >
      <div className="w-2 h-2 bg-blue-500 rounded-full mr-2 animate-pulse"></div>
      Processing...
    </motion.div>
  )

  return (
    <PageHeader
      title={title || "Processing"}
      subtitle={subtitle || "Please wait while we analyze your content..."}
      badge={badge}
      variant="secondary"
      size="md"
      className={className}
    />
  )
}

// Error Header
export const ErrorHeader = ({ title, subtitle, onRetry, className = '' }) => {
  const badge = (
    <motion.div 
      className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 border border-red-200"
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: 0.2, duration: 0.5 }}
    >
      ⚠️ Error
    </motion.div>
  )

  const actions = onRetry ? (
    <motion.button
      onClick={onRetry}
      className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg text-sm font-medium transition-all duration-200"
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
    >
      Try Again
    </motion.button>
  ) : null

  return (
    <PageHeader
      title={title || "Something went wrong"}
      subtitle={subtitle || "We encountered an error while processing your request."}
      badge={badge}
      actions={actions}
      variant="secondary"
      size="md"
      className={className}
    />
  )
}

// Success Header
export const SuccessHeader = ({ title, subtitle, className = '' }) => {
  const badge = (
    <motion.div 
      className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 border border-green-200"
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: 0.2, duration: 0.5 }}
    >
      ✅ Complete
    </motion.div>
  )

  return (
    <PageHeader
      title={title || "Success!"}
      subtitle={subtitle || "Your request has been processed successfully."}
      badge={badge}
      variant="accent"
      size="md"
      className={className}
    />
  )
}