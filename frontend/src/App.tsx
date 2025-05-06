import React from 'react';
import './index.css';
import { Routes, Route, useLocation } from 'react-router-dom';
import Faq from './pages/Faq';
import Index from './pages/Index';
import Auth from './pages/Login';
import Nav from './pages/components/Nav';
import Chat from './pages/components/Chat';

const App: React.FC = () => {
  const location = useLocation();
  const isAuthRoute = location.pathname === '/login';

  return (
    <div>
      {!isAuthRoute && <Nav />}

      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/faq" element={<Faq />} />
        <Route path="/login" element={<Auth />} />
      </Routes>

      {!isAuthRoute && <Chat />}
    </div>
  );
};

export default App;