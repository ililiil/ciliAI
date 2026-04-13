import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: { title: '控制台', icon: 'Odometer' }
      },
      {
        path: 'invite-codes',
        name: 'InviteCodes',
        component: () => import('../views/InviteCodes.vue'),
        meta: { title: '邀请码管理', icon: 'Ticket' }
      },
      {
        path: 'works',
        name: 'Works',
        component: () => import('../views/Works.vue'),
        meta: { title: '作品管理', icon: 'Picture' }
      },
      {
        path: 'order-management',
        name: 'OrderManagement',
        component: () => import('../views/OrderManagement.vue'),
        meta: { title: '接单管理', icon: 'Document' }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('../views/Users.vue'),
        meta: { title: '用户管理', icon: 'User' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || 'CiliAI'} - 后台管理`
  const token = localStorage.getItem('admin_token')
  if (to.path !== '/login' && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
