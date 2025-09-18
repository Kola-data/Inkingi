import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { api } from '../lib/api'

export interface User {
  id: number
  email: string
  phone?: string
  school_id: number
  staff_id?: number
  status: string
  email_verified: boolean
  phone_verified: boolean
  last_login_at?: string
  created_at: string
  updated_at?: string
}

interface AuthState {
  user: User | null
  token: string | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  checkAuth: () => Promise<void>
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isLoading: false,

      login: async (email: string, password: string) => {
        set({ isLoading: true })
        try {
          const response = await api.post('/auth/login', {
            email,
            password,
          })
          
          const { access_token } = response.data
          localStorage.setItem('token', access_token)
          
          // Get user profile
          const userResponse = await api.get('/auth/me', {
            headers: { Authorization: `Bearer ${access_token}` }
          })
          
          set({ 
            user: userResponse.data, 
            token: access_token,
            isLoading: false 
          })
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      logout: () => {
        localStorage.removeItem('token')
        set({ user: null, token: null })
      },

      checkAuth: async () => {
        const token = localStorage.getItem('token')
        if (!token) return

        set({ isLoading: true })
        try {
          const response = await api.get('/auth/me', {
            headers: { Authorization: `Bearer ${token}` }
          })
          set({ 
            user: response.data, 
            token,
            isLoading: false 
          })
        } catch (error) {
          localStorage.removeItem('token')
          set({ user: null, token: null, isLoading: false })
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ 
        user: state.user, 
        token: state.token 
      }),
    }
  )
)