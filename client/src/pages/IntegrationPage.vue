<script setup lang="ts">
import { ref, computed, onBeforeMount } from 'vue';
import { api } from 'boot/axios';

const integration = ref();

async function fetchCompanyInfo(){
  const r = await api.get('/api/integration/');

  integration.value = r.data;
}

onBeforeMount(async () => {
  await fetchCompanyInfo();
});
</script>


<template>
  <q-page>
  </q-page>
</template>