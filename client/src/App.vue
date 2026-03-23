<template>
  <router-view />
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue';
import { useAuthStore } from './stores/authstore';

const authStore = useAuthStore();

let intervalId: number | undefined;

onMounted(async () => {
  await authStore.updateTokens();

  intervalId = window.setInterval(async () => {
    await authStore.updateTokens();
  }, 60000);
});
</script>
