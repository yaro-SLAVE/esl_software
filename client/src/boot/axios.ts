import {boot} from 'quasar/wrappers';
import axios, {AxiosInstance} from 'axios';
import qs from 'qs';
import { useAuthStore } from 'src/stores/authstore';

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
    $api: AxiosInstance;
  }
}

const api = axios.create({
  ...(process.env.DEV ? {baseURL: "/"} : {baseURL: "/"}),
  paramsSerializer: params => {
    return qs.stringify(params, {
      arrayFormat: "comma"
    })
  }
});

api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    const token = authStore.jwt;
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default boot(({app}) => {

  app.config.globalProperties.$axios = axios;

  app.config.globalProperties.$api = api;

});

export {api};