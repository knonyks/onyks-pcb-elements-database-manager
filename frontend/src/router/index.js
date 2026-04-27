import DashboardView from '@/views/DashboardView.vue';
import ManagementView from '@/views/ManagementView.vue';
import RepositoryView from '@/views/RepositoryView.vue';
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/dashboard',
    name: 'DashboardView',
    component: DashboardView,
    meta: { title: 'Dashboard - ONYKS Bloodstone' }
  },
  {
    path: '/management',
    name: 'ManagementView',
    component: ManagementView,
    meta: { title: 'Management - ONYKS Bloodstone' }
  },
  {
    path: '/repository',
    name: 'RepositoryView',
    component: RepositoryView,
    meta: { title: 'Repository - ONYKS Bloodstone' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'ONYKS Bloodstone';
  next();
});

export default router