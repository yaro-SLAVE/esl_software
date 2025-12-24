<script setup lang="ts">
import axios from 'axios';
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

const showProduct = ref(false);

const products = ref([]);

const productToUpdate = ref();

const showRack = ref(false);
const rackToAdd = ref();

async function fetchRacks() {
  const r = await axios.get('/api/rack/?filial=1');
  console.log(r.data);
  filialInfo.value = r.data;
  rows.value = filialInfo.value.filial.rows;
  columns.value = filialInfo.value.filial.columns;

  filialInfo.value.racks.forEach((rack, index) => {
    matrix.value[rack.row][rack.column].rack_id = index;
    matrix.value[rack.row][rack.column].rack_number = rack.number;
  });

  console.log(matrix.value);
}

async function fetchProducts() {
  const r = await axios.get('/api/product/');

  products.value = r.data;

  console.log(r.data);
}

onBeforeMount(async () => {
  await fetchRacks();
  await fetchProducts();
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

  if (filialInfo.value !== undefined) {
    filialInfo.value.racks.forEach((rack, index) => {
      matrix.value[rack.row][rack.column].rack_id = index;
      matrix.value[rack.row][rack.column].rack_number = rack.number;
    });
  }
  
  return matrixArray;
});

const freeRacks = computed(() => {
  let data = [];

  if (filialInfo.value !== undefined) {
    filialInfo.value.racks.forEach(rack => {
      if (rack.col === -1 || rack.row === -1) {
        data.push(rack);
      }
    });
  }

  console.log(data);

  return data;
});

const freeProducts = computed(() => {
  let data = [];

  if (products.value !== []) {
    products.value.forEach(product => {
      if (product.rack === null) {
        data.push(product);
      }
    });
  }

  return data;
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

async function addRack(){
  let formData = new FormData();
  formData.append('row', activeSquare.value.row);
  formData.append('column', activeSquare.value.col);

  const r = await axios.put(`/api/rack/${rackToAdd.value}/`, formData);

  showRack.value = false;

  await fetchRacks();

  filialInfo.value.racks.forEach((rack, index) => {
    if (rack.row === activeSquare.value.row && activeSquare.value.col == rack.column) {
      activeSquare.value.rack_id = index;
      activeSquare.value.rack_number = rack.number;
    }
  });
}

async function deleteRack(id: number) {
  await axios.delete(`/api/rack/${id}/`);
  await fetchRacks();
  activeSquare.value.rack_id = null;
  activeSquare.value.rack_number = null;
}

async function updateProduct(){
  const dataArray = [{
    id: productToUpdate.value,
    shelf: 0,
    number: 0
  }];

  const body = {
    products: dataArray
  }

  const id = filialInfo.value.racks[activeSquare.value.rack_id].id;

  const r = await axios.put(`/api/rack/${id}/`, body, {
    headers: {
      "Content-Type": "application/json"
    }
  });

  showProduct.value = false;

  await fetchProducts();
}

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

              <q-btn
                color="negative"
                label="убрать стеллаж"
                @click="deleteRack(filialInfo.racks[activeSquare.rack_id].id)"
              />

              <div>
                <h5>Продукты:</h5>

                <div v-for="product in filialInfo.racks[activeSquare.rack_id].products">
                  <q-btn
                    square
                    class="product"
                    :label="`${product.short_name}`"
                    @click="showProduct = true"
                  />
                </div>
              </div>
            </div>

            <div v-else>
              <span>Здесь не указан стеллаж</span>

              <br>

              <q-btn
                v-if="freeRacks.length !== 0"
                color="primary"
                label="Добавить стеллаж"
                @click="showRack = true"
              />
              <span v-else>Доступных стеллажей нет</span>
            </div>
          </div>
          
        </div>
      </div>
    </div>

    <q-dialog v-model="showProduct">
      <q-card style="width: 500px; max-width: 80vw;">
        <q-card-section>
          <div class="text-h6">Изменение продукта</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-select
            v-model="productToUpdate"
            :options="freeProducts"
            label="Выберите продукт"
            option-label="short_name"
            option-value="id"
            emit-value
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" v-close-popup />
          <q-btn label="OK" color="primary" @click="updateProduct()" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="showRack">
      <q-card style="width: 500px; max-width: 80vw;">
        <q-card-section>
          <div class="text-h6">Добавление стеллажа</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-select
            v-model="rackToAdd"
            :options="freeRacks"
            label="Выберите стеллаж"
            option-label="number"
            option-value="id"
            emit-value
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" v-close-popup />
          <q-btn label="OK" color="primary" @click="addRack()" />
        </q-card-actions>
      </q-card>
    </q-dialog>
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

  .product {
    width: 90px;
    height: 90px;
    background-color: #F4F2F2;
    margin: 8px;
    border-radius: 15%;
  }
</style>