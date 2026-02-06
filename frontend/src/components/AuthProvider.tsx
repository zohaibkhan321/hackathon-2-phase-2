'use client';

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from 'react';
import { apiClient } from '../lib/api';

interface User {
  id: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Restore session on refresh
  useEffect(() => {
    const token = localStorage.getItem('jwt_token');
    const storedUser = localStorage.getItem('currentUser');

    if (token && storedUser) {
      setUser(JSON.parse(storedUser));
    }

    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    const response = await apiClient.login(email, password);

    localStorage.setItem('jwt_token', response.access_token);
    localStorage.setItem('currentUser', JSON.stringify(response.user));

    setUser(response.user);
  };

  const register = async (email: string, password: string) => {
    const response = await apiClient.register(email, password);

    localStorage.setItem('jwt_token', response.access_token);
    localStorage.setItem('currentUser', JSON.stringify(response.user));

    setUser(response.user);
  };

  const logout = () => {
    localStorage.removeItem('jwt_token');
    localStorage.removeItem('currentUser');
    setUser(null);
    window.location.href = '/login';
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        register,
        logout,
        isAuthenticated: !!user,
        loading,
      }}
    >
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
