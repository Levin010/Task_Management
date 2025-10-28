<script setup>
import { CheckCircle, ClipboardList, UserRoundPlus } from 'lucide-vue-next';
</script>

<template>
  <div class="bg-white py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <h2 class="text-3xl sm:text-4xl font-bold text-center mb-8 text-black">
        How It Works
      </h2>
      
      <div class="flex flex-col md:flex-row gap-8">
        <div class="flex-1 bg-black text-white p-8 rounded-lg shadow-lg hover:shadow-2xl transition">
          <UserRoundPlus :size="48" class="mb-4" />
          <h3 class="text-2xl font-bold mb-4">Create Account</h3>
          <p class="text-gray-300">
            Create an account as either a manager or team member
          </p>
        </div>

        <div class="flex-1 bg-black text-white p-8 rounded-lg shadow-lg hover:shadow-2xl transition">
          <ClipboardList :size="48" class="mb-4" />
          <h3 class="text-2xl font-bold mb-4">Assigning Tasks</h3>
          <p class="text-gray-300">
            Manager users can assign tasks to member users with deadlines, and can track their progress. Manager users can also create new member users
          </p>
        </div>

        <div class="flex-1 bg-black text-white p-8 rounded-lg shadow-lg hover:shadow-2xl transition">
          <CheckCircle :size="48" class="mb-4" />
          <h3 class="text-2xl font-bold mb-4">Update Progress</h3>
          <p class="text-gray-300">
            Team member users receive an email once assigned a task. After logging in, they can update the progress of an assigned task from not started to in progress to completed
          </p>
        </div>
      </div>
    </div>
  </div>
</template>