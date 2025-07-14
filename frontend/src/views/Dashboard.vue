<template>
  <div class="flex h-screen bg-gray-50">
    <Sidebar 
      :user="user" 
      :isMobileMenuOpen="isMobileMenuOpen"
      @logout="handleLogout" 
      @closeMobileMenu="closeMobileMenu"
    />
    
    <div class="flex-1 flex flex-col min-w-0">
      <Navbar :user="user" @toggleMobileMenu="toggleMobileMenu" />
      
      <main class="flex-1 p-4 sm:p-6 overflow-y-auto">
        <div class="mb-6">
          <h2 class="text-2xl sm:text-3xl font-bold text-black">Dashboard</h2>
          <p class="text-gray-600 mt-2 text-sm sm:text-base">
            {{ user?.role === 'admin' ? 'Admin overview of the task management system' : 'Overview of your task management system' }}
          </p>
        </div>

        <div v-if="isLoading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6">
          <div v-for="i in (user?.role === 'admin' ? 6 : 5)" :key="i" class="bg-white p-4 sm:p-6 rounded-lg shadow-sm border border-gray-200 animate-pulse">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <div class="h-4 bg-gray-200 rounded mb-2"></div>
                <div class="h-8 bg-gray-200 rounded"></div>
              </div>
              <div class="w-10 h-10 bg-gray-200 rounded-full ml-4"></div>
            </div>
          </div>
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6">
          <div v-if="user?.role === 'admin'" class="bg-white p-4 sm:p-6 rounded-lg shadow-sm border border-gray-200">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs sm:text-sm font-medium text-gray-600">Total Users</p>
                <p class="text-2xl sm:text-3xl font-bold text-black">{{ dashboardStats.totalUsers }}</p>
              </div>
              <div class="bg-blue-100 p-2 sm:p-3 rounded-full">
                <svg class="w-5 h-5 sm:w-6 sm:h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
                </svg>
              </div>
            </div>
          </div>

          <div class="bg-white p-4 sm:p-6 rounded-lg shadow-sm border border-gray-200">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs sm:text-sm font-medium text-gray-600">Total Tasks</p>
                <p class="text-2xl sm:text-3xl font-bold text-black">{{ dashboardStats.totalTasks }}</p>
              </div>
              <div class="bg-gray-100 p-2 sm:p-3 rounded-full">
                <svg class="w-5 h-5 sm:w-6 sm:h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
              </div>
            </div>
          </div>

          <div class="bg-white p-4 sm:p-6 rounded-lg shadow-sm border border-gray-200">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs sm:text-sm font-medium text-gray-600">Pending Tasks</p>
                <p class="text-2xl sm:text-3xl font-bold text-black">{{ dashboardStats.pendingTasks }}</p>
              </div>
              <div class="bg-yellow-100 p-2 sm:p-3 rounded-full">
                <svg class="w-5 h-5 sm:w-6 sm:h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
            </div>
          </div>

          <div class="bg-white p-4 sm:p-6 rounded-lg shadow-sm border border-gray-200">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs sm:text-sm font-medium text-gray-600">Ongoing Tasks</p>
                <p class="text-2xl sm:text-3xl font-bold text-black">{{ dashboardStats.ongoingTasks }}</p>
              </div>
              <div class="bg-blue-100 p-2 sm:p-3 rounded-full">
                <svg class="w-5 h-5 sm:w-6 sm:h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
              </div>
            </div>
          </div>

          <div class="bg-white p-4 sm:p-6 rounded-lg shadow-sm border border-gray-200">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs sm:text-sm font-medium text-gray-600">Overdue Tasks</p>
                <p class="text-2xl sm:text-3xl font-bold text-black">{{ dashboardStats.overdueTasks }}</p>
              </div>
              <div class="bg-red-100 p-2 sm:p-3 rounded-full">
                <svg class="w-5 h-5 sm:w-6 sm:h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                </svg>
              </div>
            </div>
          </div>

          <div class="bg-white p-4 sm:p-6 rounded-lg shadow-sm border border-gray-200">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs sm:text-sm font-medium text-gray-600">Completed Tasks</p>
                <p class="text-2xl sm:text-3xl font-bold text-black">{{ dashboardStats.completedTasks }}</p>
              </div>
              <div class="bg-green-100 p-2 sm:p-3 rounded-full">
                <svg class="w-5 h-5 sm:w-6 sm:h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- Error State -->
        <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mt-6">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
            <p class="text-red-800">{{ error }}</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useMainStore } from '@/stores'
import Navbar from '@/components/Navbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const router = useRouter()
const store = useMainStore()
const toast = useToast()

const user = computed(() => store.user)
const isLoading = computed(() => store.isLoading)

const dashboardStats = ref({
  totalUsers: 0,
  totalTasks: 0,
  pendingTasks: 0,
  ongoingTasks: 0,
  overdueTasks: 0,
  completedTasks: 0
})

const isMobileMenuOpen = ref(false)
const error = ref(null)

const handleLogout = async () => {
  try {
    const result = await store.logout()
    if (result.success) {
      router.push('/')
    }
  } catch (error) {
    console.error('Logout failed:', error)
  }
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

const fetchDashboardStats = async () => {
  try {
    store.setIsLoading(true)
    error.value = null
    
    const token = store.getAccessToken()
    if (!token) {
      router.push('/')
      return
    }

    
    if (user.value?.role === 'admin') {
      try {
        const usersResponse = await axios.get('/api/v1/admin/users/', {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        dashboardStats.value.totalUsers = usersResponse.data.length || 0
      } catch (err) {
        console.error('Error fetching users:', err)
        dashboardStats.value.totalUsers = 0
      }
    }
    
    dashboardStats.value = {
      ...dashboardStats.value,
      totalTasks: user.value?.role === 'admin' ? 156 : 23,
      pendingTasks: user.value?.role === 'admin' ? 23 : 8,
      ongoingTasks: user.value?.role === 'admin' ? 31 : 12,
      overdueTasks: user.value?.role === 'admin' ? 7 : 2,
      completedTasks: user.value?.role === 'admin' ? 95 : 1
    }
    
  } catch (err) {
    console.error('Error fetching dashboard stats:', err)
    error.value = 'Failed to load dashboard statistics. Please try again.'
  } finally {
    store.setIsLoading(false)
  }
}

onMounted(async () => {
  const isAuthenticated = await store.checkAuth()
  if (!isAuthenticated) {
    router.push('/')
    return
  }
  
  await fetchDashboardStats()
})
</script>