// context/AuthContext.tsx

import React, { createContext, useContext, useState, useEffect } from 'react'
import type { ReactNode } from 'react'

interface User {
  id: string
  username: string
  email: string
}

interface AuthContextType {
  user: User | null
  signIn: (username: string, password: string) => Promise<void>
  signOut: () => Promise<void>
}

// Create context without default to enforce provider usage
const AuthContext = createContext<AuthContextType | undefined>(undefined)

// --- API calls --------------------------------------------------

const API_BASE = 'http://127.0.0.1:8000/auth'

async function loginRequest(username: string, password: string): Promise<{ access_token: string; token_type: string }> {
  const res = await fetch(`${API_BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || 'Login failed')
  }
  return res.json()
}

async function fetchCurrentUser(token: string): Promise<User> {
  const res = await fetch(`${API_BASE}/validate`, {
    headers: { Authorization: token }
  })
  if (!res.ok) {
    throw new Error('Failed to fetch user')
  }
  return res.json()
}

// --- Provider ----------------------------------------------------

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)

  // On mount, restore session
  useEffect(() => {
    const token = localStorage.getItem('authToken')
    if (token) {
      fetchCurrentUser(token)
        .then(setUser)
        .catch(() => {
          localStorage.removeItem('authToken')
          setUser(null)
        })
    }
  }, [])

  const signIn = async (username: string, password: string) => {
    const { access_token, token_type } = await loginRequest(username, password)
    const authHeader = `${token_type} ${access_token}`
    localStorage.setItem('authToken', authHeader)
    const freshUser = await fetchCurrentUser(authHeader)
    setUser(freshUser)
  }

  const signOut = async () => {
    localStorage.removeItem('authToken')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}

export default AuthContext
