// context/AuthContext.tsx

import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';

interface User {
  id: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  signIn: (username: string, _password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

// Create context without default to enforce provider usage
const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  // On mount, restore session
  useEffect(() => {
    // TODO: implement session restoration
  }, []);

  const signIn = async (username: string, _password: string) => {
    // TODO: implement sign-in logic
    return new Promise<void>((resolve) => {
      // simulate setting user
      setUser({ id: '1', name: username });
      resolve();
    });
  };

  const signOut = async () => {
    // TODO: implement sign-out logic
    return new Promise<void>((resolve) => {
      setUser(null);
      resolve();
    });
  };

  return (
    <AuthContext.Provider value={{ user, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}

export default AuthContext;
