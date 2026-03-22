<script setup lang="ts">
import { h } from 'vue'
import { RouterView } from 'vue-router'

const appTitle = 'BabyCare'
</script>

<template>
  <n-layout>
    <n-layout has-sider>
      <!-- Sidebar -->
      <n-layout-sider
        bordered
        collapse-mode="width"
        :collapsed-width="64"
        :width="200"
        :native-scrollbar="false"
      >
        <div class="sidebar-header">
          <h2 class="app-title">🏠 {{ appTitle }}</h2>
        </div>

        <n-menu
          :routes="[
            {
              label: '今日看板',
              name: 'home',
              icon: () => h('span', '📊')
            },
            {
              label: '宝宝档案',
              name: 'baby-profile',
              icon: () => h('span', '👶')
            },
            {
              label: '任务管理',
              name: 'task-list',
              icon: () => h('span', '📝')
            },
            {
              label: '日程',
              name: 'schedule',
              icon: () => h('span', '📅')
            },
            {
              label: '数据分析',
              name: 'analytics',
              icon: () => h('span', '📈')
            },
            {
              label: '设置',
              name: 'settings',
              icon: () => h('span', '⚙️')
            }
          ]"
          :value="($route.name as string)"
          @update:value="($router.push($event as string))"
        />
      </n-layout-sider>

      <!-- Main Content -->
      <n-layout-content :native-scrollbar="false">
        <RouterView />
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<style scoped>
.sidebar-header {
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
}

.app-title {
  font-size: 20px;
  font-weight: 600;
}
</style>
