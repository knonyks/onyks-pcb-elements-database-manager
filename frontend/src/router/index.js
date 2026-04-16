import { createRouter, createWebHistory } from 'vue-router'
import Admin from '../views/Admin.vue'
import Dashboard from '../views/Dashboard.vue'
import Management from '../views/Management.vue'
import Settings from '../views/Settings.vue'
import Repository from '../views/Repository.vue'
import Element_Create from '../views/Element_Create.vue'

const routes = [
  // {
  //   path: '/admin',
  //   name: 'Admin',
  //   component: Admin,
  //   meta: { title: 'Admin - ONYKS Blooodstone' }
  // },
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: 'Dashboard - ONYKS Blooodstone' }
  },
  {
    path: '/management',
    name: 'Management',
    component: Management,
    meta: { title: 'Management - ONYKS Blooodstone' }
  },
  // {
  //   path: '/settings',
  //   name: 'Settings',
  //   component: Settings,
  //   meta: { title: 'Settings - ONYKS Blooodstone' }
  // },
  {
    path: '/repository',
    name: 'Repository',
    component: Repository,
    meta: { title: 'Repository - ONYKS Blooodstone' }
  },
  // {
  //   path: '/element/create',
  //   name: 'Element_Create',
  //   component: Element_Create,
  //   meta: { title: 'Creating element - ONYKS Blooodstone' }
  // },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'ONYKS Blooodstone';
  next();
});

export default router