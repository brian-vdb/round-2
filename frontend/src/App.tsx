// App.tsx

import type React from 'react';
import { Routes, Route } from 'react-router-dom';
import Faq from './pages/Faq';
import Index from './pages/Index';
import Auth from './pages/Login';
import Nav from './components/Nav';

const App: React.FC = () => {
  return (
    <div>
      <Nav />
      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/login" element={<Auth />} />
        <Route path="/faq" element={<Faq />} />
      </Routes>
    </div>
  );
};

export default App;
