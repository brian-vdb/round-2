// pages/Index.tsx

import type React from 'react';
import './Index.css';
import { useAuth } from '../context/AuthContext';

const Index: React.FC = () => {
  // Validate the user
  const { user } = useAuth();
  if (!user) {
    return (
      <div>
        <h1>Please Login</h1>
        {/* Add login form here and call signIn */}
      </div>
    );
  }

  return <h1>Hello, World!</h1>;
}

export default Index;
