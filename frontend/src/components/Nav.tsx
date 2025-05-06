// components/Nav.tsx

import type React from 'react';
import { Link } from 'react-router-dom';

const Nav: React.FC = () => {
  return (
    <nav className="nav">
      <Link to="/">Home</Link> |{' '}
      <Link to="/login">Login</Link> |{' '}
      <Link to="/faq">FAQ</Link>
    </nav>
  );
};

export default Nav;
