import type { RouteRecordRaw } from 'vue-router';
import FilialsListPage from '../pages/FilialsListPage.vue';
import FilialItemPage from '../pages/FilialItemPage.vue';
import AuthorizationPage from '../pages/AuthorizationPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import ProductShowPage from '../pages/ProductShowPage.vue'
import IndexPage from "../pages/IndexPage.vue"
import IntegrationPage from '../pages/IntegrationPage.vue';
import StatisticsPage from 'src/pages/StatisticsPage.vue';
import ErrorsPage from 'src/pages/ErrorsPage.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => IndexPage  }],
  },

  {
    path: '/filials',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => FilialsListPage },
      { path: ':id', component: () => FilialItemPage }
    ],
  },
  {
    path: '/integrations',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => IntegrationPage }
    ]
  },

  {
    path: '/login',
    component: () => import('layouts/EmptyLayout.vue'),
    children: [
      { path: '', component: () => AuthorizationPage},
    ],
  },

  {
    path: '/statistics',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => StatisticsPage },
    ],
  },

  {
    path: '/errors',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => ErrorsPage },
    ],
  },

  {
    path: '/product/:company_id/:product_id',
    component: () => ProductShowPage,
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
