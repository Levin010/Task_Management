import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import Toast from 'vue-toastification'
import "vue-toastification/dist/index.css";
import axios from 'axios'
import App from './App.vue'

axios.defaults.baseURL = import.meta.env.VITE_API_URL


const app = createApp(App)

const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(Toast)

import { useMainStore } from './stores'
const store = useMainStore()

axios.defaults.headers.post['Content-Type'] = 'application/json'
axios.defaults.headers.put['Content-Type'] = 'application/json'
axios.defaults.headers.patch['Content-Type'] = 'application/json'

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

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (
      error.response?.status === 401 && 
      !originalRequest._retry &&
      !originalRequest.url.includes('/token/refresh/')
    ) {
      originalRequest._retry = true
      
      const refreshed = await store.refreshToken()
      
      if (refreshed) {
        originalRequest.headers.Authorization = `Bearer ${store.getAccessToken()}`
        return axios(originalRequest)
      } else {
        store.clearUser()
        router.push('/')
      }
    }
    
    if (error.response?.status === 401 && originalRequest.url.includes('/token/refresh/')) {
      store.clearUser()
      router.push('/')
    }
    
    return Promise.reject(error)
  }
)

app.mount('#app')