import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import Toast from 'vue-toastification'
import axios from 'axios'
import App from './App.vue'

// Axios config
axios.defaults.baseURL = import.meta.env.VITE_API_URL
// Remove withCredentials since we're using localStorage
// axios.defaults.withCredentials = true

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(Toast)

// ✅ Now it's safe to use stores
import { useMainStore } from './stores'
const store = useMainStore()

// Request interceptor to add auth token
axios.interceptors.request.use(
  (config) => {
    const token = store.getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for auto token refresh and logout on 401
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      // Try to refresh the token
      const refreshed = await store.refreshToken()
      
      if (refreshed) {
        // Retry the original request with new token
        originalRequest.headers.Authorization = `Bearer ${store.getAccessToken()}`
        return axios(originalRequest)
      } else {
        // Refresh failed, redirect to login
        store.clearUser()
        router.push('/')
      }
    }
    
    return Promise.reject(error)
  }
)

app.mount('#app')