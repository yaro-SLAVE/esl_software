<script setup lang="ts">
import { ref, computed, onBeforeMount, onBeforeUnmount } from 'vue';
import { api } from 'boot/axios';

const errors = ref([]);
const errorTimer = ref(null);

async function fetchErrors() {
  const r = await api.get(`/api/esl/error/`);
  errors.value = r.data;
}

onBeforeMount(async () => {
  
  await fetchErrors();
  errorTimer.value = setInterval(fetchErrors, 10000);
});

onBeforeUnmount(() => {
  if (errorTimer.value) {
    clearInterval(errorTimer.value);
  }
});


</script>

<template>
  <q-page>
    <div class="error-list-container">
      <div 
        v-for="(error, index) in errors" 
        :key="index"
        class="error-item row items-center q-px-xl q-mb-md"
      >
        <div class="col-3 text-body1 text-grey-10">
          {{ error.esl.rack.filial.short_name }}
        </div>
        <div class="col-2 text-body1 text-grey-10">
          Стеллаж: <span class="text-weight-medium">{{ error.esl.rack.number }}</span>
        </div>
        <div class="col-2 text-body1 text-grey-10">
          Номер дисплея: <span class="text-weight-medium">{{ error.channel }}</span>
        </div>
      </div>
    </div>
  </q-page>
</template>

<style scoped>
.error-list-container {
  max-width: 900px;
  width: 100%;
}

.error-item {
  background-color: #ec7063;
  border: 1px solid #cb4335;
  border-radius: 12px;
  height: 75px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.error-item:hover {
  transform: translateY(-1px);
}
</style>
