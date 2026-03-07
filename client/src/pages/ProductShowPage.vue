<script setup lang="ts">
import axios from 'axios';
import { ref, onBeforeMount  } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const product = ref();

async function getProduct() {
    const company_id = route.params.company_id;
    const product_id = route.params.product_id;

    const r = await axios.get(`/api/product/show/${company_id}/${product_id}/`);

    product.value = r.data;


}

onBeforeMount(async () => {
    await getProduct();
})
</script>

<template>
  <div class="text-center">
    <h5>{{product.short_name}}</h5>
    <br>
    <h5>{{product.price}}</h5>
    <br>
    <h5>{{product.description}}</h5>
    </div>
</template>