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
          <h2 class="text-2xl sm:text-3xl font-bold text-black">My Tasks</h2>
          <p class="text-gray-600 mt-2 text-sm sm:text-base">
            View and manage tasks assigned to you
          </p>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div class="p-6">
            <div class="animate-pulse">
              <div class="h-4 bg-gray-200 rounded mb-4"></div>
              <div class="space-y-3">
                <div v-for="i in 5" :key="i" class="flex space-x-4">
                  <div class="h-4 bg-gray-200 rounded flex-1"></div>
                  <div class="h-4 bg-gray-200 rounded flex-1"></div>
                  <div class="h-4 bg-gray-200 rounded flex-1"></div>
                  <div class="h-4 bg-gray-200 rounded w-20"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tasks Table -->
        <div v-else class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold text-black">My Tasks</h3>
              <div class="flex items-center space-x-4">
                <span class="text-sm text-gray-500">Total: {{ tasks.length }} tasks</span>
                <div class="flex items-center space-x-2">
                  <button 
                    @click="refreshTasks"
                    class="inline-flex items-center px-3 py-1.5 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                    </svg>
                    Refresh
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Task
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Deadline
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Created
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="task in tasks" :key="task.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4">
                    <div class="flex flex-col">
                      <div class="text-sm font-medium text-gray-900">
                        {{ task.title }}
                      </div>
                      <div class="text-sm text-gray-500 mt-1">
                        {{ task.description }}
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getStatusBadgeClass(task.status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                      {{ formatStatus(task.status) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">
                      {{ formatDateTime(task.deadline) }}
                    </div>
                    <div v-if="isOverdue(task)" class="text-xs text-red-600 mt-1">
                      Overdue
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatDate(task.created_at) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div class="flex space-x-2">
                      <!-- Start Task Button -->
                      <button 
                        v-if="task.status === 'pending'"
                        @click="startTask(task)"
                        :disabled="isUpdating"
                        class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                      >
                        <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h.01M19 10a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        {{ isUpdating ? 'Starting...' : 'Start' }}
                      </button>
                      
                      <!-- Complete Task Button -->
                      <button 
                        v-if="task.status === 'in_progress'"
                        @click="completeTask(task)"
                        :disabled="isUpdating"
                        class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
                      >
                        <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                        </svg>
                        {{ isUpdating ? 'Completing...' : 'Complete' }}
                      </button>
                      
                      <!-- No Actions Available -->
                      <span v-if="task.status === 'completed' || task.status === 'overdue'" class="text-xs text-gray-500">
                        {{ task.status === 'completed' ? 'Completed' : 'Overdue' }}
                      </span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Empty State -->
          <div v-if="!isLoading && tasks.length === 0" class="text-center py-12">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v11a2 2 0 002 2h5.586a1 1 0 00.707-.293l5.414-5.414a1 1 0 00.293-.707V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">No tasks assigned</h3>
            <p class="mt-1 text-sm text-gray-500">You don't have any tasks assigned to you yet.</p>
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

        <!-- Success Message -->
        <div v-if="successMessage" class="bg-green-50 border border-green-200 rounded-lg p-4 mt-6">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <p class="text-green-800">{{ successMessage }}</p>
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

const router = useRouter()
const store = useMainStore()

const user = computed(() => store.user)
const isLoading = computed(() => store.isLoading)

const tasks = ref([])
const error = ref(null)
const successMessage = ref(null)
const isMobileMenuOpen = ref(false)
const isUpdating = ref(false)

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

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatDateTime = (dateString) => {
  return new Date(dateString).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatStatus = (status) => {
  const statusMap = {
    'pending': 'Pending',
    'in_progress': 'In Progress',
    'completed': 'Completed',
    'overdue': 'Overdue'
  }
  return statusMap[status] || status
}

const getStatusBadgeClass = (status) => {
  const statusClasses = {
    'pending': 'bg-yellow-100 text-yellow-800',
    'in_progress': 'bg-blue-100 text-blue-800',
    'completed': 'bg-green-100 text-green-800',
    'overdue': 'bg-red-100 text-red-800'
  }
  return statusClasses[status] || 'bg-gray-100 text-gray-800'
}

const isOverdue = (task) => {
  const now = new Date()
  const deadline = new Date(task.deadline)
  return deadline < now && task.status !== 'completed'
}

const fetchMyTasks = async () => {
  try {
    store.setIsLoading(true)
    error.value = null
    
    const token = store.getAccessToken()
    if (!token) {
      router.push('/')
      return
    }

    const response = await axios.get('/api/v1/my-tasks/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    tasks.value = response.data
  } catch (err) {
    console.error('Error fetching my tasks:', err)
    error.value = 'Failed to load your tasks. Please try again.'
  } finally {
    store.setIsLoading(false)
  }
}

const startTask = async (task) => {
  try {
    isUpdating.value = true
    error.value = null
    
    const token = store.getAccessToken()
    if (!token) {
      router.push('/')
      return
    }

    const response = await axios.post(`/api/v1/tasks/${task.id}/start/`, {}, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    // Update the task status in the local array
    const taskIndex = tasks.value.findIndex(t => t.id === task.id)
    if (taskIndex !== -1) {
      tasks.value[taskIndex] = response.data
    }
    
    successMessage.value = 'Task started successfully!'
    setTimeout(() => {
      successMessage.value = null
    }, 3000)
    
  } catch (err) {
    console.error('Error starting task:', err)
    error.value = 'Failed to start task. Please try again.'
  } finally {
    isUpdating.value = false
  }
}

const completeTask = async (task) => {
  try {
    isUpdating.value = true
    error.value = null
    
    const token = store.getAccessToken()
    if (!token) {
      router.push('/')
      return
    }

    const response = await axios.post(`/api/v1/tasks/${task.id}/complete/`, {}, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    // Update the task status in the local array
    const taskIndex = tasks.value.findIndex(t => t.id === task.id)
    if (taskIndex !== -1) {
      tasks.value[taskIndex] = response.data
    }
    
    successMessage.value = 'Task completed successfully!'
    setTimeout(() => {
      successMessage.value = null
    }, 3000)
    
  } catch (err) {
    console.error('Error completing task:', err)
    error.value = 'Failed to complete task. Please try again.'
  } finally {
    isUpdating.value = false
  }
}

const refreshTasks = () => {
  fetchMyTasks()
}

onMounted(async () => {
  const isAuthenticated = await store.checkAuth()
  if (!isAuthenticated) {
    router.push('/')
    return
  }
  
  // Only users with 'user' role can access this page
  if (user.value?.role !== 'user') {
    router.push('/dashboard')
    return
  }
  
  await fetchMyTasks()
})
</script>