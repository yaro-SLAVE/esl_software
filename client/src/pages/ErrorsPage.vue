<script setup lang="ts">
import { ref } from 'vue';

// Определение интерфейса для объекта ошибки
interface ErrorItem {
  storeName: string;
  rackId: number;
  problemDescription: string;
}

// Имитация данных с картинки
const errorItems = ref<ErrorItem[]>([
  { storeName: 'Магазин 1', rackId: 5, problemDescription: 'Нет отклика от дисплея 1' },
]);
</script>

<template>
  <q-page>
    <!-- Список ошибок -->
    <div class="error-list-container">
      <div 
        v-for="(error, index) in errorItems" 
        :key="index"
        class="error-item row items-center q-px-xl q-mb-md"
      >
        <div class="col-3 text-body1 text-grey-10">
          {{ error.storeName }}
        </div>
        <div class="col-2 text-body1 text-grey-10">
          Стеллаж: <span class="text-weight-medium">{{ error.rackId }}</span>
        </div>
        <div class="col-7 text-body1 text-grey-10">
          Проблема: <span class="text-weight-medium">{{ error.problemDescription }}</span>
        </div>
      </div>
    </div>
  </q-page>
</template>

<style scoped>
/* Стили для линии подчеркивания шапки */
.border-bottom {
  border-bottom: 1px solid #000000;
}

/* Кнопка "Ошибки" с точно заданным цветом */
.errors-btn {
  background-color: #ff5252 !important;
  font-size: 16px;
}

/* Контейнер для центрирования списка, чтобы он не растягивался на весь экран */
.error-list-container {
  max-width: 900px;
  width: 100%;
}

/* Красные плашки ошибок */
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
