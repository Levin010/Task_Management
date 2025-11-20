<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useMainStore } from '@/stores'
import Navbar from '@/components/Navbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import UsersTable from '@/components/users/UsersTable.vue'
import AddUserModal from '@/components/users/AddUserModal.vue'
import EditUserModal from '@/components/users/EditUserModal.vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const router = useRouter()
const store = useMainStore()
const toast = useToast()

const user = computed(() => store.user)
const isLoading = computed(() => store.isLoading)

const users = ref([])
const error = ref(null)
const successMessage = ref(null)
const isMobileMenuOpen = ref(false)

// Add User Modal
const showAddModal = ref(false)
const addError = ref(null)
const isCreating = ref(false)

// Edit User Modal
const showEditModal = ref(false)
const editData = ref(null)
const editError = ref(null)
const isSaving = ref(false)

// Delete User Modal
const showDeleteModal = ref(false)
const userToDelete = ref(null)
const isDeleting = ref(false)

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

const fetchUsers = async () => {
  try {
    store.setIsLoading(true)
    error.value = null
    
    const token = store.getAccessToken()
    if (!token) {
      router.push('/sign-in')
      return
    }

    const response = await axios.get('/api/v1/admin/users/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    users.value = response.data
  } catch (err) {
    console.error('Error fetching users:', err)
    error.value = 'Failed to load users. Please try again.'
  } finally {
    store.setIsLoading(false)
  }
}

const refreshUsers = () => {
  fetchUsers()
}

// Add User Functions
const openAddModal = () => {
  addError.value = null
  showAddModal.value = true
}

const closeAddModal = () => {
  showAddModal.value = false
  addError.value = null
}

const createUser = async (formData) => {
  try {
    isCreating.value = true
    addError.value = null
    
    if (formData.password !== formData.password_confirmation) {
      addError.value = 'Passwords do not match.'
      return
    }
    
    const token = store.getAccessToken()
    if (!token) {
      router.push('/sign-in')
      return
    }

    const response = await axios.post('/api/v1/admin/users/create/', {
      username: formData.username,
      email: formData.email,
      first_name: formData.first_name,
      last_name: formData.last_name,
      role: formData.role,
      password: formData.password
    }, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    users.value.push(response.data)
    
    successMessage.value = 'User created successfully!'
    setTimeout(() => {
      successMessage.value = null
    }, 3000)
    
    closeAddModal()
  } catch (err) {
    console.error('Error creating user:', err)
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
        addError.value = errorMessages.join('. ')
      } else {
        addError.value = errors
      }
    } else {
      addError.value = 'Failed to create user. Please try again.'
    }
  } finally {
    isCreating.value = false
  }
}

// Edit User Functions
const openEditModal = (userData) => {
  editData.value = userData
  editError.value = null
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  editData.value = null
  editError.value = null
}

const saveUserChanges = async (formData) => {
  try {
    isSaving.value = true
    editError.value = null
    
    const token = store.getAccessToken()
    if (!token) {
      router.push('/sign-in')
      return
    }

    const response = await axios.put(`/api/v1/admin/users/${formData.id}/`, {
      first_name: formData.first_name,
      last_name: formData.last_name,
      username: formData.username,
      email: formData.email,
      role: formData.role
    }, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    const userIndex = users.value.findIndex(u => u.id === formData.id)
    if (userIndex !== -1) {
      users.value[userIndex] = response.data
    }
    
    successMessage.value = 'User updated successfully!'
    setTimeout(() => {
      successMessage.value = null
    }, 3000)
    
    closeEditModal()
  } catch (err) {
    console.error('Error updating user:', err)
    editError.value = err.response?.data?.error || 'Failed to update user. Please try again.'
  } finally {
    isSaving.value = false
  }
}

// Delete User Functions
const confirmDeleteUser = (userData) => {
  userToDelete.value = userData
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  userToDelete.value = null
}

const deleteUser = async () => {
  try {
    isDeleting.value = true
    
    const token = store.getAccessToken()
    if (!token) {
      router.push('/sign-in')
      return
    }

    await axios.delete(`/api/v1/admin/users/${userToDelete.value.id}/`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    users.value = users.value.filter(u => u.id !== userToDelete.value.id)
    
    successMessage.value = 'User deleted successfully!'
    setTimeout(() => {
      successMessage.value = null
    }, 3000)
    
    closeDeleteModal()
  } catch (err) {
    console.error('Error deleting user:', err)
    error.value = 'Failed to delete user. Please try again.'
  } finally {
    isDeleting.value = false
  }
}

onMounted(async () => {
  const isAuthenticated = await store.checkAuth()
  if (!isAuthenticated) {
    router.push('/sign-in')
    return
  }
  
  if (user.value?.role !== 'admin') {
    router.push('/dashboard')
    return
  }
  
  await fetchUsers()
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
          <h2 class="text-2xl sm:text-3xl font-bold text-black">Users</h2>
          <p class="text-gray-600 mt-2 text-sm sm:text-base">
            Manage system users and their details
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
                  <div class="h-4 bg-gray-200 rounded w-20"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Users Table Component -->
        <UsersTable 
          v-else
          :users="users"
          @add-user="openAddModal"
          @refresh="refreshUsers"
          @edit-user="openEditModal"
          @delete-user="confirmDeleteUser"
        />
      </main>
    </div>

    <!-- Add User Modal Component -->
    <AddUserModal 
      :isOpen="showAddModal"
      :isSubmitting="isCreating"
      :formError="addError"
      @close="closeAddModal"
      @submit="createUser"
    />

    <!-- Edit User Modal Component -->
    <EditUserModal 
      :isOpen="showEditModal"
      :initialData="editData"
      :isSubmitting="isSaving"
      :formError="editError"
      @close="closeEditModal"
      @submit="saveUserChanges"
    />

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3 text-center">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
            <svg class="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Delete User</h3>
          <p class="text-sm text-gray-500 mb-4">
            Are you sure you want to delete <strong>{{ userToDelete?.first_name }} {{ userToDelete?.last_name }}</strong>? 
            This action cannot be undone.
          </p>
          
          <div class="flex justify-center space-x-3">
            <button 
              @click="closeDeleteModal"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Cancel
            </button>
            <button 
              @click="deleteUser"
              :disabled="isDeleting"
              class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
            >
              {{ isDeleting ? 'Deleting...' : 'Delete User' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>