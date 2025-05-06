import { Routes, Route, Link } from 'react-router-dom';
import Faq from './pages/Faq';
import Index from './pages/Index';
import type React from 'react';

const App: React.FC = () => {
  return (
    <div style={{ padding: '1rem' }}>
      <nav style={{ marginBottom: '1rem' }}>
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
