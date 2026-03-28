<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { RouterView, useRouter, useRoute } from 'vue-router'
import { NIcon } from 'naive-ui'
import { h } from 'vue'
import { HomeOutline, PersonOutline, DocumentTextOutline, CalendarOutline, BarChartOutline, SettingsOutline } from '@vicons/ionicons5'

const appTitle = 'BabyCare'
const router = useRouter()
const route = useRoute()

// 渲染图标
const renderIcon = (icon: any) => {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const menuOptions = [
  {
    label: '今日看板',
    key: 'home',
    icon: renderIcon(HomeOutline),
    iconStr: '🏠',
    color: 'from-blue-500 to-blue-600'
  },
  {
    label: '宝宝档案',
    key: 'baby-profile',
    icon: renderIcon(PersonOutline),
    iconStr: '👶',
    color: 'from-pink-500 to-rose-500'
  },
  {
    label: '任务管理',
    key: 'task-list',
    icon: renderIcon(DocumentTextOutline),
    iconStr: '📝',
    color: 'from-purple-500 to-violet-500'
  },
  {
    label: '日程',
    key: 'schedule',
    icon: renderIcon(CalendarOutline),
    iconStr: '📅',
    color: 'from-amber-500 to-orange-500'
  },
  {
    label: '数据分析',
    key: 'analytics',
    icon: renderIcon(BarChartOutline),
    iconStr: '📊',
    color: 'from-green-500 to-emerald-500'
  },
  {
    label: '设置',
    key: 'settings',
    icon: renderIcon(SettingsOutline),
    iconStr: '⚙️',
    color: 'from-gray-500 to-slate-500'
  }
]

const activeKey = computed(() => route.name as string)

// 动画变体
const menuVariants = {
  initial: { opacity: 0, x: -20 },
  enter: (index: number) => ({
    opacity: 1,
    x: 0,
    transition: {
      delay: index * 50,
      duration: 300,
      ease: 'easeOut'
    }
  })
}

function handleMenuUpdate(key: string) {
  router.push({ name: key })
}

function handleMobileNav(key: string) {
  router.push({ name: key })
}

// 响应式设计检测
const isMobile = ref(false)
const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<template>
  <n-message-provider>
    <n-layout>
      <n-layout has-sider>
        <!-- Sidebar - Desktop -->
        <n-layout-sider
          v-if="!isMobile"
          bordered
          collapse-mode="width"
          :collapsed-width="64"
          :width="220"
          :native-scrollbar="false"
          class="desktop-sidebar"
        >
          <!-- Logo -->
          <div class="sidebar-logo">
            <div class="logo-container">
              <div class="logo-icon">
                <span class="logo-emoji">🏠</span>
              </div>
              <h1 class="logo-text">{{ appTitle }}</h1>
            </div>
          </div>

          <!-- Menu -->
          <div class="sidebar-menu">
            <div
              v-for="(option, index) in menuOptions"
              :key="option.key"
              class="menu-item"
              :class="{ active: activeKey === option.key }"
              @click="handleMenuUpdate(option.key)"
            >
              <div class="menu-icon">
                <span class="menu-emoji">{{ option.iconStr }}</span>
              </div>
              <span class="menu-label">{{ option.label }}</span>
              <div
                v-if="activeKey === option.key"
                class="active-indicator"
                :class="option.color"
              ></div>
            </div>
          </div>
        </n-layout-sider>

        <!-- Main Content -->
        <n-layout-content :native-scrollbar="false" class="main-content">
          <div class="content-wrapper">
            <RouterView v-slot="{ Component }">
              <Transition name="page" mode="out-in">
                <component :is="Component" :key="route.name" />
              </Transition>
            </RouterView>
          </div>
        </n-layout-content>
      </n-layout>

      <!-- Bottom Navigation - Mobile -->
      <div v-if="isMobile" class="mobile-nav">
        <div
          v-for="(option, index) in menuOptions"
          :key="option.key"
          class="mobile-nav-item"
          :class="{ active: activeKey === option.key }"
          @click="handleMobileNav(option.key)"
        >
          <div class="nav-icon-wrapper">
            <span class="nav-icon">{{ option.iconStr }}</span>
            <div
              v-if="activeKey === option.key"
              class="nav-indicator"
              :class="option.color"
            ></div>
          </div>
          <span class="nav-label">{{ option.label }}</span>
        </div>
      </div>
    </n-layout>
  </n-message-provider>
</template>

<style scoped>
/* === Logo === */
.sidebar-logo {
  padding: 20px 16px;
  border-bottom: 1px solid #f0f0f0;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.logo-emoji {
  font-size: 20px;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

/* === Menu === */
.sidebar-menu {
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.menu-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  color: #666;
  animation: fadeInLeft 0.5s ease-out backwards;
}

.menu-item:nth-child(1) { animation-delay: 0.05s; }
.menu-item:nth-child(2) { animation-delay: 0.1s; }
.menu-item:nth-child(3) { animation-delay: 0.15s; }
.menu-item:nth-child(4) { animation-delay: 0.2s; }
.menu-item:nth-child(5) { animation-delay: 0.25s; }
.menu-item:nth-child(6) { animation-delay: 0.3s; }

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.menu-item:hover {
  background: #f5f5f5;
  transform: translateX(4px);
}

.menu-item.active {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  color: #0284c7;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(14, 165, 233, 0.15);
}

.menu-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
}

.menu-item:hover .menu-icon {
  transform: scale(1.1);
}

.menu-emoji {
  font-size: 18px;
}

.menu-label {
  flex: 1;
  font-size: 14px;
  font-weight: 500;
}

.active-indicator {
  position: absolute;
  right: 12px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.2);
  }
}

/* 渐变颜色 */
.from-blue-500 { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.from-pink-500 { background: linear-gradient(135deg, #ec4899, #f43f5e); }
.from-purple-500 { background: linear-gradient(135deg, #a855f7, #8b5cf6); }
.from-amber-500 { background: linear-gradient(135deg, #f59e0b, #f97316); }
.from-green-500 { background: linear-gradient(135deg, #22c55e, #10b981); }
.from-gray-500 { background: linear-gradient(135deg, #6b7280, #64748b); }

/* === Main Content === */
.desktop-sidebar {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  z-index: 1000;
  background: white;
}

.main-content {
  margin-left: 220px;
  min-height: 100vh;
  background: #fafafa;
}

.content-wrapper {
  padding: 24px;
  min-height: calc(100vh - 48px);
}

/* === Page Transition === */
.page-enter-active,
.page-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* === Mobile Navigation === */
.mobile-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  align-items: center;
  background: white;
  border-top: 1px solid #f0f0f0;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.08);
  padding: 8px 0 calc(8px + env(safe-area-inset-bottom));
  z-index: 2000;
}

.mobile-nav-item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  color: #999;
  flex: 1;
  animation: fadeInUp 0.5s ease-out backwards;
}

.mobile-nav-item:nth-child(1) { animation-delay: 0.05s; }
.mobile-nav-item:nth-child(2) { animation-delay: 0.1s; }
.mobile-nav-item:nth-child(3) { animation-delay: 0.15s; }
.mobile-nav-item:nth-child(4) { animation-delay: 0.2s; }
.mobile-nav-item:nth-child(5) { animation-delay: 0.25s; }
.mobile-nav-item:nth-child(6) { animation-delay: 0.3s; }

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.mobile-nav-item:active {
  transform: scale(0.92);
}

.mobile-nav-item.active {
  color: #0284c7;
}

.nav-icon-wrapper {
  position: relative;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: #f5f5f5;
  transition: all 0.3s;
}

.mobile-nav-item.active .nav-icon-wrapper {
  background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
  box-shadow: 0 4px 12px rgba(14, 165, 233, 0.2);
}

.nav-icon {
  font-size: 22px;
}

.nav-indicator {
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 3px;
  border-radius: 2px;
}

.nav-label {
  font-size: 11px;
  font-weight: 500;
  margin-top: 2px;
}

/* === Responsive === */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }

  .content-wrapper {
    padding: 16px 16px 100px 16px;
  }
}

@media (min-width: 769px) {
  .mobile-nav {
    display: none;
  }
}

@media (max-width: 768px) {
  .desktop-sidebar {
    display: none;
  }
}
</style>
