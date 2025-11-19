<script setup>
import SignUpForm from '@/components/SignUpForm.vue'
</script>

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
                        <router-link to="/sign-in" class="bg-white text-black px-6 py-3 rounded-full font-medium hover:bg-gray-100 transition-colors">
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

                <SignUpForm />

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