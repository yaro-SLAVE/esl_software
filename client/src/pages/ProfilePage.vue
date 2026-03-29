<script setup lang="ts">
import { useAuthStore } from '../stores/authstore';

const authStore = useAuthStore();

</script>

<template>
  <q-page>
    <q-btn
      label="Выйти"
      color="deep-orange"
      @click="authStore.logout"
    />
  </q-page>
</template>