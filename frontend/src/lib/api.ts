// lib/api.ts

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? 'https://hackathon-2-phase-2-orpin.vercel.app/api';

/* ================================
   Types
================================ */
export interface ApiError {
  message: string;
  status?: number;
}

export interface AuthResponse {
  access_token: string;
  user: {
    id: string;
    email: string;
  };
}

/* ================================
   Api Client
================================ */
class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private getToken() {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('jwt_token');
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getToken();

    const res = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
    });

    if (!res.ok) {
      if (res.status === 401 && typeof window !== 'undefined') {
        localStorage.removeItem('jwt_token');
        localStorage.removeItem('currentUser');
        window.location.href = '/login';
      }

      let errorMessage = 'Something went wrong';
      try {
        const data = await res.json();
        errorMessage = data.detail || data.message || errorMessage;
      } catch {
        /* ignore */
      }

      throw {
        message: errorMessage,
        status: res.status,
      } as ApiError;
    }

    return res.json();
  }

  /* ================================
     AUTH
  ================================ */
  login(email: string, password: string) {
    return this.request<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  register(email: string, password: string) {
    return this.request<AuthResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  /* ================================
     TASKS
  ================================ */
  getTasks() {
    return this.request('/tasks');
  }

  createTask(title: string, description?: string) {
    return this.request('/tasks', {
      method: 'POST',
      body: JSON.stringify({ title, description }),
    });
  }

  updateTask(
    id: string,
    payload: {
      title?: string;
      description?: string;
      completed?: boolean;
    }
  ) {
    return this.request(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    });
  }

  deleteTask(id: string) {
    return this.request(`/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  toggleTaskCompletion(id: string, completed: boolean) {
    return this.request(`/tasks/${id}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ completed }),
    });
  }

  chat(userId: string, message: string) {
    return this.request(`/${userId}/chat`, {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }
}

/* ================================
   Export Singleton
================================ */
export const apiClient = new ApiClient(API_BASE_URL);
