<script setup lang="ts">
import { api } from 'boot/axios';
import { ref, computed, onBeforeMount } from 'vue';
import { useRoute } from 'vue-router';

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

const route = useRoute();

const filialId = ref(route.params.id);

const rows = ref(3);
const columns = ref(3);

const activeSquare = ref<ActiveSquare | null>(null);

const filialInfo = ref();

const showProduct = ref(false);

const products = ref([]);

const productToUpdate = ref();

const showRack = ref(false);
const rackToAdd = ref();
const rackNumberToCreate = ref();

async function fetchRacks() {
  const r = await api.get('/api/rack/?filial=1');
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
  const r = await api.get('/api/product/');

  products.value = r.data;

  console.log(r.data);
}

// async function fetchFilialInfo() {
//   const r = await api.get(`/api/filial/${filialId.value}`);

//   filialInfo.value = r.data;

//   console.log(r.data);
// }

onBeforeMount(async () => {
  
  await fetchRacks();
  await fetchProducts();
  //await fetchFilialInfo();
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
      if (rack.row !== null && rack.column !== null) {
        matrix.value[rack.row][rack.column].rack_id = index;
        matrix.value[rack.row][rack.column].rack_number = rack.number;
      }
    });
  }
  
  return matrixArray;
});

const freeRacks = computed(() => {
  let data = [];

  if (filialInfo.value !== undefined) {
    filialInfo.value.racks.forEach(rack => {
      if (rack.col === null || rack.row === null) {
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

async function updateFilial() {
  const r = await api.put(`/api/filial/${filialId.value}/`, {
    rows: rows.value,
    columns: columns.value,
  });
}

const selectSquare = (row: number, col: number) => {
  const square = matrix.value[row][col];
  activeSquare.value = {
    row,
    col,
    rack_id: square.rack_id,
    rack_number: square.rack_number
  };
};

const addRow = async () => {
  rows.value++;
  await updateFilial();
};

const addColumn = async () => {
  columns.value++;
  await updateFilial();
};

const removeRow = async () => {
  if (rows.value > 1) {
    rows.value--;
    if (activeSquare.value && activeSquare.value.row >= rows.value) {
      activeSquare.value = null;
    }
    await updateFilial();
  }
};

const removeColumn = async () => {
  if (columns.value > 1) {
    columns.value--;
    if (activeSquare.value && activeSquare.value.col >= columns.value) {
      activeSquare.value = null;
    }
    await updateFilial();
  }
};

async function addRack(){
  let formData = new FormData();
  formData.append('row', activeSquare.value.row);
  formData.append('column', activeSquare.value.col);

  const r = await api.put(`/api/rack/${rackToAdd.value}/`, formData);

  showRack.value = false;

  rackToAdd.value = undefined;

  await fetchRacks();

  filialInfo.value.racks.forEach((rack, index) => {
    if (rack.row === activeSquare.value.row && activeSquare.value.col == rack.column) {
      activeSquare.value.rack_id = index;
      activeSquare.value.rack_number = rack.number;
    }
  });
}

async function createRack(){
  let formData = new FormData();
  formData.append('row', activeSquare.value.row);
  formData.append('column', activeSquare.value.col);
  formData.append('number', rackNumberToCreate.value);
  formData.append('filial', filialId.value);

  const r = await api.post(`/api/rack/`, formData);

  showRack.value = false;

  rackNumberToCreate.value = undefined;

  await fetchRacks();

  filialInfo.value.racks.forEach((rack, index) => {
    if (rack.row === activeSquare.value.row && activeSquare.value.col == rack.column) {
      activeSquare.value.rack_id = index;
      activeSquare.value.rack_number = rack.number;
    }
  });
}

async function deleteRack(id: number) {
  await api.delete(`/api/rack/${id}/`);
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

  const r = await api.put(`/api/rack/${id}/`, body, {
    headers: {
      "Content-Type": "application/json"
    }
  });

  showProduct.value = false;

  await fetchProducts();
  await fetchRacks();
}

</script>

<template>
  <q-page>
    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 10px">
      <div style="display: flex; flex-direction: column;">
        <div class="row">
          <q-btn
            href="#/filials"
            label="Назад"
          />
        </div>

        <div style="display: flex; flex-direction: row; align-items: center">
          <div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
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

            <div style="display: flex; flex-direction: row">
              <q-btn
                label="+"
                @click="addRow"
                class="col-2"
              />
              <q-btn
                label="-"
                @click="removeRow"
                :disabled="columns <= 1"
                class="col-2"
              />
            </div>
          </div>

          <div style="display: flex; flex-direction: column">
            <q-btn
              label="+"
              @click="addColumn"
              class="col-2"
            />
            <q-btn
              label="-"
              @click="removeColumn"
              :disabled="columns <= 1"
              class="col-2"
            />
          </div>
        </div>
      </div>
      
      <div>
        <div class="controls q-mt-xl">          
          <div v-if="activeSquare" style="display: flex; flex-direction: column; margin: 15px; gap: 20px">
            <q-btn
              color="primary"
              label="Обновить информацию на ценниках"
            />

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
                <q-btn
                  v-if="filialInfo.racks[activeSquare.rack_id].products.length === 0"
                  square
                  class="product"
                  label="Добавить продукт"
                  @click="showProduct = true"
                />
              </div>
            </div>

            <div v-else>
              <span>Здесь не указан стеллаж</span>

              <br>

              <q-btn
                color="primary"
                label="Добавить стеллаж"
                @click="showRack = true"
              />
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
          <div style="display: grid; grid-template-columns: 3fr auto; gap: 10px; margin: 10px">
            <q-input
              v-model="rackNumberToCreate"
              label="№ стеллажа"
              type="number"
            />
            <q-btn label="Создать" color="primary" @click="createRack()" />
          </div>

          <q-separator/>

          <div style="display: grid; grid-template-columns: 3fr auto; gap: 10px; margin: 10px">
            <q-select
              v-model="rackToAdd"
              :options="freeRacks"
              label="Выберите стеллаж"
              option-label="number"
              option-value="id"
              emit-value
            />
            <q-btn label="Выбрать" color="primary" @click="addRack()" />
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Отмена" color="primary" v-close-popup />
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