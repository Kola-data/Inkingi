import axios, { AxiosError, AxiosInstance, AxiosRequestConfig } from 'axios'
import { useAuthStore } from '@/stores/auth-store'
import toast from 'react-hot-toast'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

class ApiService {
  private client: AxiosInstance
  private isRefreshing = false
  private failedQueue: Array<{
    resolve: (token: string) => void
    reject: (error: any) => void
  }> = []

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.setupInterceptors()
  }

  private processQueue(error: any, token: string | null = null) {
    this.failedQueue.forEach((prom) => {
      if (error) {
        prom.reject(error)
      } else {
        prom.resolve(token!)
      }
    })
    this.failedQueue = []
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        const token = useAuthStore.getState().accessToken
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as AxiosRequestConfig & {
          _retry?: boolean
        }

        if (error.response?.status === 401 && !originalRequest._retry) {
          if (this.isRefreshing) {
            return new Promise((resolve, reject) => {
              this.failedQueue.push({ resolve, reject })
            }).then((token) => {
              originalRequest.headers!.Authorization = `Bearer ${token}`
              return this.client(originalRequest)
            })
          }

          originalRequest._retry = true
          this.isRefreshing = true

          const refreshToken = useAuthStore.getState().refreshToken

          if (!refreshToken) {
            useAuthStore.getState().logout()
            window.location.href = '/login'
            return Promise.reject(error)
          }

          try {
            const response = await axios.post(`${API_URL}/auth/refresh`, {
              refresh_token: refreshToken,
            })

            const { access_token } = response.data
            useAuthStore.getState().setTokens(access_token, refreshToken)
            
            this.processQueue(null, access_token)
            originalRequest.headers!.Authorization = `Bearer ${access_token}`
            
            return this.client(originalRequest)
          } catch (refreshError) {
            this.processQueue(refreshError, null)
            useAuthStore.getState().logout()
            window.location.href = '/login'
            return Promise.reject(refreshError)
          } finally {
            this.isRefreshing = false
          }
        }

        // Handle other errors
        if (error.response?.status === 403) {
          toast.error('You do not have permission to perform this action')
        } else if (error.response?.status === 404) {
          toast.error('Resource not found')
        } else if (error.response?.status === 500) {
          toast.error('Server error. Please try again later')
        }

        return Promise.reject(error)
      }
    )
  }

  // HTTP methods
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config)
    return response.data
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config)
    return response.data
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config)
    return response.data
  }

  async patch<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.patch<T>(url, data, config)
    return response.data
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config)
    return response.data
  }
}

export const api = new ApiService()
export default api