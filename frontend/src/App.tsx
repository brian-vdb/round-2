// Auth.tsx

import { Routes, Route, Link } from 'react-router-dom';
import Faq from './pages/Faq';
import Index from './pages/Index';
import type React from 'react';

const App: React.FC = () => {
  return (
    <div>
      <nav>
        <Link to="/">Home</Link> |{' '}
        <Link to="/faq">FAQ</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/faq" element={<Faq />} />
      </Routes>
    </div>
  );
}

export default App;
