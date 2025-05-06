import { Routes, Route, Link } from 'react-router-dom';
import Faq from './pages/Faq';

function Home() {
  return <h1>Hello, World!</h1>;
}

export default function App() {
  return (
    <div style={{ padding: '1rem' }}>
      <nav style={{ marginBottom: '1rem' }}>
        <Link to="/">Home</Link> |{' '}
        <Link to="/faq">FAQ</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/faq" element={<Faq />} />
      </Routes>
    </div>
  );
}
