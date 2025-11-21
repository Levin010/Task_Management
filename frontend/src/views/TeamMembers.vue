<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useMainStore } from '@/stores'
import Navbar from '@/components/Navbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import TeamMembersTable from '@/components/users/TeamMembersTable.vue'
import axios from 'axios'

const router = useRouter()
const store = useMainStore()

const user = computed(() => store.user)
const isLoading = computed(() => store.isLoading)

const teamMembers = ref([])
const error = ref(null)
const isMobileMenuOpen = ref(false)

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

const fetchTeamMembers = async () => {
  try {
    store.setIsLoading(true)
    error.value = null
    
    const token = store.getAccessToken()
    if (!token) {
      router.push('/sign-in')
      return
    }

    const response = await axios.get('/api/v1/manager/team-members/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    teamMembers.value = response.data
  } catch (err) {
    console.error('Error fetching team members:', err)
    if (err.response?.status === 403) {
      router.push('/dashboard')
    } else {
      error.value = 'Failed to load team members. Please try again.'
    }
  } finally {
    store.setIsLoading(false)
  }
}

const refreshTeamMembers = () => {
  fetchTeamMembers()
}

onMounted(async () => {
  const isAuthenticated = await store.checkAuth()
  if (!isAuthenticated) {
    router.push('/sign-in')
    return
  }
  
  if (user.value?.role !== 'manager') {
    router.push('/dashboard')
    return
  }
  
  await fetchTeamMembers()
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
          <h2 class="text-2xl sm:text-3xl font-bold text-black">Team Members</h2>
          <p class="text-gray-600 mt-2 text-sm sm:text-base">
            View team members you've assigned tasks and their performance history.
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
                  <div class="h-4 bg-gray-200 rounded flex-1"></div>
                  <div class="h-4 bg-gray-200 rounded w-20"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Team Members Table Component -->
        <TeamMembersTable 
          v-else
          :members="teamMembers"
          @refresh="refreshTeamMembers"
        />
      </main>
    </div>
  </div>
</template>