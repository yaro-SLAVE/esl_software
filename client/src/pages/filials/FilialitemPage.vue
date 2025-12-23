<script setup lang="ts">
import axios from 'axios';
import { watch } from 'fs';
import { ref, computed, onBeforeMount } from 'vue';

type ActiveSquare = {
  row: number;
  col: number;
  rack_id: number | null;
  rack_number: number | null;
}

type MatrixSquare = {
  row: number;
  col: number;
  rack_id: number | null;
  rack_number: number | null;
}

const rows = ref(3);
const columns = ref(3);

const activeSquare = ref<ActiveSquare | null>(null);

const filialInfo = ref();

async function fetchRacks() {
  const r = await axios.get('/api/rack/?filial=1');
  console.log(r.data);
  filialInfo.value = r.data;
  rows.value = filialInfo.value.filial.rows;
  columns.value = filialInfo.value.filial.columns;

  filialInfo.value.racks.forEach((rack, index) => {
    matrix.value[rack.row][rack.column].rack_id = index;
    matrix.value[rack.row][rack.column].rack_number = rack.number;
    console.log(rack.number);
  });

  console.log(matrix.value);
}

onBeforeMount(async () => {
  await fetchRacks();
});

const matrix = computed(() => {
  const matrixArray: MatrixSquare[][] = [];
  
  for (let i = 0; i < rows.value; i++) {
    const row: MatrixSquare[] = [];
    for (let j = 0; j < columns.value; j++) {
      row.push({
        row: i,
        col: j,
        rack_id: null,
        rack_number: null
      });
    }
    matrixArray.push(row);
  }
  
  return matrixArray;
});

const selectSquare = (row: number, col: number) => {
  const square = matrix.value[row][col];
  activeSquare.value = {
    row,
    col,
    rack_id: square.rack_id,
    rack_number: square.rack_number
  };
};

const addRow = () => {
  rows.value++;
};

const addColumn = () => {
  columns.value++;
};

const removeRow = () => {
  if (rows.value > 1) {
    rows.value--;
    if (activeSquare.value && activeSquare.value.row >= rows.value) {
      activeSquare.value = null;
    }
  }
};

const removeColumn = () => {
  if (columns.value > 1) {
    columns.value--;
    if (activeSquare.value && activeSquare.value.col >= columns.value) {
      activeSquare.value = null;
    }
  }
};

const addRack = async () => {
  let formData = new FormData();
  FormData.append
};

</script>

<template>
  <q-page>
    <div style="display: grid; grid-template-columns: 2fr 1fr;">
      <div>
        <div 
          class="matrix-container q-mt-md"
          style="overflow: auto; max-height: 70vh; "
        >
          <div
            v-for="(row, rowIndex) in matrix"
            :key="rowIndex"
            class="row no-wrap"
          >
            <div
              v-for="(square, colIndex) in row"
              :key="colIndex"
              class="square-container"
            >
              <q-btn
                square
                class="square"
                :label="`${square.rack_number !== null ? square.rack_number : ''}`"
                :class="{ 'selected-square': square.rack_id !== null, 'active-square': activeSquare?.row === rowIndex && activeSquare?.col === colIndex }"
                @click="selectSquare(rowIndex, colIndex)"
              />
            </div>
          </div>
        </div>
      </div>
      
      <div>
        <div class="controls q-mt-xl">          
          <div class="row q-gutter-md">
            <q-btn
              color="primary"
              label="+ строка"
              @click="addRow"
              class="col-2"
            />
            <q-btn
              color="primary"
              label="+ столбец"
              @click="addColumn"
              class="col-2"
            />
            <q-btn
              color="negative"
              label="- строка"
              @click="removeRow"
              :disabled="rows <= 1"
              class="col-2"
            />
            <q-btn
              color="negative"
              label="- столбец"
              @click="removeColumn"
              :disabled="columns <= 1"
              class="col-2"
            />
          </div>

          <div v-if="activeSquare" style="margin: 15px">
            <h4>Сведения о стеллаже</h4>

            <div v-if="activeSquare.rack_id !== null">
              <span>IP адрес устройства: {{ filialInfo.racks[activeSquare.rack_id].esl_ip }}</span>
            </div>

            <div v-else>
              <span>Здесь не указанстеллаж</span>
              <q-btn
                color="primary"
                label="Добавить стеллаж"
                @click="addRack()"
              />
            </div>
          </div>
          
        </div>
      </div>
    </div>
  </q-page>
</template>

<style lang="scss">
  .square {
    width: 60px;
    height: 60px;
    background-color: #F4F2F2;
    margin: 8px;
    border-radius: 15%;
  }

  .selected-square {
    background-color: #A4A4A4;
  }

  .active-square {
    background-color: #8383F8;
  }
</style>