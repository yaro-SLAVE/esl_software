<script setup lang="ts">
import { ref, onBeforeMount  } from 'vue';
import { useRoute } from 'vue-router';
import useAuthStore from '../stores/authstore';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();

const router = useRouter();

const username = ref('');
const password = ref('');

async function loginUser() {
  const r = await authStore.login(username.value, password.value);
  if (r) {
    router.push('/');
  }
}

</script>

<template>
  <q-page>
    <div class="login-container">
      <div class="login-form">
        <span>Авторизация в системе</span>
        <q-input
          label="Логин"
          type="text"
          v-model="username"
        />
        <q-input
          label="Пароль"
          type="text"
          v-model="password"
        />
        <q-btn
          label="Войти"
          color="primary"
          @click="loginUser"
        />
      </div>
    </div>
  </q-page>
</template>

<style lang="scss">
  .login-container {
    display: flex; 
    justify-content: center; 
    align-items: center; 
    height: 100vh;
  }

  .login-form {
    display: flex; 
    flex-direction: column; 
    justify-content: center; 
    align-items: center; 
    gap: 15px;
    padding: 15px;
    border: 2px solid grey;
    border-radius: 10px;
    font-size: 20px;
  }
</style>