import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import { useMainStore } from './stores'

axios.defaults.baseURL = import.meta.env.VITE_API_URL

axios.defaults.withCredentials = true

// response interceptor for automatic logout on 401
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const store = useMainStore()
      store.clearUser()
      router.push('/')
    }
    return Promise.reject(error)
  }
)

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Toast);

app.mount('#app')
