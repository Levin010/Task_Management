<template>
    <div class="min-h-screen flex">
        <div class="hidden lg:flex lg:w-1/2 bg-black text-white flex-col justify-start items-center p-8 relative">
            <div class="max-w-md">
                <div class="text-center mt-46 mb-16">
                    <h1 class="text-4xl font-bold tracking-tight">Task Management</h1>
                </div>
                
                <div class="space-y-8">
                    <div class="text-left">
                        <h2 class="text-lg font-medium mb-4">Already have an account?</h2>
                        <router-link to="/" class="bg-white text-black px-6 py-3 rounded-full font-medium hover:bg-gray-100 transition-colors">
                            Log In
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
                    <h2 class="text-3xl font-bold text-black mb-4">Create a new account</h2>
                    <p class="text-gray-600">All fields required. Enter your credentials to access your account.</p>
                </div>

                <form @submit.prevent="submitForm" class="space-y-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">First Name</label>
                        <input 
                            v-model="firstName"
                            type="text" 
                            class="w-full px-4 py-3 border-0 border-b-2 border-gray-300 focus:border-black focus:outline-none bg-transparent text-gray-900 placeholder-gray-500"
                            :class="{ 'border-red-500 focus:border-red-500': hasFieldError('first_name') }"
                            placeholder="Enter your first name"
                            required
                        >
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Last Name</label>
                        <input 
                            v-model="lastName"
                            type="text" 
                            class="w-full px-4 py-3 border-0 border-b-2 border-gray-300 focus:border-black focus:outline-none bg-transparent text-gray-900 placeholder-gray-500"
                            :class="{ 'border-red-500 focus:border-red-500': hasFieldError('last_name') }"
                            placeholder="Enter your last name"
                            required
                        >
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Username</label>
                        <input 
                            v-model="username"
                            type="text" 
                            class="w-full px-4 py-3 border-0 border-b-2 border-gray-300 focus:border-black focus:outline-none bg-transparent text-gray-900 placeholder-gray-500"
                            :class="{ 'border-red-500 focus:border-red-500': hasFieldError('username') }"
                            placeholder="Enter your username"
                            required
                        >
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                        <input 
                            v-model="email"
                            type="email" 
                            class="w-full px-4 py-3 border-0 border-b-2 border-gray-300 focus:border-black focus:outline-none bg-transparent text-gray-900 placeholder-gray-500"
                            :class="{ 'border-red-500 focus:border-red-500': hasFieldError('email') }"
                            placeholder="Enter your email"
                            required
                        >
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Password</label>
                        <input 
                            v-model="password"
                            type="password" 
                            class="w-full px-4 py-3 border-0 border-b-2 border-gray-300 focus:border-black focus:outline-none bg-transparent text-gray-900 placeholder-gray-500"
                            :class="{ 'border-red-500 focus:border-red-500': hasFieldError('password') }"
                            placeholder="Enter your password"
                            required
                        >
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Confirm Password</label>
                        <input 
                            v-model="password2"
                            type="password" 
                            class="w-full px-4 py-3 border-0 border-b-2 border-gray-300 focus:border-black focus:outline-none bg-transparent text-gray-900 placeholder-gray-500"
                            :class="{ 'border-red-500 focus:border-red-500': hasFieldError('password2') }"
                            placeholder="Confirm your password"
                            required
                        >
                    </div>

                    <!-- Error Messages -->
                    <div v-if="store.formErrors.length" class="bg-red-50 border-l-4 border-red-400 p-4 rounded-md">
                        <div class="flex">
                            <div class="flex-shrink-0">
                                <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                                </svg>
                            </div>
                            <div class="ml-3">
                                <h3 class="text-sm font-medium text-red-800">
                                    Please fix the following errors:
                                </h3>
                                <div class="mt-2 text-sm text-red-700">
                                    <ul class="list-disc list-inside space-y-1">
                                        <li v-for="error in store.formErrors" :key="error">{{ error }}</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="pt-4">
                        <button 
                            type="submit" 
                            :disabled="store.isLoading"
                            class="w-full bg-black text-white py-3 px-4 rounded-md font-medium hover:bg-gray-800 transition-colors focus:outline-none focus:ring-2 focus:ring-black focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <span v-if="store.isLoading" class="flex items-center justify-center">
                                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Signing up...
                            </span>
                            <span v-else>Sign Up</span>
                        </button>
                    </div>
                </form>

                <div class="lg:hidden mt-8 text-center">
                    <p class="text-gray-600">Already have an account?</p>
                    <router-link to="/" class="mt-2 bg-black text-white px-6 py-3 rounded-full font-medium hover:bg-gray-800 transition-colors">
                        Log In
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useMainStore } from '@/stores'

const router = useRouter()
const toast = useToast()
const store = useMainStore()

// Form fields
const firstName = ref('')
const lastName = ref('')
const username = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')

// Validation functions
const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

const validatePassword = (password) => {
  return password.length >= 8
}

const hasFieldError = (fieldName) => {
  return store.formErrors.some(error => error.toLowerCase().includes(fieldName.toLowerCase()))
}

const submitForm = async () => {
  store.clearFormErrors()

  // Client-side validation
  const clientErrors = []

  if (!firstName.value.trim()) {
    clientErrors.push('First name is required')
  }

  if (!lastName.value.trim()) {
    clientErrors.push('Last name is required')
  }

  if (!username.value.trim()) {
    clientErrors.push('Username is required')
  } else if (username.value.length < 3) {
    clientErrors.push('Username must be at least 3 characters long')
  }

  if (!email.value.trim()) {
    clientErrors.push('Email is required')
  } else if (!validateEmail(email.value)) {
    clientErrors.push('Please enter a valid email address')
  }

  if (!password.value) {
    clientErrors.push('Password is required')
  } else if (!validatePassword(password.value)) {
    clientErrors.push('Password must be at least 8 characters long')
  }

  if (!password2.value) {
    clientErrors.push('Please confirm your password')
  } else if (password.value !== password2.value) {
    clientErrors.push('Passwords do not match')
  }

  if (clientErrors.length) {
    store.setFormErrors(clientErrors)
    toast.error("Please fix the form errors below.")
    return
  }

  // Prepare form data
  const formData = {
    first_name: firstName.value.trim(),
    last_name: lastName.value.trim(),
    username: username.value.trim(),
    email: email.value.trim(),
    password: password.value,
    confirm_password: password2.value
  }

  // Submit to store
  const result = await store.signup(formData)
  
  if (result.success) {
    toast.success("Account created successfully! Welcome aboard!")
    router.push('/')
  } else {
    toast.error(store.errorMessage || "Failed to create account. Please try again.")
  }
}
</script>