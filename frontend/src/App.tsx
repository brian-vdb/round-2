// App.tsx

import type React from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import Faq from './pages/Faq';
import Index from './pages/Index';
import Auth from './pages/Login';

const App: React.FC = () => {
  const location = useLocation();
  const hideNav = location.pathname === '/login';

  return (
    <div>
      {!hideNav && (
        <nav>
          <Link to="/">Home</Link> |{' '}
          <Link to="/login">Login</Link> |{' '}
          <Link to="/faq">FAQ</Link>
        </nav>
      )}
      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/login" element={<Auth />} />
        <Route path="/faq" element={<Faq />} />
      </Routes>
    </div>
  );
};

export default App;
