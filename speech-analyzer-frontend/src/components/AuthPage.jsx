import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import SignupForm from './SignupForm'
import SigninForm from './SigninForm'

const AuthPage = () => {
  const [currentView, setCurrentView] = useState('signup')
  const [signupEmail, setSignupEmail] = useState('')
  const [showSuccessMessage, setShowSuccessMessage] = useState(false)
  const navigate = useNavigate()
  const { signin, signup } = useAuth()

  const handleSignupSuccess = async (userData) => {
    const result = await signup(userData)
    if (result.success) {
      // Store the email for pre-filling signin form
      setSignupEmail(userData.email)
      setShowSuccessMessage(true)
      setCurrentView('signin')
      
      // Hide success message after 5 seconds
      setTimeout(() => {
        setShowSuccessMessage(false)
      }, 5000)
    }
    return result
  }

  const handleSigninSuccess = async (credentials) => {
    const result = await signin(credentials)
    if (result.success) {
      navigate('/dashboard')
    }
    return result
  }

  const switchToSignin = () => {
    setCurrentView('signin')
    setShowSuccessMessage(false)
  }
  
  const switchToSignup = () => {
    setCurrentView('signup')
    setShowSuccessMessage(false)
    setSignupEmail('')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-pink-500/20 rounded-full blur-3xl"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
      </div>

      <div className="relative z-10 w-full max-w-sm">
        {/* Header */}
        <div className="text-center mb-6">
          <div className="flex items-center justify-center mb-3">
            <span className="text-3xl mr-2">🎤</span>
            <span className="text-2xl font-bold text-white">SpeechAnalyzer Pro</span>
          </div>
          <p className="text-white/70 text-sm">
            {currentView === 'signup' 
              ? 'Create your professional account' 
              : 'Welcome back to your dashboard'
            }
          </p>
        </div>

        {/* Success Message */}
        {showSuccessMessage && (
          <div className="mb-4 bg-green-500/10 backdrop-blur-sm border border-green-500/20 text-green-300 px-4 py-3 rounded-xl text-sm animate-fade-in">
            <div className="flex items-center">
              <div className="text-green-400 mr-2 text-lg">✅</div>
              <div>
                <strong>Account created successfully!</strong>
                <br />
                <span className="text-green-200">Please sign in to access your dashboard.</span>
              </div>
            </div>
          </div>
        )}

        {currentView === 'signup' && (
          <div className="animate-fade-in">
            <SignupForm 
              onSuccess={handleSignupSuccess}
              onSwitchToSignin={switchToSignin}
            />
          </div>
        )}
        
        {currentView === 'signin' && (
          <div className="animate-fade-in">
            <SigninForm 
              onSuccess={handleSigninSuccess}
              onSwitchToSignup={switchToSignup}
              prefillEmail={signupEmail}
            />
          </div>
        )}
      </div>
    </div>
  )
}

export default AuthPage