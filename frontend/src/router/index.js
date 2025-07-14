import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignUp from '@/views/SignUp.vue'
import Dashboard from '@/views/Dashboard.vue'
import { useMainStore } from '@/stores'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/sign-up',
      name: 'SignUp',
      component: SignUp
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard,
      meta: {
        requiresAuth: true  
      }
    }
  ],
})

router.beforeEach(async (to, from, next) => {
  const store = useMainStore()
  
  if (to.meta.requiresAuth) {
    const isAuthenticated = await store.checkAuth()
    if (!isAuthenticated) {
      next('/')
      return
    }
  }
  
  // Optional: Redirect authenticated users away from login/signup pages
  if (to.name === 'home' || to.name === 'SignUp') {
    const isAuthenticated = store.isAuthenticated
    if (isAuthenticated) {
      next('/dashboard')
      return
    }
  }
  
  next()
})

export default router
