import { createRouter, createWebHistory } from 'vue-router'
import SignIn from '../views/SignIn.vue'
import SignUp from '@/views/SignUp.vue'
import Dashboard from '@/views/Dashboard.vue'
import { useMainStore } from '@/stores'
import Users from '@/views/Users.vue'
import AllTasks from '@/views/AllTasks.vue'
import MyTasks from '@/views/MyTasks.vue'
import Landing from '@/views/Landing.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Landing',
      component: Landing,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/sign-in',
      name: 'SignIn',
      component: SignIn
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
    },
    {
      path: '/users',
      name: 'Users',
      component: Users,
      meta: {
        requiresAuth: true  
      }
    },
    {
      path: '/all-tasks',
      name: 'AllTasks',
      component: AllTasks,
      meta: {
        requiresAuth: true  
      }
    },
    {
      path: '/my-tasks',
      name: 'MyTasks',
      component: MyTasks,
      meta: {
        requiresAuth: true  
      }
    },
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
