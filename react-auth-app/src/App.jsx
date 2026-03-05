import { useState, useEffect } from 'react'
import SignupForm from './components/SignupForm'
import SigninForm from './components/SigninForm'
import Dashboard from './components/Dashboard'
import { useAuth } from './hooks/useAuth'

function App() {
  const [currentView, setCurrentView] = useState('signup')
  const { currentUser, login, logout, signup } = useAuth()

  useEffect(() => {
    if (currentUser) {
      setCurrentView('dashboard')
    }
  }, [currentUser])

  const handleSignupSuccess = (userData) => {
    signup(userData)
    setCurrentView('signin')
  }

  const handleSigninSuccess = (userData) => {
    login(userData)
    setCurrentView('dashboard')
  }

  const handleLogout = () => {
    logout()
    setCurrentView('signup')
  }

  const switchToSignin = () => setCurrentView('signin')
  const switchToSignup = () => setCurrentView('signup')

  return (
    <div className="min-h-screen flex items-center justify-center p-4 overflow-hidden">
      <div className="w-full max-w-md relative">
        {currentView === 'signup' && (
          <div className="animate-bounce-in">
            <SignupForm 
              onSuccess={handleSignupSuccess}
              onSwitchToSignin={switchToSignin}
            />
          </div>
        )}
        
        {currentView === 'signin' && (
          <div className="animate-bounce-in">
            <SigninForm 
              onSuccess={handleSigninSuccess}
              onSwitchToSignup={switchToSignup}
            />
          </div>
        )}
        
        {currentView === 'dashboard' && (
          <div className="animate-bounce-in">
            <Dashboard 
              user={currentUser}
              onLogout={handleLogout}
            />
          </div>
        )}
      </div>
    </div>
  )
}

export default App