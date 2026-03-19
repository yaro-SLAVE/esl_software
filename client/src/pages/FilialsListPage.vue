<script setup lang="ts">
import { ref, computed, onBeforeMount } from 'vue';
import { api } from 'boot/axios';

const company = ref();
const filials = ref([]);

async function fetchCompanyInfo(){
  const r = await api.get('/api/company/');

  company.value = r.data.company;
  filials.value = r.data.filials;
}

onBeforeMount(async () => {
  await fetchCompanyInfo();
})
</script>

<template>
  <q-page>
    <diiv v-for="filial in filials" style="display: flex; flex-direction: row">
      <div>
        <a :href="'#/filials/' + filial.id">
        <h4>{{ filial.name }}</h4>
        </a>
      </div>
    </diiv>
  </q-page>
</template>