// components/Nav.tsx

import type React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Nav: React.FC = () => {
  const { user } = useAuth();

  return (
    <nav className="nav">
      <Link to="/">Home</Link> |{' '}
      <Link to="/faq">FAQ</Link>
      {!user && (
        <> | <Link to="/login">Login</Link></>
      )}
    </nav>
  );
};

export default Nav;
