<script setup>
import { Facebook, Instagram, Twitter, Linkedin, Youtube } from 'lucide-vue-next';
</script>

<template>
  <footer class="border-t border-gray-200 py-20">
    <div class="max-w-4xl mx-auto px-6 sm:px-8">
      <div class="flex flex-col md:flex-row justify-between items-center">
        <div class="mb-4">
          <a href="/" class="text-xl font-bold">
            TASK MANAGEMENT
          </a>
        </div>
        <nav class="mb-4">
          <ul class="flex space-x-6">
            <li>
              <a href="/about">About Us</a>
            </li>
            <li>
              <a href="/contact">Contact Us</a>
            </li>
            <li>
              <a href="/faq">FAQ</a>
            </li>
            <li>
              <a href="/terms">Terms</a>
            </li>
            <li>
              <a href="/privacy">Privacy</a>
            </li>
          </ul>
        </nav>
        <div class="flex space-x-4 mb-4">
          <a 
            href="#"
            aria-label="Facebook"
            class="hover:text-blue-600"
          >
            <Facebook :size="24" />
          </a>
          <a 
            href="#"
            aria-label="Instagram"
            class="hover:text-blue-600"
          >
            <Instagram :size="24" />
          </a>
          <a 
            href="#"
            aria-label="Twitter"
            class="hover:text-blue-600"
          >
            <Twitter :size="24" />
          </a>
          <a 
            href="#"
            aria-label="LinkedIn"
            class="hover:text-blue-600"
          >
            <Linkedin :size="24" />
          </a>
          <a 
            href="#"
            aria-label="Youtube"
            class="hover:text-blue-600"
          >
            <Youtube :size="24" />
          </a>
        </div>
      </div>
      <div class="mt-8 text-center text-sm text-gray-500 flex justify-center space-x-4">
        <span>© Task Management. All rights reserved.</span>
        <a href="/privacy">Privacy Policy</a>
        <a href="/terms">Terms of Service</a>
        <a href="/cookies">Cookie Policy</a>
      </div>
    </div>
  </footer>
</template>