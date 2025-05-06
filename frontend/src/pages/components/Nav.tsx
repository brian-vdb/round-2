// components/Nav.tsx

import React from 'react'
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
      <Link to="/">Home</Link> |{' '}
      <Link to="/faq">FAQ</Link>
      {!user && (
        <> | <Link to="/login">Login</Link></>
      )}
      {user && (
        <> | <a href="#" onClick={handleLogout}>Logout</a></>
      )}
    </nav>
  )
}

export default Nav
