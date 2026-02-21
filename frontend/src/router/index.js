import { createRouter, createWebHistory } from 'vue-router'
import Admin from '../views/Admin.vue'
import Dashboard from '../views/Dashboard.vue'
import Management from '../views/Management.vue'
import Settings from '../views/Settings.vue'
import Repository from '../views/Repository.vue'

const routes = [
  {
    path: '/admin',
    name: 'Admin',
    component: Admin
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/management',
    name: 'Management',
    component: Management
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  },
  {
    path: '/repository',
    name: 'Repository',
    component: Repository
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router