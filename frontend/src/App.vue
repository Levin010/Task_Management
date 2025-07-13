<template>
    <router-view></router-view>
</template>

<script setup>
import { onMounted } from 'vue'
import { useMainStore } from '@/stores'

const mainStore = useMainStore()

onMounted(() => {
  mainStore.checkAuth()
})
</script>
