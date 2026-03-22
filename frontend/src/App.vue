<script setup lang="ts">
import { h, computed } from 'vue'
import { RouterView, useRouter, useRoute } from 'vue-router'

const appTitle = 'BabyCare'
const router = useRouter()
const route = useRoute()

const renderIcon = (icon: string) => {
  return () => h('span', icon)
}

const menuOptions = [
  {
    label: '今日看板',
    key: 'home',
    icon: renderIcon('📊'),
    iconStr: '📊'
  },
  {
    label: '宝宝档案',
    key: 'baby-profile',
    icon: renderIcon('👶'),
    iconStr: '👶'
  },
  {
    label: '任务管理',
    key: 'task-list',
    icon: renderIcon('📝'),
    iconStr: '📝'
  },
  {
    label: '日程',
    key: 'schedule',
    icon: renderIcon('📅'),
    iconStr: '📅'
  },
  {
    label: '数据分析',
    key: 'analytics',
    icon: renderIcon('📈'),
    iconStr: '📈'
  },
  {
    label: '设置',
    key: 'settings',
    icon: renderIcon('⚙️'),
    iconStr: '⚙️'
  }
]

const activeKey = computed(() => route.name as string)

function handleMenuUpdate(key: string) {
  // Navigate by route name
  router.push({ name: key })
}

function handleMobileNav(key: string) {
  router.push({ name: key })
}
</script>

<template>
  <n-layout>
    <n-layout has-sider>
      <!-- Sidebar - Desktop only (hidden on mobile via CSS) -->
      <n-layout-sider
        bordered
        collapse-mode="width"
        :collapsed-width="64"
        :width="200"
        :native-scrollbar="false"
        class="desktop-sidebar"
      >
        <div class="sidebar-header">
          <h2 class="app-title">🏠 {{ appTitle }}</h2>
        </div>

        <n-menu
          :options="menuOptions"
          :value="activeKey"
          @update:value="handleMenuUpdate"
        />
      </n-layout-sider>

      <!-- Main Content -->
      <n-layout-content :native-scrollbar="false" class="main-content">
        <RouterView />
      </n-layout-content>
    </n-layout>

    <!-- Bottom Navigation - Mobile only (visible on mobile via CSS) -->
    <div class="mobile-nav">
      <div
        v-for="option in menuOptions"
        :key="option.key"
        class="mobile-nav-item"
        :class="{ active: activeKey === option.key }"
        @click="handleMobileNav(option.key)"
      >
        <span class="mobile-nav-icon">{{ option.iconStr }}</span>
        <span class="mobile-nav-label">{{ option.label }}</span>
      </div>
    </div>
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

.desktop-sidebar {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  z-index: 10;
}

.main-content {
  margin-left: 200px;
  min-height: 100vh;
  padding: var(--spacing-md);
}

/* Mobile Bottom Navigation */
.mobile-nav {
  display: none; /* Hidden on desktop by default */
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  justify-content: space-around;
  align-items: center;
  background: white;
  border-top: 1px solid var(--border-color);
  padding: 8px 0;
  z-index: 1000;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
}

.mobile-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 4px 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-secondary);
  flex: 1;
}

.mobile-nav-item.active {
  color: var(--primary-color);
}

.mobile-nav-icon {
  font-size: 20px;
}

.mobile-nav-label {
  font-size: 10px;
}

/* Mobile Responsive - Apply CSS media queries */
@media (max-width: 768px) {
  .desktop-sidebar {
    display: none;
  }

  .main-content {
    margin-left: 0;
    padding: var(--spacing-sm);
    padding-bottom: 80px; /* More space for bottom nav + content */
    min-height: calc(100vh - 60px); /* Ensure content is visible */
  }

  .mobile-nav {
    display: flex;
    padding-bottom: env(safe-area-inset-bottom, 8px);
    height: 60px;
  }
}

/* iPad adaptation */
@media (min-width: 769px) and (max-width: 1024px) {
  .desktop-sidebar {
    width: 180px;
  }

  .main-content {
    margin-left: 180px;
  }
}
</style>
