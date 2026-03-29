<script setup lang="ts">
import { ref, computed, onBeforeMount } from 'vue';
import { api } from 'boot/axios';
import { useQuasar } from 'quasar';
import type {CompanyOrFilial, Integration} from '../types';

const $q = useQuasar();

$q.loading.show();

const integration = ref<Integration>();

const company = ref<CompanyOrFilial>({
  name: null,
  id: null
});
const filials = ref<[CompanyOrFilial]>([]);

async function fetchCompanyInfo(){
  const r = await api.get('/api/company/');

  company.value = r.data.company;
  filials.value = r.data.filials;
}

async function fetchIntegrationInfo(){
  const r = await api.get(`/api/integration/2/`);

  integration.value = r.data;
}

onBeforeMount(async () => {
  await fetchCompanyInfo();
  await fetchIntegrationInfo();
  $q.loading.hide();
});
</script>

<template>
  <q-page>
    <div v-if="integration?.integration_url !== null">
    <h5>{{ company.name }}</h5>

    <diiv style="display: flex; flex-direction: row; gap: 20px">
      <q-btn
        v-for="filial in filials"
        class="filial"
        :label="filial.name"
        :href="'#/filials/' + filial.id"
      />
    </diiv>
    </div>
    <div v-else>
      <h5>Еще не добавлена интеграция, невозможно получить информацию о филиалах</h5>
    </div>
  </q-page>
</template>

<style lang="scss">
  .filial {
    width: 250px;
    height: 120px;
    background-color: #F4F2F2;
    margin: 8px;
    border-radius: 15px;
  }
</style>