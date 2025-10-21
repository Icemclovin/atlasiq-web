import apiClient from './api';
import type {
  LoginCredentials,
  RegisterData,
  AuthResponse,
  User,
} from '@/types';

export const authService = {
  /**
   * Register a new user
   */
  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await apiClient.getClient().post<AuthResponse>('/api/v1/auth/register', data);
    
    // Save tokens
    apiClient.setTokens(response.data.access_token, response.data.refresh_token);
    
    return response.data;
  },

  /**
   * Login with email and password
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await apiClient.getClient().post<AuthResponse>('/api/v1/auth/login', credentials);
    
    // Save tokens
    apiClient.setTokens(response.data.access_token, response.data.refresh_token);
    
    return response.data;
  },

  /**
   * Get current user profile
   */
  async getCurrentUser(): Promise<User> {
    const response = await apiClient.getClient().get<User>('/api/v1/auth/me');
    return response.data;
  },

  /**
   * Logout - clear tokens
   */
  logout(): void {
    apiClient.clearTokens();
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return apiClient.isAuthenticated();
  },

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<string> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await apiClient.getClient().post<{ access_token: string }>('/api/v1/auth/refresh', {
      refresh_token: refreshToken,
    });

    apiClient.setAccessToken(response.data.access_token);
    return response.data.access_token;
  },
};
