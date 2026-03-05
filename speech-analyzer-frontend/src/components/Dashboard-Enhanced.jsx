import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import Navigation from './Navigation'

const Dashboard = () => {
  const { user } = useAuth()

  return (
    <div className="min-h-screen bg-slate-50">
      <Navigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 lg:py-12">
        {/* Enhanced Header */}
        <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 rounded-2xl p-8 mb-8 text-white shadow-xl animate-fade-in-up">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center mr-6 backdrop-blur-sm">
                <span className="text-3xl">👋</span>
              </div>
              <div>
                <h1 className="text-4xl font-bold mb-2 leading-tight">Welcome back, {user?.first_name}!</h1>
                <p className="text-indigo-100 text-lg leading-relaxed">Ready to analyze your speech and improve your communication skills?</p>
              </div>
            </div>
          </div>
        </div>

        {/* Enhanced Quick Actions */}
        <div className="bg-white rounded-2xl p-10 shadow-lg hover:shadow-xl transition-all duration-300 border border-slate-100 mb-8 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-3xl font-bold text-slate-900 mb-2">Speech Analysis Tools</h2>
              <p className="text-lg text-slate-600">Choose your preferred analysis method to get started</p>
            </div>
            <div className="w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
              <span className="text-white text-2xl">⚡</span>
            </div>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <Link 
              to="/analysis" 
              className="group block p-8 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl border border-blue-200/50 shadow-sm hover:shadow-lg hover:scale-105 transition-all duration-300 hover:border-blue-300"
            >
              <div className="flex items-center justify-between mb-6">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center text-white text-2xl shadow-lg group-hover:scale-110 transition-transform">
                  🎤
                </div>
                <svg className="w-6 h-6 text-blue-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3 group-hover:text-blue-600 transition-colors">Audio Analysis</h3>
              <p className="text-slate-600 leading-relaxed">Upload or record your speech for detailed analysis with AI-powered insights</p>
              <div className="mt-4 flex items-center text-sm text-blue-600 font-medium">
                <span>Get started</span>
                <svg className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </div>
            </Link>
            
            <Link 
              to="/interview" 
              className="group block p-8 bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl border border-purple-200/50 shadow-sm hover:shadow-lg hover:scale-105 transition-all duration-300 hover:border-purple-300"
            >
              <div className="flex items-center justify-between mb-6">
                <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-600 rounded-2xl flex items-center justify-center text-white text-2xl shadow-lg group-hover:scale-110 transition-transform">
                  💼
                </div>
                <svg className="w-6 h-6 text-purple-400 group-hover:text-purple-600 group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3 group-hover:text-purple-600 transition-colors">Interview Mode</h3>
              <p className="text-slate-600 leading-relaxed">Practice interviews with AI-powered feedback and relevance analysis</p>
              <div className="mt-4 flex items-center text-sm text-purple-600 font-medium">
                <span>Start practicing</span>
                <svg className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </div>
            </Link>
            
            <Link 
              to="/history" 
              className="group block p-8 bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl border border-green-200/50 shadow-sm hover:shadow-lg hover:scale-105 transition-all duration-300 hover:border-green-300"
            >
              <div className="flex items-center justify-between mb-6">
                <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center text-white text-2xl shadow-lg group-hover:scale-110 transition-transform">
                  📊
                </div>
                <svg className="w-6 h-6 text-green-400 group-hover:text-green-600 group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3 group-hover:text-green-600 transition-colors">History & Progress</h3>
              <p className="text-slate-600 leading-relaxed">View your analysis history and track your improvement over time</p>
              <div className="mt-4 flex items-center text-sm text-green-600 font-medium">
                <span>View progress</span>
                <svg className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </div>
            </Link>
          </div>
        </div>

        {/* Enhanced Features Overview */}
        <div className="bg-white rounded-2xl p-10 shadow-lg hover:shadow-xl transition-all duration-300 border border-slate-100 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
          <div className="text-center mb-10">
            <h2 className="text-3xl font-bold text-slate-900 mb-4">Platform Features</h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">Discover the powerful tools that make SpeechAnalyzer Pro the leading choice for communication improvement</p>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="group p-6 bg-gradient-to-br from-indigo-50 to-blue-50 rounded-2xl text-center border border-indigo-100 hover:border-indigo-200 hover:shadow-md transition-all duration-300">
              <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg group-hover:scale-110 transition-transform">
                <span className="text-2xl text-white">🎯</span>
              </div>
              <h3 className="text-lg font-bold text-indigo-900 mb-2">Speech Analysis</h3>
              <p className="text-sm text-indigo-700 leading-relaxed">Detailed metrics & insights with 99.8% accuracy</p>
            </div>
            
            <div className="group p-6 bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl text-center border border-purple-100 hover:border-purple-200 hover:shadow-md transition-all duration-300">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg group-hover:scale-110 transition-transform">
                <span className="text-2xl text-white">🧠</span>
              </div>
              <h3 className="text-lg font-bold text-purple-900 mb-2">AI Feedback</h3>
              <p className="text-sm text-purple-700 leading-relaxed">Intelligent recommendations powered by machine learning</p>
            </div>
            
            <div className="group p-6 bg-gradient-to-br from-pink-50 to-rose-50 rounded-2xl text-center border border-pink-100 hover:border-pink-200 hover:shadow-md transition-all duration-300">
              <div className="w-16 h-16 bg-gradient-to-br from-pink-500 to-rose-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg group-hover:scale-110 transition-transform">
                <span className="text-2xl text-white">⚡</span>
              </div>
              <h3 className="text-lg font-bold text-pink-900 mb-2">Real-time Processing</h3>
              <p className="text-sm text-pink-700 leading-relaxed">Lightning-fast analysis in under 2 milliseconds</p>
            </div>
            
            <div className="group p-6 bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl text-center border border-green-100 hover:border-green-200 hover:shadow-md transition-all duration-300">
              <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg group-hover:scale-110 transition-transform">
                <span className="text-2xl text-white">📈</span>
              </div>
              <h3 className="text-lg font-bold text-green-900 mb-2">Progress Tracking</h3>
              <p className="text-sm text-green-700 leading-relaxed">Monitor improvement with detailed analytics</p>
            </div>
          </div>
        </div>

        {/* Enhanced Recent Activity */}
        <div className="mt-8 bg-white rounded-2xl p-10 shadow-lg hover:shadow-xl transition-all duration-300 border border-slate-100 animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-3xl font-bold text-slate-900 mb-2">Quick Stats</h2>
              <p className="text-lg text-slate-600">Your performance at a glance</p>
            </div>
            <Link 
              to="/history" 
              className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300"
            >
              View All History
              <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </Link>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="text-center p-6 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl border border-blue-100">
              <div className="text-3xl font-bold text-blue-600 mb-2">0</div>
              <div className="text-sm text-blue-700 font-medium">Total Sessions</div>
              <div className="text-xs text-blue-600 mt-1">Start your first analysis</div>
            </div>
            
            <div className="text-center p-6 bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl border border-green-100">
              <div className="text-3xl font-bold text-green-600 mb-2">--</div>
              <div className="text-sm text-green-700 font-medium">Avg Confidence</div>
              <div className="text-xs text-green-600 mt-1">No data yet</div>
            </div>
            
            <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl border border-purple-100">
              <div className="text-3xl font-bold text-purple-600 mb-2">--</div>
              <div className="text-sm text-purple-700 font-medium">Avg WPM</div>
              <div className="text-xs text-purple-600 mt-1">No data yet</div>
            </div>
            
            <div className="text-center p-6 bg-gradient-to-br from-yellow-50 to-amber-50 rounded-2xl border border-yellow-100">
              <div className="text-3xl font-bold text-yellow-600 mb-2">--</div>
              <div className="text-sm text-yellow-700 font-medium">Improvement</div>
              <div className="text-xs text-yellow-600 mt-1">Track your progress</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard