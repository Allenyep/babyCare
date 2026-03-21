import { createRouter } from 'vue-router'
import { createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue'),
      meta: { title: '今日看板' }
    },
    {
      path: '/baby',
      name: 'baby-profile',
      component: () => import('../views/BabyProfile.vue'),
      meta: { title: '宝宝档案' }
    },
    {
      path: '/tasks',
      name: 'task-list',
      component: () => import('../views/TaskList.vue'),
      meta: { title: '任务管理' }
    },
    {
      path: '/schedule',
      name: 'schedule',
      component: () => import('../views/Schedule.vue'),
      meta: { title: '日程' }
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: () => import('../views/Analytics.vue'),
      meta: { title: '数据分析' }
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../views/Settings.vue'),
      meta: { title: '设置' }
    }
  ]
})

export default router
