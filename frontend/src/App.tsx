// App.tsx

import type React from 'react';
import './index.css';
import { Routes, Route } from 'react-router-dom';
import Faq from './pages/Faq';
import Index from './pages/Index';
import Auth from './pages/Login';
import Nav from './pages/components/Nav';
import Chat from './pages/components/Chat';

const App: React.FC = () => {
  return (
    <div>
      <Nav />
      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/faq" element={<Faq />} />
        <Route path="/login" element={<Auth />} />
      </Routes>
      <Chat />
    </div>
  );
};

export default App;
