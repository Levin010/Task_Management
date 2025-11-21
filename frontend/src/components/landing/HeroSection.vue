<script setup>

</script>

<template>
  <div class="relative min-h-screen flex items-center justify-center">
    <div 
      class="absolute inset-0 bg-cover bg-center"
      style="background-image: url('/task_hero1.jpg')"
    >
      <div class="absolute inset-0 bg-black opacity-50"></div>
    </div>

    <div class="relative z-10 text-center text-white px-4 sm:px-6 lg:px-8 max-w-4xl">
      <h1 class="text-3xl sm:text-4xl lg:text-4xl font-bold mb-6">
        Manage all your tasks in one central location
      </h1>
      
      <p class="text-lg sm:text-xl lg:text-xl mb-8 text-gray-200">
        Streamline your workflow, boost productivity, and never miss a deadline. Keep your team aligned with powerful task management tools designed for modern teams.
      </p>
      
      <a 
        href="/sign-in" 
        class="inline-block bg-black hover:text-black hover:bg-white border-2 hover:border-black text-white font-semibold px-3 py-1 sm:px-4 sm:py-1.5 lg:px-6 lg:py-2 rounded-lg transition text-base sm:text-lg"
      >
        Get Started
      </a>
    </div>
  </div>
</template>