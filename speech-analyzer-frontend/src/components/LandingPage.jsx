import { Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import LandingHero from './LandingHero'
import InteractiveDemo from './InteractiveDemo'

const LandingPage = () => {
  const [scrolled, setScrolled] = useState(false)
  const [isVisible, setIsVisible] = useState({})

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50)
      
      // Intersection Observer for scroll animations
      const elements = document.querySelectorAll('.animate-on-scroll')
      elements.forEach((element, index) => {
        const rect = element.getBoundingClientRect()
        const isInView = rect.top < window.innerHeight && rect.bottom > 0
        
        if (isInView && !isVisible[index]) {
          setIsVisible(prev => ({ ...prev, [index]: true }))
          element.classList.add('animate-slide-in-up')
        }
      })
    }

    window.addEventListener('scroll', handleScroll)
    handleScroll() // Initial check
    
    return () => window.removeEventListener('scroll', handleScroll)
  }, [isVisible])

  const scrollToSection = (sectionId) => {
    document.getElementById(sectionId)?.scrollIntoView({
      behavior: 'smooth'
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 overflow-hidden">
      {/* Navigation */}
      <nav className={`fixed top-0 w-full z-50 transition-all duration-500 ${
        scrolled ? 'bg-white/95 backdrop-blur-lg shadow-xl animate-nav-slide-down' : 'bg-transparent'
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className={`text-2xl font-bold transition-all duration-500 ${
                scrolled ? 'text-slate-800' : 'text-white'
              }`}>
                <span className="text-3xl mr-2">🎤</span>
                SpeechAnalyzer
              </div>
            </div>
            <div className="hidden md:flex space-x-8">
              <button 
                onClick={() => scrollToSection('features')} 
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 hover:scale-105 ${
                  scrolled 
                    ? 'text-slate-700 hover:text-purple-600 hover:bg-purple-50' 
                    : 'text-white/90 hover:text-white hover:bg-white/10'
                }`}
              >
                Features
              </button>
              <button 
                onClick={() => scrollToSection('about')} 
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 hover:scale-105 ${
                  scrolled 
                    ? 'text-slate-700 hover:text-purple-600 hover:bg-purple-50' 
                    : 'text-white/90 hover:text-white hover:bg-white/10'
                }`}
              >
                About
              </button>
              <button 
                onClick={() => scrollToSection('demo')} 
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 hover:scale-105 ${
                  scrolled 
                    ? 'text-slate-700 hover:text-purple-600 hover:bg-purple-50' 
                    : 'text-white/90 hover:text-white hover:bg-white/10'
                }`}
              >
                Demo
              </button>
              <Link 
                to="/auth" 
                className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-2 rounded-full text-sm font-semibold hover:from-purple-700 hover:to-pink-700 hover:scale-105 hover:shadow-lg transition-all duration-300"
              >
                Get Started
              </Link>
            </div>
            
            {/* Mobile menu button */}
            <div className="md:hidden">
              <Link 
                to="/auth" 
                className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-4 py-2 rounded-full text-sm font-semibold"
              >
                Start
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <LandingHero scrollToSection={scrollToSection} />

      {/* Features Section */}
      <section id="features" className="py-12 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12 animate-on-scroll">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-purple-100 text-purple-700 text-sm font-medium mb-6 animate-badge-bounce">
              <span className="mr-2 animate-sparkle">✨</span>
              Features
            </div>
            <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-6 animate-title-slide-up">
              Speech Analysis
              <span className="block text-purple-600 animate-gradient-text">Tools</span>
            </h2>
            <p className="text-xl text-slate-600 max-w-3xl mx-auto animate-subtitle-fade">
              AI-powered speech analysis and feedback system
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: '🎯',
                title: 'Speech Analysis',
                description: 'Analyze your speaking patterns and identify areas for improvement with detailed metrics and feedback.',
                features: ['Speaking pace analysis', 'Filler word detection', 'Vocabulary assessment', 'Speech clarity metrics'],
                gradient: 'from-purple-50 to-pink-50',
                iconGradient: 'from-purple-500 to-pink-500',
                borderColor: 'border-purple-100',
                dotColor: 'bg-purple-500'
              },
              {
                icon: '💼',
                title: 'Interview Practice',
                description: 'Practice with interview questions and get feedback on your responses to improve your interview skills.',
                features: ['Interview question practice', 'Answer evaluation', 'Response feedback', 'Practice sessions'],
                gradient: 'from-blue-50 to-indigo-50',
                iconGradient: 'from-blue-500 to-indigo-500',
                borderColor: 'border-blue-100',
                dotColor: 'bg-blue-500'
              },
              {
                icon: '😊',
                title: 'Sentiment Analysis',
                description: 'Understand the emotional tone of your speech and learn to convey the right emotions in your communication.',
                features: ['Emotion detection', 'Sentiment analysis', 'Tone assessment', 'Communication feedback'],
                gradient: 'from-green-50 to-emerald-50',
                iconGradient: 'from-green-500 to-emerald-500',
                borderColor: 'border-green-100',
                dotColor: 'bg-green-500'
              },
              {
                icon: '📊',
                title: 'Progress Tracking',
                description: 'Track your improvement over time with detailed analytics and personalized recommendations.',
                features: ['Performance tracking', 'Progress analytics', 'Improvement insights', 'Personal recommendations'],
                gradient: 'from-orange-50 to-red-50',
                iconGradient: 'from-orange-500 to-red-500',
                borderColor: 'border-orange-100',
                dotColor: 'bg-orange-500'
              },
              {
                icon: '⚡',
                title: 'Real-time Feedback',
                description: 'Get instant feedback on your speech with our fast processing engine for immediate insights.',
                features: ['Instant analysis', 'Real-time results', 'Quick transcription', 'Immediate feedback'],
                gradient: 'from-yellow-50 to-amber-50',
                iconGradient: 'from-yellow-500 to-amber-500',
                borderColor: 'border-yellow-100',
                dotColor: 'bg-yellow-500'
              },
              {
                icon: '🎵',
                title: 'Audio Support',
                description: 'Works with various audio formats and recording methods for flexible speech analysis.',
                features: ['Multiple audio formats', 'Recording options', 'File upload support', 'Cross-platform compatibility'],
                gradient: 'from-teal-50 to-cyan-50',
                iconGradient: 'from-teal-500 to-cyan-500',
                borderColor: 'border-teal-100',
                dotColor: 'bg-teal-500'
              }
            ].map((feature, index) => (
              <div
                key={index}
                className={`group bg-gradient-to-br ${feature.gradient} p-8 rounded-3xl hover:shadow-2xl hover:scale-105 transition-all duration-500 ${feature.borderColor} animate-on-scroll animate-feature-card`}
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className={`w-16 h-16 bg-gradient-to-br ${feature.iconGradient} rounded-2xl flex items-center justify-center text-2xl text-white mb-6 group-hover:scale-110 group-hover:rotate-6 transition-all duration-300 animate-icon-float`}>
                  {feature.icon}
                </div>
                <h3 className="text-2xl font-bold text-slate-900 mb-4 animate-title-slide">{feature.title}</h3>
                <p className="text-slate-600 mb-6 leading-relaxed animate-description-slide">
                  {feature.description}
                </p>
                <ul className="space-y-3">
                  {feature.features.map((item, featureIndex) => (
                    <li key={featureIndex} className="flex items-center text-slate-700 animate-list-item" style={{ animationDelay: `${featureIndex * 0.1}s` }}>
                      <div className={`w-2 h-2 ${feature.dotColor} rounded-full mr-3 animate-dot-pulse`}></div>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-12 px-4 bg-gradient-to-br from-slate-50 to-purple-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-purple-100 text-purple-700 text-sm font-medium mb-6">
              <span className="mr-2">🧠</span>
              About SpeechAnalyzer
            </div>
            <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-6">
              Speech Analysis
              <span className="block text-purple-600">Platform</span>
            </h2>
            <p className="text-xl text-slate-600 max-w-3xl mx-auto">
              A comprehensive tool for analyzing and improving your communication skills
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <h3 className="text-3xl font-bold text-slate-900 mb-6">Key Features</h3>
              
              <div className="space-y-6">
                <div className="flex items-start group">
                  <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center text-white text-xl mr-4 group-hover:scale-110 transition-transform">
                    🧠
                  </div>
                  <div>
                    <h4 className="text-xl font-semibold text-slate-900 mb-2">AI-Powered Analysis</h4>
                    <p className="text-slate-600 leading-relaxed">Advanced machine learning algorithms analyze your speech patterns and provide detailed feedback on various aspects of your communication.</p>
                  </div>
                </div>
                
                <div className="flex items-start group">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-500 rounded-xl flex items-center justify-center text-white text-xl mr-4 group-hover:scale-110 transition-transform">
                    🎯
                  </div>
                  <div>
                    <h4 className="text-xl font-semibold text-slate-900 mb-2">Personalized Feedback</h4>
                    <p className="text-slate-600 leading-relaxed">Get tailored recommendations based on your unique speaking patterns and areas for improvement.</p>
                  </div>
                </div>
                
                <div className="flex items-start group">
                  <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl flex items-center justify-center text-white text-xl mr-4 group-hover:scale-110 transition-transform">
                    📈
                  </div>
                  <div>
                    <h4 className="text-xl font-semibold text-slate-900 mb-2">Progress Tracking</h4>
                    <p className="text-slate-600 leading-relaxed">Monitor your improvement over time with detailed analytics and track your communication development.</p>
                  </div>
                </div>
                
                <div className="flex items-start group">
                  <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center text-white text-xl mr-4 group-hover:scale-110 transition-transform">
                    🔒
                  </div>
                  <div>
                    <h4 className="text-xl font-semibold text-slate-900 mb-2">Secure & Private</h4>
                    <p className="text-slate-600 leading-relaxed">Your data is protected with industry-standard security measures and privacy protocols.</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-3xl p-8 shadow-2xl border border-purple-100">
              <h3 className="text-2xl font-bold text-slate-900 mb-6 text-center">Ideal For:</h3>
              
              <div className="space-y-4">
                <div className="flex items-center p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl hover:shadow-lg transition-all duration-300">
                  <div className="w-3 h-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full mr-4"></div>
                  <span className="text-slate-700 font-medium">Students preparing for presentations</span>
                </div>
                <div className="flex items-center p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl hover:shadow-lg transition-all duration-300">
                  <div className="w-3 h-3 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full mr-4"></div>
                  <span className="text-slate-700 font-medium">Job seekers practicing interviews</span>
                </div>
                <div className="flex items-center p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl hover:shadow-lg transition-all duration-300">
                  <div className="w-3 h-3 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full mr-4"></div>
                  <span className="text-slate-700 font-medium">Public speakers and presenters</span>
                </div>
                <div className="flex items-center p-4 bg-gradient-to-r from-orange-50 to-red-50 rounded-2xl hover:shadow-lg transition-all duration-300">
                  <div className="w-3 h-3 bg-gradient-to-r from-orange-500 to-red-500 rounded-full mr-4"></div>
                  <span className="text-slate-700 font-medium">Professionals improving communication</span>
                </div>
                <div className="flex items-center p-4 bg-gradient-to-r from-yellow-50 to-amber-50 rounded-2xl hover:shadow-lg transition-all duration-300">
                  <div className="w-3 h-3 bg-gradient-to-r from-yellow-500 to-amber-500 rounded-full mr-4"></div>
                  <span className="text-slate-700 font-medium">Language learners</span>
                </div>
                <div className="flex items-center p-4 bg-gradient-to-r from-teal-50 to-cyan-50 rounded-2xl hover:shadow-lg transition-all duration-300">
                  <div className="w-3 h-3 bg-gradient-to-r from-teal-500 to-cyan-500 rounded-full mr-4"></div>
                  <span className="text-slate-700 font-medium">Anyone looking to improve speaking skills</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Demo Section */}
      <section id="demo" className="py-12 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-purple-100 text-purple-700 text-sm font-medium mb-6">
              <span className="mr-2">🎬</span>
              Try It Out
            </div>
            <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-6">
              Experience
              <span className="block text-purple-600">Speech Analysis</span>
            </h2>
            <p className="text-xl text-slate-600 max-w-3xl mx-auto">
              Try our speech analysis system and see how it can help improve your communication skills.
            </p>
          </div>
          
          {/* Interactive Demo */}
          <InteractiveDemo />

          <div className="grid md:grid-cols-3 gap-8 mt-8">
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-purple-100 hover:shadow-2xl hover:scale-105 transition-all duration-300">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center text-2xl text-white mb-6">
                📤
              </div>
              <h4 className="text-xl font-bold text-slate-900 mb-3">1. Record or Upload</h4>
              <p className="text-slate-600 leading-relaxed">Record directly in your browser or upload professional presentations, interview responses, or practice sessions in any audio format.</p>
            </div>
            
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-blue-100 hover:shadow-2xl hover:scale-105 transition-all duration-300">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-500 rounded-2xl flex items-center justify-center text-2xl text-white mb-6">
                🔍
              </div>
              <h4 className="text-xl font-bold text-slate-900 mb-3">2. AI Analysis</h4>
              <p className="text-slate-600 leading-relaxed">Our AI processes your speech and analyzes various aspects including pace, clarity, emotions, and content quality.</p>
            </div>
            
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-green-100 hover:shadow-2xl hover:scale-105 transition-all duration-300">
              <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center text-2xl text-white mb-6">
                📋
              </div>
              <h4 className="text-xl font-bold text-slate-900 mb-3">3. Get Feedback</h4>
              <p className="text-slate-600 leading-relaxed">Receive detailed insights and personalized recommendations to help you improve your communication skills.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-12 px-4 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
        <div className="relative max-w-6xl mx-auto text-center">
          <div className="mb-8">
            <span className="inline-flex items-center px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm text-white/90 text-sm font-medium border border-white/20">
              <span className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></span>
              Ready to Transform Your Speaking?
            </span>
          </div>
          
          <h2 className="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">
            Start Your Journey to
            <span className="block bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
              Better Communication
            </span>
          </h2>
          
          <p className="text-xl md:text-2xl text-white/80 mb-8 max-w-4xl mx-auto leading-relaxed">
            Improve your speaking skills with AI-powered analysis and personalized feedback.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-8">
            <Link 
              to="/auth" 
              className="group bg-gradient-to-r from-purple-600 to-pink-600 text-white px-10 py-5 rounded-2xl text-xl font-semibold hover:from-purple-700 hover:to-pink-700 hover:scale-105 hover:shadow-2xl transition-all duration-300 flex items-center"
            >
              <span className="mr-3">🚀</span>
              Start Analysis
              <svg className="w-6 h-6 ml-3 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 bg-slate-900">
        <div className="max-w-7xl mx-auto">
          <div className="bg-white/5 backdrop-blur-sm rounded-3xl p-8 border border-white/10">
            <div className="text-center">
              <div className="flex items-center justify-center mb-6">
                <span className="text-3xl mr-3">🎤</span>
                <span className="text-2xl font-bold text-white">SpeechAnalyzer</span>
              </div>
              
              <p className="text-white/70 mb-6 max-w-2xl mx-auto">
                AI-powered speech analysis and communication training platform.
              </p>
              
              <div className="flex flex-wrap justify-center gap-6 mb-8 text-white/60">
                <button onClick={() => scrollToSection('features')} className="hover:text-white transition-colors">Features</button>
                <button onClick={() => scrollToSection('about')} className="hover:text-white transition-colors">About</button>
                <button onClick={() => scrollToSection('demo')} className="hover:text-white transition-colors">Demo</button>
                <Link to="/auth" className="hover:text-white transition-colors">Get Started</Link>
              </div>
              
              <div className="border-t border-white/10 pt-6">
                <div className="text-white/50 text-sm">
                  © 2025 SpeechAnalyzer. All rights reserved.
                </div>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage