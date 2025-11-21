<script setup>
import HeroSection from '@/components/landing/HeroSection.vue'
import HowItWorks from '@/components/landing/HowItWorks.vue';
import CallToAction from '@/components/landing/CallToAction.vue';
import LandingNavbar from '@/components/landing/LandingNavbar.vue';
import FooterSection from '@/components/landing/FooterSection.vue';

// import { onMounted } from 'vue';
// import { useMainStore } from '@/stores';
// import { useToast } from 'vue-toastification';

// const store = useMainStore()
// const toast = useToast()

// onMounted(() => {
//   if (store.successMessage) {
//     toast.success(store.successMessage)
//     store.clearMessages()
//   }
// })
</script>

<template>
    <div class="h-full w-full relative">
        <div class="relative">
            <div>
                <LandingNavbar/>
            </div>
            <div>
                <HeroSection/>
            </div>
            <div>
                <HowItWorks/>
            </div>
            <div>
                <CallToAction/>
            </div>
            <div>
                <FooterSection/>
            </div>
        </div>
    </div>
</template>

