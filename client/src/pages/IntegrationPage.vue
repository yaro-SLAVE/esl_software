<script setup lang="ts">
import { ref, computed, onBeforeMount } from 'vue';
import { api } from 'boot/axios';
import { useAuthStore } from '../stores/authstore';
import type {Integration, IntegrationToUpdateCreate} from '../types';

const authStore = useAuthStore();

const integration = ref<Integration>();

const showIntegration = ref(false);

const integrationToCreateUpdate = ref<IntegrationToUpdateCreate>({
    login: '',
    password: '',
    type: integration.value?.integration_type,
    url: integration.value?.integration_url,
    start_time: integration.value?.start_time,
    end_time: integration.value?.end_time,
    polling_frequency: integration.value?.polling_frequency
  });

async function fetchIntegrationInfo(){
  const r = await api.get(`/api/integration/2/`);

  console.log(r.data);

  integration.value = r.data;
}

onBeforeMount(async () => {
  await fetchIntegrationInfo();
});

async function createUpdateIntegration() {
  let formData = new FormData();
  formData.append('login', integrationToCreateUpdate.value.login);
  formData.append('password', integrationToCreateUpdate.value.password);
  formData.append('url', integrationToCreateUpdate.value.url);
  formData.append('polling_frequency', integrationToCreateUpdate.value.polling_frequency);
  formData.append('start_time', integrationToCreateUpdate.value.start_time);
  formData.append('end_time', integrationToCreateUpdate.value.end_time);

  if (integration.value?.integration_url === null) {
    const r = await api.post('/api/integration/', formData);
  } else {
    const r = await api.put('/api/integration/2/', formData);
  }

  await fetchIntegrationInfo();

  showIntegration.value = false;
}

async function deleteIntegration() {
  const r = await api.delete('/api/integration/2/');

  await fetchIntegrationInfo();
}
</script>


<template>
  <q-page>
    <div v-if="integration?.integration_url === null">
      <q-btn
        label="Создать интеграцию"
        color="primary"
        @click="showIntegration = true"
      />
    </div>

    <div v-else style="display: flex; flex-direction: column; padding: 10px">
      <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 20px; align-items: center; margin: 20px">
        <div style="display: flex; flex-direction: column">
          <span>URL-адрес</span>
          <span>Периодичность обновлений</span>
          <span>Время обновлений</span>
        </div>

        <div style="display: flex; flex-direction: column">
          <span>{{ integration?.integration_url }}</span>
          <span>раз в {{ integration?.polling_frequency }} секунд</span>
          <span>с {{ integration?.start_time }} до {{ integration?.end_time }}</span>
        </div>
      </div>

      <div style="display: flex; flex-direction: row; gap: 25px">
        <q-btn
          color="primary"
          label="Изменить"
          @click="showIntegration = true"
        />

        <q-btn
          color="deep-orange"
          label="Удалить"
          @click="deleteIntegration"
        />
      </div>
    </div>

    <q-dialog v-model="showIntegration">
      <q-card style="width: 500px; max-width: 80vw;">
        <q-card-section>
          <div class="text-h6">Настройка интеграции</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 10px; margin: 10px; align-items: center; justify-content: center;">
            <span>Логин</span>
            <q-input
              v-model="integrationToCreateUpdate.login"
              type="text"
            />
          </div>

          <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 10px; margin: 10px; align-items: center; justify-content: center;">
            <span>Пароль</span>
            <q-input
              v-model="integrationToCreateUpdate.password"
              type="password"
            />
          </div>

          <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 10px; margin: 10px; align-items: center; justify-content: center;">
            <span>URL</span>
            <q-input
              v-model="integrationToCreateUpdate.url"
              type="text"
            />
          </div>

          <div style="display: grid; grid-template-columns: 3fr 2fr 1fr; gap: 10px; margin: 10px; align-items: center; justify-content: center;">
            <span>Периодичность опросов раз в </span>
            <q-input
              v-model="integrationToCreateUpdate.polling_frequency"
              type="number"
            />
            <span>секунд</span>
          </div>

          <div style="display: grid; grid-template-columns: 3fr 2fr auto 2fr; align-items: center; justify-content: center; gap: 12px; margin: 10px">
            <span>Время обновлений с </span>
            <q-input
              v-model="integrationToCreateUpdate.start_time"
              type="time"
            />
            <span> до </span>
            <q-input
              v-model="integrationToCreateUpdate.end_time"
              type="time"
            />
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn label="Сохранить" color="primary" @click="createUpdateIntegration" />
          <q-btn label="Отмена" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>