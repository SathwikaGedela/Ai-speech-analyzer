import { motion } from 'framer-motion'
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

const LandingHero = ({ scrollToSection }) => {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    // Trigger animations after component mounts
    setIsVisible(true)
  }, [])

  // Animation variants for staggered text appearance
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.3,
        delayChildren: 0.2
      }
    }
  }

  const itemVariants = {
    hidden: { 
      opacity: 0, 
      y: 20,
      filter: 'blur(4px)'
    },
    visible: { 
      opacity: 1, 
      y: 0,
      filter: 'blur(0px)',
      transition: {
        duration: 0.8,
        ease: [0.25, 0.46, 0.45, 0.94] // Custom easing for smooth feel
      }
    }
  }

  // Subtle floating animation for accent elements
  const floatingVariants = {
    animate: {
      y: [-2, 2, -2],
      transition: {
        duration: 4,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  }

  // Gradient text animation
  const gradientVariants = {
    hidden: { backgroundPosition: '200% center' },
    visible: {
      backgroundPosition: '0% center',
      transition: {
        duration: 2,
        ease: 'easeOut',
        delay: 0.5
      }
    }
  }

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Subtle background elements */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,119,198,0.1),transparent_50%)]" />
      
      {/* Animated grid pattern */}
      <motion.div 
        className="absolute inset-0 opacity-20"
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.2 }}
        transition={{ duration: 2, delay: 1 }}
      >
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:50px_50px]" />
      </motion.div>

      {/* Main content container */}
      <motion.div
        className="relative z-10 max-w-6xl mx-auto px-6 text-center"
        variants={containerVariants}
        initial="hidden"
        animate={isVisible ? "visible" : "hidden"}
      >
        {/* Badge/Label */}
        <motion.div
          variants={itemVariants}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 text-sm text-white/90 mb-8"
        >
          <motion.div
            variants={floatingVariants}
            animate="animate"
            className="w-2 h-2 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full"
          />
          AI-Powered Speech Analysis
        </motion.div>

        {/* Main headline */}
        <motion.h1
          variants={itemVariants}
          className="text-5xl md:text-7xl lg:text-8xl font-bold mb-6 leading-tight"
        >
          <motion.span
            className="bg-gradient-to-r from-white via-purple-200 to-white bg-[length:200%_100%] bg-clip-text text-transparent"
            variants={gradientVariants}
            initial="hidden"
            animate={isVisible ? "visible" : "hidden"}
          >
            Transform Your
          </motion.span>
          <br />
          <motion.span
            className="bg-gradient-to-r from-purple-400 via-pink-400 to-purple-400 bg-[length:200%_100%] bg-clip-text text-transparent"
            variants={gradientVariants}
            initial="hidden"
            animate={isVisible ? "visible" : "hidden"}
          >
            Communication
          </motion.span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          variants={itemVariants}
          className="text-xl md:text-2xl text-white/80 mb-12 max-w-3xl mx-auto leading-relaxed"
        >
          Advanced AI speech analysis that provides real-time insights into your communication patterns, 
          emotional tone, and professional presence.
        </motion.p>

        {/* Trust indicators */}
        <motion.div
          variants={itemVariants}
          className="flex flex-wrap justify-center items-center gap-8 mb-12 text-white/60"
        >
          <div className="flex items-center gap-2">
            <motion.div
              variants={floatingVariants}
              animate="animate"
              className="w-3 h-3 bg-green-400 rounded-full"
            />
            <span className="text-sm">99.9% Accuracy</span>
          </div>
          <div className="flex items-center gap-2">
            <motion.div
              variants={floatingVariants}
              animate="animate"
              style={{ animationDelay: '1s' }}
              className="w-3 h-3 bg-blue-400 rounded-full"
            />
            <span className="text-sm">Real-time Analysis</span>
          </div>
          <div className="flex items-center gap-2">
            <motion.div
              variants={floatingVariants}
              animate="animate"
              style={{ animationDelay: '2s' }}
              className="w-3 h-3 bg-purple-400 rounded-full"
            />
            <span className="text-sm">Enterprise Ready</span>
          </div>
        </motion.div>

        {/* CTA Buttons */}
        <motion.div
          variants={itemVariants}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
        >
          <Link to="/auth">
            <motion.button
              className="group relative px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl overflow-hidden transition-all duration-300 hover:shadow-2xl hover:shadow-purple-500/25"
              whileHover={{ 
                scale: 1.02,
                boxShadow: "0 20px 40px rgba(168, 85, 247, 0.4)"
              }}
              whileTap={{ scale: 0.98 }}
            >
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-purple-400 to-pink-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                initial={false}
              />
              <span className="relative z-10">Start Free Analysis</span>
            </motion.button>
          </Link>

          <motion.button
            className="group px-8 py-4 border-2 border-white/20 text-white font-semibold rounded-xl backdrop-blur-sm hover:bg-white/10 transition-all duration-300"
            whileHover={{ 
              scale: 1.02,
              borderColor: "rgba(255, 255, 255, 0.4)"
            }}
            whileTap={{ scale: 0.98 }}
            onClick={() => scrollToSection && scrollToSection('demo')}
          >
            Watch Demo
          </motion.button>
        </motion.div>
      </motion.div>

      {/* Subtle scroll indicator */}
      <motion.div
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 2, duration: 1 }}
      >
        <motion.div
          className="w-6 h-10 border-2 border-white/30 rounded-full flex justify-center"
          animate={{ y: [0, 5, 0] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        >
          <motion.div
            className="w-1 h-3 bg-white/50 rounded-full mt-2"
            animate={{ scaleY: [1, 0.5, 1] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
          />
        </motion.div>
      </motion.div>
    </section>
  )
}

export default LandingHero