<template>
  <nav class="bg-white border-b border-gray-200 px-4 sm:px-6 py-4">
    <div class="flex justify-between items-center">
      <div class="flex items-center">
        <!-- Mobile menu button -->
        <button 
          @click="toggleMobileMenu" 
          class="md:hidden mr-3 p-2 rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
        </button>
        
        <div class="flex items-center space-x-3">
          <h1 class="text-xl sm:text-2xl font-bold text-black">Task Management</h1>
          
          <!-- Role Badge -->
          <span 
            v-if="user?.role" 
            :class="[
              'px-2 py-1 text-xs font-medium rounded-full',
              user.role === 'admin' 
                ? 'bg-purple-100 text-purple-800' 
                : 'bg-blue-100 text-blue-800'
            ]"
          >
            {{ user.role === 'admin' ? 'Admin' : 'User' }}
          </span>
        </div>
      </div>
      
      <div class="flex items-center space-x-4">
        <!-- User Info -->
        <div class="text-gray-600 text-sm sm:text-base">
          <span class="hidden sm:inline">Welcome, </span>
          <span class="font-medium text-black">
            {{ user?.username || 'User' }}
          </span>
        </div>
        
        <!-- User Profile/Menu (Optional for future) -->
        <div class="hidden sm:flex items-center space-x-2">
          <div class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
            <span class="text-sm font-medium text-gray-700">
              {{ getUserInitials(user?.username || user?.first_name || 'U') }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
defineProps({
  user: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['toggleMobileMenu'])

const toggleMobileMenu = () => {
  emit('toggleMobileMenu')
}

const getUserInitials = (name) => {
  if (!name) return 'U'
  return name.charAt(0).toUpperCase()
}
</script>