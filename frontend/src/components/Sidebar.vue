<script setup>

import { LayoutDashboard, CheckSquare, Users, LogOut, X } from 'lucide-vue-next'

defineProps({
  user: {
    type: Object,
    required: true
  },
  isMobileMenuOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['logout', 'closeMobileMenu'])

const handleLogout = () => {
  emit('logout')
}

const closeMobileMenu = () => {
  emit('closeMobileMenu')
}
</script>

<template>
  <div 
    v-if="isMobileMenuOpen" 
    class="fixed inset-0 z-20 md:hidden"
    @click="closeMobileMenu"
  ></div>

  <div :class="[
    'fixed inset-y-0 left-0 z-30 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out md:relative md:translate-x-0',
    isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
  ]">
    <div class="flex flex-col h-full">
      <div class="flex items-center justify-between p-4 border-b border-gray-200">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-black rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-sm">TM</span>
          </div>
          <div>
            <h3 class="font-semibold text-gray-900">{{ user?.username || 'User' }}</h3>
            <p class="text-xs text-gray-500 capitalize">{{ user?.role || 'user' }}</p>
          </div>
        </div>
        
        <button 
          @click="closeMobileMenu"
          class="md:hidden p-1 rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-black"
        >
          <X class="w-5 h-5" />
        </button>
      </div>

      <nav class="flex-1 p-4 space-y-2">
        <!-- Dashboard -->
        <router-link 
          to="/dashboard" 
          class="flex items-center space-x-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          active-class="bg-blue-50 text-blue-700 border-r-2 border-blue-600"
          @click="closeMobileMenu"
        >
          <LayoutDashboard class="w-5 h-5" />
          <span>Dashboard</span>
        </router-link>

        <!-- Tasks -->
        <router-link 
          :to="user?.role === 'admin' || user?.role === 'manager' ? '/all-tasks' : '/my-tasks'"
          class="flex items-center space-x-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          active-class="bg-blue-50 text-blue-700 border-r-2 border-blue-600"
          @click="closeMobileMenu"
        >
          <CheckSquare class="w-5 h-5" />
          <span>Tasks</span>
        </router-link>

        <!-- Manager Only Links -->
        <template v-if="user?.role === 'manager'">
          <!-- User Management -->
          <router-link 
            to="/team-members" 
            class="flex items-center space-x-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            active-class="bg-blue-50 text-blue-700 border-r-2 border-blue-600"
            @click="closeMobileMenu"
          >
            <Users class="w-5 h-5" />
            <span>Team Members</span>
          </router-link>

        </template>

        <!-- Admin Only Links -->
        <template v-if="user?.role === 'admin'">
          <hr class="border-gray-200 my-3">
          <p class="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Admin</p>
          
          <!-- User Management -->
          <router-link 
            to="/users" 
            class="flex items-center space-x-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            active-class="bg-blue-50 text-blue-700 border-r-2 border-blue-600"
            @click="closeMobileMenu"
          >
            <Users class="w-5 h-5" />
            <span>Users</span>
          </router-link>

        </template>

        <!-- User Profile -->
        <hr class="border-gray-200 my-3">
        <!-- <router-link 
          to="/profile" 
          class="flex items-center space-x-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          active-class="bg-blue-50 text-blue-700 border-r-2 border-blue-600"
          @click="closeMobileMenu"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
          </svg>
          <span>Profile</span>
        </router-link> -->
      </nav>

      <!-- Logout Button -->
      <div class="p-4 border-t border-gray-200">
        <button 
          @click="handleLogout"
          class="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-red-600 cursor-pointer hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors"
        >
          <LogOut class="w-5 h-5" />
          <span>Logout</span>
        </button>
      </div>
    </div>
  </div>
</template>