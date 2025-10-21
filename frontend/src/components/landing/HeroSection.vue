<script setup>

</script>

<template>
  <div class="relative min-h-screen flex items-center justify-center">
    <!-- Background Image with Overlay -->
    <div 
      class="absolute inset-0 bg-cover bg-center"
      style="background-image: url('/task_hero1.jpg')"
    >
      <div class="absolute inset-0 bg-black opacity-50"></div>
    </div>

    <!-- Content -->
    <div class="relative z-10 text-center text-white px-4 sm:px-6 lg:px-8 max-w-4xl">
      <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6">
        Manage all your tasks in one central location
      </h1>
      
      <p class="text-lg sm:text-xl lg:text-2xl mb-8 text-gray-200">
        Streamline your workflow, boost productivity, and never miss a deadline. Keep your team aligned with powerful task management tools designed for modern teams.
      </p>
      
      <a 
        href="/signin" 
        class="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3 rounded-lg transition text-lg"
      >
        Get Started
      </a>
    </div>
  </div>
</template>