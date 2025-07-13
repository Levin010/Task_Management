<template>
    <div class="min-h-screen flex">
        <div class="hidden lg:flex lg:w-1/2 bg-black text-white flex-col justify-start items-center p-8 relative">
            <div class="max-w-md">
                <div class="text-center mt-46 mb-16">
                    <h1 class="text-4xl font-bold tracking-tight">Task Management</h1>
                </div>
                
                <div class="space-y-8">
                    <div class="text-left">
                        <h2 class="text-lg font-medium mb-4">Don't have an account?</h2>
                        <router-link to="/sign-up" class="bg-white text-black px-6 py-3 rounded-full font-medium hover:bg-gray-100 transition-colors">
                            Sign Up
                        </router-link>
                    </div>
                </div>
            </div>
        </div>

        <div class="w-full lg:w-1/2 flex items-center justify-center p-8">
            <div class="w-full max-w-md">
                <div class="lg:hidden text-center mb-8 bg-black w-full">
                    <h1 class="text-3xl font-bold tracking-tight text-white">Task Management</h1>
                </div>

                <div class="mb-8">
                    <h2 class="text-3xl font-bold text-black mb-4">Log in to your account</h2>
                    <p class="text-gray-600">All fields required. Enter your credentials to access your account.</p>
                </div>

                <form @submit.prevent="submitForm" class="space-y-6">

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Username (Admin username: admin)</label>
                        <input 
                            v-model="username"
                            type="text" 
                            class="w-full px-4 py-3 border-0 border-b-2 border-gray-300 focus:border-black focus:outline-none bg-transparent text-gray-900 placeholder-gray-500"
                            placeholder="Enter your username"
                            required
                        >
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Password (Admin password: Admin@1234)</label>
                        <input 
                            v-model="password"
                            type="password" 
                            class="w-full px-4 py-3 border-0 border-b-2 border-gray-300 focus:border-black focus:outline-none bg-transparent text-gray-900 placeholder-gray-500"
                            placeholder="Enter your password"
                            required
                        >
                    </div>

                    <div class="pt-4">
                        <button 
                            type="submit" 
                            class="w-full bg-black text-white py-3 px-4 rounded-md font-medium hover:bg-gray-800 transition-colors focus:outline-none focus:ring-2 focus:ring-black focus:ring-offset-2"
                        >
                            Log In
                        </button>
                    </div>
                </form>

                <div class="lg:hidden mt-8 text-center">
                    <p class="text-gray-600">Don't have an account?</p>
                    <router-link to="/sign-up" class="mt-2 bg-black text-white px-6 py-3 rounded-full font-medium hover:bg-gray-800 transition-colors">
                        Sign Up
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useMainStore } from '@/stores'

const router = useRouter()
const toast = useToast()
const store = useMainStore()

// Form fields
const username = ref('')
const password = ref('')

// Show success message from signup if it exists
onMounted(() => {
  if (store.successMessage) {
    toast.success(store.successMessage)
    store.clearMessages()
  }
})

const submitForm = async () => {
  store.clearFormErrors()
  
  if (!username.value.trim() || !password.value) {
    store.setFormErrors(['Username and password are required'])
    toast.error("Please fill in all fields.")
    return
  }

  const credentials = {
    username: username.value.trim(),
    password: password.value
  }

  const result = await store.login(credentials)
  
  if (result.success) {
    toast.success("Login successful! Welcome back!")
    router.push('/dashboard') 
  } else {
    toast.error(store.errorMessage || "Login failed. Please try again.")
  }
}
</script>
