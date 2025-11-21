<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useMainStore } from '@/stores'

const router = useRouter()
const toast = useToast()
const store = useMainStore()

const firstName = ref('')
const lastName = ref('')
const username = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')
const role = ref('member')

const showPassword = ref(false)
const showPassword2 = ref(false)

const togglePasswordVisibility = (field) => {
  if (field === 'password') {
    showPassword.value = !showPassword.value
  } else if (field === 'password2') {
    showPassword2.value = !showPassword2.value
  }
}

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

  const formData = {
    first_name: firstName.value.trim(),
    last_name: lastName.value.trim(),
    username: username.value.trim(),
    email: email.value.trim(),
    password: password.value,
    confirm_password: password2.value,
    role: role.value
  }

  const result = await store.signup(formData)
  
  if (result.success) {
    toast.success("Account created successfully! Welcome aboard!")
    router.push('/dashboard')
  } else {
    toast.error(store.errorMessage || "Failed to create account. Please try again.")
  }
}
</script>

<template>
    <div class="space-y-6">
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
            <label class="block text-sm font-medium text-gray-700 mb-4">Role</label>
            <div class="flex gap-6">
                <label class="flex items-center cursor-pointer">
                    <input 
                        v-model="role"
                        type="radio" 
                        value="member" 
                        class="w-4 h-4 accent-black bg-gray-100 border-gray-300"
                    >
                    <span class="ml-2 text-sm text-gray-700">Team Member</span>
                </label>
                <label class="flex items-center cursor-pointer">
                    <input 
                        v-model="role"
                        type="radio" 
                        value="manager" 
                        class="w-4 h-4 accent-black bg-gray-100 border-gray-300"
                    >
                    <span class="ml-2 text-sm text-gray-700">Manager</span>
                </label>
            </div>
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Password</label>
            <div class="relative">
                <input 
                    v-model="password"
                    :type="showPassword ? 'text' : 'password'" 
                    class="w-full px-4 py-3 pr-12 border-0 border-b-2 border-gray-300 focus:border-black focus:outline-none bg-transparent text-gray-900 placeholder-gray-500"
                    :class="{ 'border-red-500 focus:border-red-500': hasFieldError('password') }"
                    placeholder="Enter your password"
                    required
                >
                <font-awesome-icon 
                    :icon="['fas', showPassword ? 'eye' : 'eye-slash']" 
                    class="absolute right-3 top-1/2 transform -translate-y-1/2 cursor-pointer text-gray-500 hover:text-gray-700"
                    @click="togglePasswordVisibility('password')"
                />
            </div>
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Confirm Password</label>
            <div class="relative">
                <input 
                    v-model="password2"
                    :type="showPassword2 ? 'text' : 'password'" 
                    class="w-full px-4 py-3 pr-12 border-0 border-b-2 border-gray-300 focus:border-black focus:outline-none bg-transparent text-gray-900 placeholder-gray-500"
                    :class="{ 'border-red-500 focus:border-red-500': hasFieldError('password2') }"
                    placeholder="Confirm your password"
                    required
                >
                <font-awesome-icon 
                    :icon="['fas', showPassword2 ? 'eye' : 'eye-slash']" 
                    class="absolute right-3 top-1/2 transform -translate-y-1/2 cursor-pointer text-gray-500 hover:text-gray-700"
                    @click="togglePasswordVisibility('password2')"
                />
            </div>
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
                @click="submitForm"
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
    </div>
</template>