<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useMainStore } from '@/stores'
import Navbar from '@/components/Navbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import AllTasksTable from '@/components/tasks/AllTasksTable.vue'
import AddTaskModal from '@/components/tasks/AddTaskModal.vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const router = useRouter()
const store = useMainStore()
const toast = useToast()

const user = computed(() => store.user)
const isLoading = computed(() => store.isLoading)

const tasks = ref([])
const availableUsers = ref([])
const error = ref(null)
const successMessage = ref(null)
const isMobileMenuOpen = ref(false)

const showAddModal = ref(false)
const formError = ref(null)
const isCreating = ref(false)

const handleLogout = async () => {
  try {
    const result = await store.logout()
    if (result.success) {
      router.push('/sign-in')
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

const fetchTasks = async () => {
  try {
    store.setIsLoading(true)
    error.value = null
    
    const token = store.getAccessToken()
    if (!token) {
      router.push('/sign-in')
      return
    }

    const response = await axios.get('/api/v1/tasks/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    tasks.value = response.data
  } catch (err) {
    console.error('Error fetching tasks:', err)
    error.value = 'Failed to load tasks. Please try again.'
  } finally {
    store.setIsLoading(false)
  }
}

const fetchAvailableUsers = async () => {
  try {
    const token = store.getAccessToken()
    if (!token) {
      router.push('/sign-in')
      return
    }

    const response = await axios.get('/api/v1/admin/users/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    // Filter users with role 'member' only
    availableUsers.value = response.data.filter(user => user.role === 'member')
  } catch (err) {
    console.error('Error fetching users:', err)
    error.value = 'Failed to load users. Please try again.'
  }
}

const refreshTasks = () => {
  fetchTasks()
}

const openAddModal = () => {
  formError.value = null
  showAddModal.value = true
}

const closeAddModal = () => {
  showAddModal.value = false
  formError.value = null
}

const createTask = async (formData) => {
  try {
    isCreating.value = true
    formError.value = null
    
    const token = store.getAccessToken()
    if (!token) {
      router.push('/sign-in')
      return
    }

    const response = await axios.post('/api/v1/tasks/', {
      title: formData.title,
      description: formData.description,
      assigned_to: formData.assigned_to,
      status: formData.status,
      deadline: formData.deadline
    }, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    // Add the new task to the local array
    tasks.value.unshift(response.data)
    
    successMessage.value = 'Task created successfully!'
    setTimeout(() => {
      successMessage.value = null
    }, 3000)
    
    closeAddModal()
  } catch (err) {
    console.error('Error creating task:', err)
    if (err.response?.data) {
      const errors = err.response.data
      if (typeof errors === 'object') {
        const errorMessages = []
        for (const [field, messages] of Object.entries(errors)) {
          if (Array.isArray(messages)) {
            errorMessages.push(...messages)
          } else {
            errorMessages.push(messages)
          }
        }
        formError.value = errorMessages.join('. ')
      } else {
        formError.value = errors
      }
    } else {
      formError.value = 'Failed to create task. Please try again.'
    }
  } finally {
    isCreating.value = false
  }
}

onMounted(async () => {
  const isAuthenticated = await store.checkAuth()
  if (!isAuthenticated) {
    router.push('/sign-in')
    return
  }
  
  // Allow both admin and manager roles
  if (user.value?.role !== 'admin' && user.value?.role !== 'manager') {
    router.push('/dashboard')
    return
  }
  
  await Promise.all([fetchTasks(), fetchAvailableUsers()])
})
</script>

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
          <h2 class="text-2xl sm:text-3xl font-bold text-black">Tasks</h2>
          <p class="text-gray-600 mt-2 text-sm sm:text-base">
            Manage all system tasks and assignments
          </p>
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
                  <div class="h-4 bg-gray-200 rounded flex-1"></div>
                  <div class="h-4 bg-gray-200 rounded w-20"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tasks Table Component -->
        <AllTasksTable 
          v-else
          :tasks="tasks"
          @add-task="openAddModal"
          @refresh="refreshTasks"
        />

        <!-- Add Task Modal Component -->
        <AddTaskModal 
          :isOpen="showAddModal"
          :availableUsers="availableUsers"
          :isSubmitting="isCreating"
          :formError="formError"
          @close="closeAddModal"
          @submit="createTask"
        />
      </main>
    </div>
  </div>
</template>