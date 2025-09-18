import api from './api'
import { useAuthStore } from '@/stores/auth-store'

export interface LoginRequest {
  email: string
  password: string
  schoolSlug?: string
}

export interface RegisterRequest {
  schoolName: string
  schoolSlug: string
  email: string
  password: string
  firstName: string
  lastName: string
  phone?: string
  address: string
  city: string
  country: string
}

export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: {
    id: string
    email: string
    first_name?: string
    last_name?: string
    school_id: string
  }
}

export interface RegisterResponse {
  message: string
  school: {
    id: string
    name: string
    slug: string
    status: string
  }
  user: {
    id: string
    email: string
    first_name?: string
    last_name?: string
  }
}

class AuthService {
  async login(data: LoginRequest): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>('/auth/login', data)
    
    // Store auth data
    const { access_token, refresh_token, user } = response
    useAuthStore.getState().login(
      {
        id: user.id,
        email: user.email,
        firstName: user.first_name,
        lastName: user.last_name,
        schoolId: user.school_id,
      },
      access_token,
      refresh_token
    )
    
    return response
  }

  async register(data: RegisterRequest): Promise<RegisterResponse> {
    return api.post<RegisterResponse>('/auth/register', data)
  }

  async logout(): Promise<void> {
    // Clear local storage
    useAuthStore.getState().logout()
    // Optionally call logout endpoint
    // await api.post('/auth/logout')
  }

  async refreshToken(refreshToken: string): Promise<{ access_token: string }> {
    return api.post('/auth/refresh', { refresh_token: refreshToken })
  }

  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    await api.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    })
  }

  async resetPassword(email: string): Promise<void> {
    await api.post('/auth/reset-password', { email })
  }

  async confirmResetPassword(token: string, newPassword: string): Promise<void> {
    await api.post('/auth/reset-password/confirm', {
      token,
      new_password: newPassword,
    })
  }
}

export const authService = new AuthService()
export default authService