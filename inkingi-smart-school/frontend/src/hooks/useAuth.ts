import { useMutation, useQuery } from '@tanstack/react-query';
import { useAuthStore } from '../stores/authStore';
import { api } from '../lib/api';
import type { LoginRequest, Token, User } from '../types/api';
import { toast } from 'sonner';

// Auth API functions
const authApi = {
  login: async (credentials: LoginRequest): Promise<Token> => {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  getMe: async (): Promise<User> => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  refreshToken: async (): Promise<Token> => {
    const response = await api.post('/auth/refresh');
    return response.data;
  },
};

// Hooks
export const useLogin = () => {
  const { login: setAuth, setLoading } = useAuthStore();

  return useMutation({
    mutationFn: authApi.login,
    onMutate: () => {
      setLoading(true);
    },
    onSuccess: async (tokenData) => {
      try {
        // Get user data after successful login
        localStorage.setItem('access_token', tokenData.access_token);
        const userData = await authApi.getMe();
        setAuth(userData, tokenData.access_token);
        toast.success('Login successful!');
      } catch (error) {
        console.error('Failed to get user data:', error);
        toast.error('Login failed. Please try again.');
      }
    },
    onError: (error: any) => {
      console.error('Login error:', error);
      const message = error?.response?.data?.detail || 'Login failed. Please check your credentials.';
      toast.error(message);
    },
    onSettled: () => {
      setLoading(false);
    },
  });
};

export const useLogout = () => {
  const { logout } = useAuthStore();

  return () => {
    logout();
    toast.success('Logged out successfully');
  };
};

export const useCurrentUser = () => {
  const { isAuthenticated } = useAuthStore();

  return useQuery({
    queryKey: ['currentUser'],
    queryFn: authApi.getMe,
    enabled: isAuthenticated && !!localStorage.getItem('access_token'),
    staleTime: 1000 * 60 * 30, // 30 minutes
    retry: false,
  });
};

export const useRefreshToken = () => {
  return useMutation({
    mutationFn: authApi.refreshToken,
    onSuccess: (tokenData) => {
      localStorage.setItem('access_token', tokenData.access_token);
    },
    onError: () => {
      // Refresh failed, logout user
      const { logout } = useAuthStore.getState();
      logout();
    },
  });
};