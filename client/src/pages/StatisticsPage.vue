<script setup class="ts">
import { ref } from 'vue';
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top',
      align: 'end',
      labels: {
        usePointStyle: false,
        boxWidth: 40,
        boxHeight: 12
      }
    }
  },
  scales: {
    x: {
      grid: { display: false },
      title: {
        display: true,
        text: 'Даты',
        align: 'end',
        font: { size: 12 }
      }
    },
    y: {
      grid: { display: false },
      ticks: { display: false },
      title: {
        display: true,
        text: 'Количество',
        align: 'end',
        font: { size: 12 }
      }
    }
  }
});

const updateChartData = ref({
  labels: ['20.05.2026', '20.05.2026'],
  datasets: [
    {
      label: 'Успешные',
      borderColor: '#2196F3',
      backgroundColor: '#2196F3',
      data: [1, 1],
      tension: 0.1,
      pointRadius: 0
    },
    {
      label: 'Неудачные',
      borderColor: '#F44336',
      backgroundColor: '#F44336',
      data: [0, 0],
      tension: 0.1,
      pointRadius: 0
    }
  ]
});

const errorChartData = ref({
  labels: ['20.05.2026', '20.05.2026'],
  datasets: [
    {
      label: 'Количество ошибок',
      borderColor: '#F44336',
      backgroundColor: '#F44336',
      data: [1, 1],
      tension: 0.1,
      pointRadius: 0
    }
  ]
});
</script>

<template>
  <q-page>
    <div class="row q-col-gutter-md q-mb-md">
      <div class="col-12 col-md-3">
        <q-card flat bordered class="full-height rounded-borders">
          <q-card-section>
            <div class="text-subtitle1 text-grey-8 q-mb-sm">Магазины</div>
            <div class="text-body1">Всего: <span class="text-weight-bold">1</span></div>
            <div class="text-body1">Проблемных: <span class="text-weight-bold">1</span></div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-3">
        <q-card flat bordered class="full-height rounded-borders">
          <q-card-section>
            <div class="text-subtitle1 text-grey-8 q-mb-sm">Товары</div>
            <div class="text-body1">Всего: <span class="text-weight-bold">3</span></div>
            <div class="text-body1 text-no-wrap">
              Контролируются ценниками: <span class="text-weight-bold">1</span>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-3">
        <q-card flat bordered class="full-height rounded-borders">
          <q-card-section>
            <div class="text-subtitle1 text-grey-8 q-mb-sm">Устройства</div>
            <div class="text-body1">Всего: <span class="text-weight-bold">1</span></div>
            <div class="text-body1">Проблемных: <span class="text-weight-bold">1</span></div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-3">
        <q-card flat bordered class="bg-grey-3 full-height rounded-borders">
          <q-card-section class="q-gutter-y-sm">
            <div class="text-subtitle1 text-grey-9 text-weight-medium">Фильтры</div>
            
            <div class="row items-center justify-between no-wrap">
              <span class="text-body2 text-grey-8 q-mr-sm">Период</span>
              <div class="row items-center no-wrap bg-grey-5 rounded-borders q-px-sm" style="height: 32px; width: 120px;">
                <span class="text-white text-center full-width">-</span>
              </div>
            </div>

            <div class="row items-center justify-between no-wrap">
              <span class="text-body2 text-grey-8 q-mr-sm">Магазины</span>
              <div class="row items-center justify-between bg-grey-5 rounded-borders q-px-sm text-white cursor-pointer" style="height: 32px; width: 120px;">
                <span></span>
                <q-icon name="chevron_left" size="xs" />
              </div>
            </div>

            <div class="row justify-end q-mt-sm">
              <q-btn unelevated no-caps color="indigo-5" text-color="white" label="Выгрузка в Excel" class="full-width q-py-xs" />
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <div class="row q-col-gutter-md">
      <div class="col-12 col-md-6">
        <q-card flat bordered class="rounded-borders">
          <q-card-section>
            <div class="text-h6 text-grey-9 q-mb-md text-weight-regular">Обновление</div>
            <div style="height: 300px; position: relative;">
              <Line :data="updateChartData" :options="chartOptions" />
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-6">
        <q-card flat bordered class="rounded-borders">
          <q-card-section>
            <div class="text-h6 text-grey-9 q-mb-md text-weight-regular">Ошибки устройств</div>
            <div style="height: 300px; position: relative;">
              <Line :data="errorChartData" :options="chartOptions" />
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<style scoped>
.custom-tab {
  background-color: #757575 !important;
  border-radius: 4px;
}
.rounded-borders {
  border-radius: 8px !important;
  border: 1px solid #bdc3c7 !important;
}
</style>
