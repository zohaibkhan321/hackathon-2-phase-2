'use client';

import React from 'react';
import { useAuth } from '../../components/AuthProvider';
import { useRouter } from 'next/navigation';

const DashboardLayout = ({ children }: { children: React.ReactNode }) => {
  const { user, logout, isAuthenticated } = useAuth();
  const router = useRouter();

  if (!isAuthenticated) {
    router.push('/login');
    return null;
  }

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">Todo App</h1>
            </div>
            <div className="flex items-center">
              <div className="ml-3 relative">
                <div className="flex items-center space-x-4">
                  <span className="text-sm text-gray-700">Welcome, {user?.email}</span>
                  <button
                    onClick={handleLogout}
                    className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
                  >
                    Logout
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          {children}
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;