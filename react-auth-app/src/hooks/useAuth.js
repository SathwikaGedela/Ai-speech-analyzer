import { useState, useEffect } from 'react'

export const useAuth = () => {
  const [currentUser, setCurrentUser] = useState(null)
  const [users, setUsers] = useState([])

  useEffect(() => {
    // Load users and current user from localStorage
    const storedUsers = JSON.parse(localStorage.getItem('users') || '[]')
    const storedCurrentUser = JSON.parse(localStorage.getItem('currentUser') || 'null')
    
    setUsers(storedUsers)
    setCurrentUser(storedCurrentUser)
  }, [])

  const signup = (userData) => {
    const newUser = {
      ...userData,
      id: Date.now(),
      joinDate: new Date().toLocaleDateString()
    }
    
    const updatedUsers = [...users, newUser]
    setUsers(updatedUsers)
    localStorage.setItem('users', JSON.stringify(updatedUsers))
    
    return newUser
  }

  const login = (credentials) => {
    const user = users.find(u => 
      u.email === credentials.email && u.password === credentials.password
    )
    
    if (user) {
      setCurrentUser(user)
      localStorage.setItem('currentUser', JSON.stringify(user))
      return user
    }
    
    return null
  }

  const logout = () => {
    setCurrentUser(null)
    localStorage.removeItem('currentUser')
  }

  const isEmailTaken = (email) => {
    return users.some(user => user.email === email.toLowerCase())
  }

  return {
    currentUser,
    users,
    signup,
    login,
    logout,
    isEmailTaken
  }
}