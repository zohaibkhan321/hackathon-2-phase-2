// Authentication utilities for frontend
export const isAuthenticated = (): boolean => {
  const token = localStorage.getItem('jwt_token');
  return !!token;
};

export const logout = (): void => {
  localStorage.removeItem('jwt_token');
  localStorage.removeItem('currentUser');
};

export const getAuthToken = (): string | null => {
  return localStorage.getItem('jwt_token');
};

export const setAuthToken = (token: string): void => {
  localStorage.setItem('jwt_token', token);
};