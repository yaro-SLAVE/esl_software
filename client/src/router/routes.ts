import type { RouteRecordRaw } from 'vue-router';
import FilialListPage from '../pages/filials/FilialListPage.vue';
import FilialItemPage from '../pages/filials/FilialItemPage.vue';
import AuthorizationPage from '../pages/AuthorizationPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import ProductShowPage from '../pages/ProductShowPage.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => FilialItemPage  }], //import('pages/IndexPage.vue')
  },

  {
    path: '/filials',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => FilialListPage },
      { path: '/:id', component: () => FilialItemPage }
    ],
  },

  {
    path: '/authorization',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => AuthorizationPage},
    ],
  },

  {
    path: '/profile',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => ProfilePage },
    ],
  },

  {
    path: '/product/:barcode',
    component: () => ProductShowPage,
    children: [
    ],
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
