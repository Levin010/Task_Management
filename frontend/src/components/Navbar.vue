<template>
  <nav class="bg-white border-b border-gray-200 px-4 sm:px-6 py-4">
    <div class="flex justify-between items-center">
      <div class="flex items-center">
        <button 
          @click="toggleMobileMenu"
          class="md:hidden mr-3 p-2 rounded-md hover:bg-gray-100"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
        </button>
        
        <h1 class="text-xl sm:text-2xl font-bold text-black">Task Management</h1>
      </div>
      
      <div class="text-gray-600 text-sm sm:text-base">
        <span class="hidden sm:inline">Welcome, </span>
        <span class="font-medium text-black">{{ user.username }}</span>
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
</script>