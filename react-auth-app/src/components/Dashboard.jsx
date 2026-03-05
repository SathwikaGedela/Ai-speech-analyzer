import { useState } from 'react'

const Dashboard = ({ user, onLogout }) => {
  const [isLoggingOut, setIsLoggingOut] = useState(false)

  const handleLogout = () => {
    setIsLoggingOut(true)
    
    setTimeout(() => {
      onLogout()
      setIsLoggingOut(false)
    }, 400)
  }

  return (
    <div className={`glass-card overflow-hidden min-h-[500px] ${isLoggingOut ? 'animate-slide-out' : ''}`}>
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white p-6">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-xl font-bold">Welcome, {user.firstName}!</h3>
            <p className="text-indigo-100 text-sm">{user.email}</p>
          </div>
          <button
            onClick={handleLogout}
            className="bg-white/20 hover:bg-white/30 border border-white/30 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 hover:-translate-y-0.5"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-6">User Details</h3>
        
        <div className="space-y-4">
          <DetailItem 
            label="Full Name" 
            value={`${user.firstName} ${user.lastName}`} 
          />
          <DetailItem 
            label="Email" 
            value={user.email} 
          />
          <DetailItem 
            label="Phone" 
            value={user.phone} 
          />
          <DetailItem 
            label="Member Since" 
            value={user.joinDate} 
          />
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 gap-4 mt-8">
          <StatCard 
            title="Account Status" 
            value="Active" 
            color="green" 
          />
          <StatCard 
            title="Profile" 
            value="Complete" 
            color="blue" 
          />
        </div>
      </div>
    </div>
  )
}

const DetailItem = ({ label, value }) => (
  <div className="flex justify-between items-center p-4 bg-gray-50 rounded-xl border-l-4 border-indigo-500 hover:bg-gray-100 transition-colors duration-300">
    <span className="font-semibold text-gray-700">{label}:</span>
    <span className="text-gray-900">{value}</span>
  </div>
)

const StatCard = ({ title, value, color }) => {
  const colorClasses = {
    green: 'bg-green-50 text-green-700 border-green-200',
    blue: 'bg-blue-50 text-blue-700 border-blue-200',
  }

  return (
    <div className={`p-4 rounded-xl border-2 ${colorClasses[color]} text-center hover:scale-105 transition-transform duration-300`}>
      <div className="text-sm font-medium opacity-75">{title}</div>
      <div className="text-lg font-bold">{value}</div>
    </div>
  )
}

export default Dashboard