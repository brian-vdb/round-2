// pages/Login.tsx

import type React from 'react';
import './Login.css';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const { signIn } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await signIn(username, password);
      navigate('/');
    } catch (err) {
      console.error(err);
      setError('Failed to log in. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="page login-page">
      <h1>Login Panel</h1>
      <form onSubmit={handleSubmit} className="login-form">
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit" disabled={loading} className="btn">
          {loading ? 'Logging in...' : 'Login'}
        </button>

        {error && <p className="error-message">{error}</p>}
      </form>
    </main>
  );
};

export default Login;
