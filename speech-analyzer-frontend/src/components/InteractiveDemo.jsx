import { useState } from 'react'
import { Link } from 'react-router-dom'

const InteractiveDemo = () => {
  const [currentStep, setCurrentStep] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)

  const demoSteps = [
    {
      title: "Welcome to Speech Analyzer",
      description: "An AI-powered tool for improving your communication skills",
      image: "🎤",
      content: "Get detailed feedback on your speaking patterns, pace, and clarity."
    },
    {
      title: "Create Your Account",
      description: "Sign up to start analyzing your speech",
      image: "👤",
      content: "Quick registration process - just enter your basic information."
    },
    {
      title: "Dashboard Overview",
      description: "Access all features from your personal dashboard",
      image: "🏠",
      content: "Speech Analysis, Interview Mode, and Progress History all in one place."
    },
    {
      title: "Record Your Speech",
      description: "Use our built-in recorder or upload audio files",
      image: "🎙️",
      content: "Record directly in your browser or upload existing audio files."
    },
    {
      title: "AI Analysis Results",
      description: "Get comprehensive feedback on your communication",
      image: "📊",
      content: "Speaking speed, filler words, sentiment, grammar, and more."
    },
    {
      title: "Interview Practice",
      description: "Practice with real interview questions",
      image: "💼",
      content: "Get relevance scores and improvement suggestions for your answers."
    },
    {
      title: "Track Your Progress",
      description: "Monitor improvement over time",
      image: "📈",
      content: "View detailed analytics and track your communication development."
    }
  ]

  const playDemo = () => {
    setIsPlaying(true)
    setCurrentStep(0)
    
    const interval = setInterval(() => {
      setCurrentStep(prev => {
        if (prev >= demoSteps.length - 1) {
          clearInterval(interval)
          setIsPlaying(false)
          return 0
        }
        return prev + 1
      })
    }, 3000) // Change step every 3 seconds
  }

  const nextStep = () => {
    setCurrentStep(prev => (prev + 1) % demoSteps.length)
  }

  const prevStep = () => {
    setCurrentStep(prev => (prev - 1 + demoSteps.length) % demoSteps.length)
  }

  return (
    <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-3xl p-8 border border-purple-100">
      <div className="text-center mb-8">
        <h3 className="text-3xl font-bold text-slate-900 mb-4">Interactive Demo</h3>
        <p className="text-slate-600 mb-6">
          See how Speech Analyzer works step by step
        </p>
        
        {!isPlaying && (
          <button
            onClick={playDemo}
            className="inline-flex items-center bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-2xl text-lg font-semibold hover:from-purple-700 hover:to-pink-700 hover:scale-105 hover:shadow-xl transition-all duration-300 mb-6"
          >
            <span className="text-2xl mr-2">▶️</span>
            Play Demo
          </button>
        )}
        
        {isPlaying && (
          <div className="inline-flex items-center bg-green-100 text-green-700 px-4 py-2 rounded-full text-sm font-medium mb-6">
            <div className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
            Demo Playing...
          </div>
        )}
      </div>

      {/* Demo Content */}
      <div className="bg-white rounded-2xl p-8 shadow-lg mb-6">
        <div className="text-center">
          <div className="text-6xl mb-4">{demoSteps[currentStep].image}</div>
          <h4 className="text-2xl font-bold text-slate-900 mb-3">
            {demoSteps[currentStep].title}
          </h4>
          <p className="text-lg text-slate-600 mb-4">
            {demoSteps[currentStep].description}
          </p>
          <p className="text-slate-700 leading-relaxed">
            {demoSteps[currentStep].content}
          </p>
        </div>
      </div>

      {/* Navigation Controls */}
      <div className="flex items-center justify-between">
        <button
          onClick={prevStep}
          className="flex items-center px-4 py-2 bg-white border border-purple-200 text-purple-600 rounded-lg hover:bg-purple-50 transition-colors"
          disabled={isPlaying}
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Previous
        </button>

        {/* Step Indicators */}
        <div className="flex space-x-2">
          {demoSteps.map((_, index) => (
            <button
              key={index}
              onClick={() => !isPlaying && setCurrentStep(index)}
              className={`w-3 h-3 rounded-full transition-colors ${
                index === currentStep
                  ? 'bg-purple-600'
                  : 'bg-purple-200 hover:bg-purple-300'
              }`}
              disabled={isPlaying}
            />
          ))}
        </div>

        <button
          onClick={nextStep}
          className="flex items-center px-4 py-2 bg-white border border-purple-200 text-purple-600 rounded-lg hover:bg-purple-50 transition-colors"
          disabled={isPlaying}
        >
          Next
          <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      {/* Call to Action */}
      <div className="text-center mt-8 pt-6 border-t border-purple-200">
        <p className="text-slate-600 mb-4">Ready to try it yourself?</p>
        <Link
          to="/auth"
          className="inline-flex items-center bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-2xl font-semibold hover:from-purple-700 hover:to-pink-700 hover:scale-105 hover:shadow-xl transition-all duration-300"
        >
          <span className="mr-2">🚀</span>
          Get Started Now
          <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </Link>
      </div>
    </div>
  )
}

export default InteractiveDemo