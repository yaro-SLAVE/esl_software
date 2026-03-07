import {route} from 'quasar/wrappers';
import {
  createMemoryHistory,
  createRouter,
  createWebHashHistory,
  createWebHistory,
} from 'vue-router';

import routes from './routes';
import useAuthStore from '../stores/authstore';
// import _ from "lodash";

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory);

  const Router = createRouter({
    scrollBehavior: () => ({left: 0, top: 0}),
    routes,
    history: createHistory(process.env.VUE_ROUTER_BASE),
  });

  Router.beforeEach((to, from, next) => {
    const userStore = useAuthStore();

    if (!userStore.is_auth && to.path != '/login') {
      next('/login');
    } else if (userStore.is_auth && to.path == '/login') {
      next('/profile')
    } else {
      next();
    }

    // if (mainStore.isAuthenticated && to.meta.permissions) {
    //   if (_.intersection(to.meta.permissions, mainStore.permissions).length > 0) {
    //     next()
    //     return;
    //   } else {
    //     next('/');
    //     return;
    //   }
    // }
    // next()
  })

  return Router;
});