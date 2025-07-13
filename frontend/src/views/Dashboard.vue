<template>
  <div class="p-6">
    <h1 class="text-2xl font-semibold mb-4">Welcome user to the dashboard</h1>
    <button
      @click="handleLogout"
      class="bg-red-500 hover:bg-red-600 text-white font-medium py-2 px-4 rounded-md transition duration-200"
    >
      Logout
    </button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useMainStore } from '@/stores'

const router = useRouter()
const mainStore = useMainStore()

async function handleLogout() {
  const result = await mainStore.logout()
  if (result.success) {
    router.push('/')
  } else {
    alert(result.error)
  }
}
</script>

