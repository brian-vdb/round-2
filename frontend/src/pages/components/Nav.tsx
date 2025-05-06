// components/Nav.tsx

import React from 'react'
import './Nav.css'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

const Nav: React.FC = () => {
  const { user, signOut } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async (e: React.MouseEvent) => {
    e.preventDefault()
    await signOut()
    navigate('/')
  }

  return (
    <nav className="nav">
      <div className="nav-center">
        <Link to="/" draggable={false}>Home</Link>
        <Link to="/faq" draggable={false}>FAQ</Link>
      </div>
      <div className="nav-right">
        {!user ? (
          <Link to="/login" draggable={false}>Login</Link>
        ) : (
          <a href="#" onClick={handleLogout}>Logout</a>
        )}
      </div>
    </nav>
  )
}

export default Nav
