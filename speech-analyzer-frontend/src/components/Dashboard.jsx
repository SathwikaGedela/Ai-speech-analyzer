import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import Navigation from './Navigation'
import PageWrapper from './PageWrapper'
import SectionWrapper from './SectionWrapper'
import { WelcomeHeader } from './HeaderVariants'

const Dashboard = () => {
  const { user } = useAuth()

  return (
    <PageWrapper className="min-h-screen">
      <Navigation />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Enhanced Header */}
        <SectionWrapper index={0}>
          <WelcomeHeader user={user} className="mb-6" />
        </SectionWrapper>

        {/* Quick Actions */}
        <SectionWrapper index={1}>
          <div className="glass-card rounded-3xl p-6 mb-6 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">Speech Analysis Tools</h2>
            
            <div className="grid md:grid-cols-3 gap-4">
              <Link 
                to="/analysis" 
                className="block p-6 bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl border-2 border-blue-200 hover:border-blue-300 hover:shadow-lg hover:-translate-y-1 hover:scale-[1.01] transition-all duration-300 ease-out active:scale-[0.99] active:translate-y-0 group"
              >
                <div className="text-blue-600 text-2xl mb-2 group-hover:scale-110 transition-transform duration-200">🎤</div>
                <h3 className="font-semibold text-gray-800 mb-2 group-hover:text-blue-700 transition-colors">Audio Analysis</h3>
                <p className="text-gray-600 text-sm">Upload or record your speech for detailed analysis</p>
              </Link>
              
              <Link 
                to="/interview" 
                className="block p-6 bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl border-2 border-purple-200 hover:border-purple-300 hover:shadow-lg hover:-translate-y-1 hover:scale-[1.01] transition-all duration-300 ease-out active:scale-[0.99] active:translate-y-0 group"
              >
                <div className="text-purple-600 text-2xl mb-2 group-hover:scale-110 transition-transform duration-200">💼</div>
                <h3 className="font-semibold text-gray-800 mb-2 group-hover:text-purple-700 transition-colors">Interview Mode</h3>
                <p className="text-gray-600 text-sm">Practice interviews with AI-powered feedback</p>
              </Link>
              
              <Link 
                to="/history" 
                className="block p-6 bg-gradient-to-br from-green-50 to-green-100 rounded-xl border-2 border-green-200 hover:border-green-300 hover:shadow-lg hover:-translate-y-1 hover:scale-[1.01] transition-all duration-300 ease-out active:scale-[0.99] active:translate-y-0 group"
              >
                <div className="text-green-600 text-2xl mb-2 group-hover:scale-110 transition-transform duration-200">📊</div>
                <h3 className="font-semibold text-gray-800 mb-2 group-hover:text-green-700 transition-colors">History & Progress</h3>
                <p className="text-gray-600 text-sm">View your analysis history and track progress</p>
              </Link>
            </div>
          </div>
        </SectionWrapper>

        {/* Features Overview */}
        <SectionWrapper index={2}>
          <div className="glass-card rounded-3xl p-6 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">Platform Features</h2>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="p-4 bg-gradient-to-br from-indigo-50 to-indigo-100 rounded-xl text-center hover:shadow-md hover:-translate-y-0.5 hover:scale-[1.01] hover:bg-indigo-25 transition-all duration-250 ease-out cursor-pointer group">
                <div className="text-2xl mb-2 group-hover:scale-110 transition-transform duration-200">🎯</div>
                <div className="text-sm font-semibold text-indigo-800 group-hover:text-indigo-900 transition-colors">Speech Analysis</div>
                <div className="text-xs text-gray-600 mt-1">Detailed metrics & insights</div>
              </div>
              <div className="p-4 bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl text-center hover:shadow-md hover:-translate-y-0.5 hover:scale-[1.01] hover:bg-purple-25 transition-all duration-250 ease-out cursor-pointer group">
                <div className="text-2xl mb-2 group-hover:scale-110 transition-transform duration-200">🧠</div>
                <div className="text-sm font-semibold text-purple-800 group-hover:text-purple-900 transition-colors">AI Feedback</div>
                <div className="text-xs text-gray-600 mt-1">Intelligent recommendations</div>
              </div>
              <div className="p-4 bg-gradient-to-br from-pink-50 to-pink-100 rounded-xl text-center hover:shadow-md hover:-translate-y-0.5 hover:scale-[1.01] hover:bg-pink-25 transition-all duration-250 ease-out cursor-pointer group">
                <div className="text-2xl mb-2 group-hover:scale-110 transition-transform duration-200">⚡</div>
                <div className="text-sm font-semibold text-pink-800 group-hover:text-pink-900 transition-colors">Real-time Processing</div>
                <div className="text-xs text-gray-600 mt-1">5ms analysis speed</div>
              </div>
              <div className="p-4 bg-gradient-to-br from-green-50 to-green-100 rounded-xl text-center hover:shadow-md hover:-translate-y-0.5 hover:scale-[1.01] hover:bg-green-25 transition-all duration-250 ease-out cursor-pointer group">
                <div className="text-2xl mb-2 group-hover:scale-110 transition-transform duration-200">📈</div>
                <div className="text-sm font-semibold text-green-800 group-hover:text-green-900 transition-colors">Progress Tracking</div>
                <div className="text-xs text-gray-600 mt-1">Monitor improvement</div>
              </div>
            </div>
          </div>
        </SectionWrapper>
      </div>
    </PageWrapper>
  )
}

export default Dashboard