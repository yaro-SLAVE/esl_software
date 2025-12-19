import type { RouteRecordRaw } from 'vue-router';
import FilialListPage from '../pages/filials/FilialListPage.vue';
import FilialItemPage from '../pages/filials/FilialItemPage.vue';
import AuthorizationPage from '../pages/AuthorizationPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/IndexPage.vue') }],
  },

  {
    path: '/filial',
    component: () => FilialListPage,
    children: [{ path: '/:id', component: () => FilialItemPage }],
  },

  {
    path: '/authorization',
    component: () => AuthorizationPage,
    children: [],
  },

  {
    path: '/profile',
    component: () => ProfilePage,
    children: [],
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
