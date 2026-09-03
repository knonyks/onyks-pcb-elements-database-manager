import DashboardView from '@/views/DashboardView.vue';
import ManagementView from '@/views/ManagementView.vue';
import RepositoryView from '@/views/RepositoryView.vue';
import { createRouter, createWebHistory } from 'vue-router'
import ErrorView from '@/views/ErrorView.vue';
import ElementView from '@/views/ElementView.vue';
import LoginView from '@/views/LoginView.vue';
import ManagerView from '@/views/ManagerView.vue';
import AdminView from '@/views/AdminView.vue';
import SettingsView from '@/views/SettingsView.vue';

const routes = [
  {
    path: '/',
    redirect: 'manager/dashboard'
  },
  {
    path: '/login',
    component: LoginView,
    name: 'Login',
    meta: { title: 'Login - ONYKS Bloodstone' }
  },
  {
    path: '/manager',
    component: ManagerView,
    children: 
    [
      {
        path: 'dashboard',
        component: DashboardView,
        meta: { title: 'Dashboard - ONYKS Bloodstone' }
      },
      {
        path: 'management',
        component: ManagementView,
        meta: { title: 'Management - ONYKS Bloodstone' }
      },
      {
        path: 'repository',
        component: RepositoryView,
        meta: { title: 'Repository - ONYKS Bloodstone' }
      },
      {
        path: 'admin',
        component: AdminView,
        meta: { title: 'Admin - ONYKS Bloodstone' }
      },
      {
        path: 'settings',
        component: SettingsView,
        meta: { title: 'Settings - ONYKS Bloodstone' }
      },

      {
        path: 'element/add',
        component: ElementView,
        meta: { title: 'Add an element - ONYKS Bloodstone' },
        props: { type: 'add' }
      },
      {
        path: 'element/details/:uuid',
        component: ElementView,
        meta: { title: 'Element details - ONYKS Bloodstone' },
        props: { type: 'details' }
      },
      {
        path: 'element/edit/:uuid',
        component: ElementView,
        meta: { title: 'Edit an element - ONYKS Bloodstone' },
        props: { type: 'edit' }
      },
      {
        path: 'element/duplicate/:uuid',
        component: ElementView,
        meta: { title: 'Duplicate an element - ONYKS Bloodstone' },
        props: { type: 'duplicate' }
      },
    ]
  },
  {
    path: '/error',
    component: ErrorView,
    meta: { title: 'Error! - ONYKS Bloodstone' },
  }
]

const router = createRouter(
{
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => 
{
  document.title = to.meta.title || 'ONYKS Bloodstone';
  next();
});

export default router