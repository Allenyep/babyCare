<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useBabyStore } from '@/stores/baby'
import { useTaskStore } from '@/stores/task'
import { useRouter } from 'vue-router'
import type { Task } from '@/types'

const router = useRouter()
const babyStore = useBabyStore()
const taskStore = useTaskStore()

const currentBaby = computed(() => babyStore.currentBaby)
const loading = ref(false)

// DatePicker timestamp
const selectedDateTimestamp = ref(new Date().getTime())
const selectedDateString = computed(() => {
  return new Date(selectedDateTimestamp.value).toISOString().split('T')[0]
})

const momFatigue = ref(0.35)
const dadFatigue = ref(0.25)

const timeSlots = [
  { code: 'early', name: '早间', icon: '🌅', time: '06:00-09:00' },
  { code: 'morning', name: '上午', icon: '☀️', time: '09:00-12:00' },
  { code: 'noon', name: '中午', icon: '🌞', time: '12:00-15:00' },
  { code: 'afternoon', name: '下午', icon: '🌤', time: '15:00-18:00' },
  { code: 'evening', name: '晚上', icon: '🌆', time: '18:00-21:00' },
  { code: 'night', name: '夜间', icon: '🌙', time: '21:00-06:00' }
]

const allTasks = computed(() => taskStore.tasks)
const totalTasks = computed(() => allTasks.value.length)
const completedTasksCount = computed(() => taskStore.completedTasks.length)
const completionRate = computed(() => {
  if (totalTasks.value === 0) return 0
  return Math.round((completedTasksCount.value / totalTasks.value) * 100)
})

// 动画变体
const cardVariants = {
  initial: { opacity: 0, y: 30 },
  enter: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 500,
      ease: 'easeOut'
    }
  }
}

const statVariants = {
  initial: { scale: 0.8, opacity: 0 },
  enter: {
    scale: 1,
    opacity: 1,
    transition: {
      duration: 400,
      ease: 'easeOut'
    }
  }
}

onMounted(async () => {
  loading.value = true
  try {
    if (!babyStore.babies.length) {
      await babyStore.fetchBabies()
    }

    if (!currentBaby.value && babyStore.babies.length > 0) {
      babyStore.setCurrentBaby(babyStore.babies[0])
    }

    if (currentBaby.value) {
      await taskStore.fetchTasks({
        baby_id: currentBaby.value.id,
        date: selectedDateString.value
      })
    }
  } catch (error) {
    console.error('Failed to load data:', error)
  } finally {
    loading.value = false
  }
})

function getTasksBySlot(slotCode: string) {
  return allTasks.value.filter(t => t.time_slot === slotCode)
}

function getFatigueColor(score: number) {
  if (score < 0.3) return '#10B981'
  if (score < 0.5) return '#F59E0B'
  if (score < 0.8) return '#F97316'
  return '#EF4444'
}

function getCategoryType(category: string) {
  const types: Record<string, any> = {
    'feeding': 'success',
    'diaper': 'info',
    'education': 'warning',
    'food': 'error',
    'medical': 'default'
  }
  return types[category] || 'default'
}

function switchBaby() {
  router.push('/baby-profile')
}

async function completeTask(task: Task) {
  await taskStore.completeTask(task.id)
}
</script>

<template>
  <div class="home-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else class="content-grid">
      <!-- Header -->
      <header
        class="header"
        v-motion
        :initial="{ opacity: 0, y: -20 }"
        :enter="{ opacity: 1, y: 0, transition: { duration: 400 } }"
      >
        <div class="header-left">
          <h1>📊 今日看板</h1>
          <p class="subtitle">{{ selectedDateString }}</p>
        </div>
        <div class="header-right">
          <n-date-picker v-model:value="selectedDateTimestamp" type="date" />
        </div>
      </header>

      <!-- Baby Info Card -->
      <section
        v-if="currentBaby"
        class="baby-section"
        v-motion="cardVariants"
      >
        <div class="baby-card">
          <div class="baby-avatar">
            <span class="avatar-text">{{ (currentBaby.nickname || currentBaby.name).charAt(0) }}</span>
          </div>
          <div class="baby-info">
            <h2>{{ currentBaby.nickname || currentBaby.name }}</h2>
            <div class="baby-meta">
              <span class="age-badge">{{ currentBaby.age_months }} 个月</span>
              <span class="gender-badge">
                {{ currentBaby.gender === 'male' ? '男宝宝' : '女宝宝' }}
              </span>
            </div>
          </div>
          <n-button @click="switchBaby" secondary>
            切换
          </n-button>
        </div>
      </section>

      <!-- Stats Cards -->
      <section class="stats-section">
        <div
          class="stat-card stat-primary"
          v-motion="statVariants"
          :delay="100"
        >
          <div class="stat-icon">
            ✅
          </div>
          <div class="stat-content">
            <p class="stat-label">已完成任务</p>
            <p class="stat-value">{{ completedTasksCount }}/{{ totalTasks }}</p>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${completionRate}%` }"></div>
            </div>
            <p class="stat-percent">{{ completionRate }}%</p>
          </div>
        </div>

        <div
          class="stat-card stat-warning"
          v-motion="statVariants"
          :delay="200"
        >
          <div class="stat-icon">
            👩
          </div>
          <div class="stat-content">
            <p class="stat-label">妈妈疲劳度</p>
            <p class="stat-value">{{ (momFatigue * 100).toFixed(0) }}%</p>
            <div class="progress-bar">
              <div
                class="progress-fill"
                :style="{ width: `${momFatigue * 100}%`, background: getFatigueColor(momFatigue) }"
              ></div>
            </div>
          </div>
        </div>

        <div
          class="stat-card stat-info"
          v-motion="statVariants"
          :delay="300"
        >
          <div class="stat-icon">
            👨
          </div>
          <div class="stat-content">
            <p class="stat-label">爸爸疲劳度</p>
            <p class="stat-value">{{ (dadFatigue * 100).toFixed(0) }}%</p>
            <div class="progress-bar">
              <div
                class="progress-fill"
                :style="{ width: `${dadFatigue * 100}%`, background: getFatigueColor(dadFatigue) }"
              ></div>
            </div>
          </div>
        </div>
      </section>

      <!-- Quick Actions -->
      <section
        class="actions-section"
        v-motion="cardVariants"
        :delay="400"
      >
        <div class="actions-card">
          <h3>⚡ 快捷操作</h3>
          <div class="actions-grid">
            <button class="action-btn" @click="router.push('/task-list')">
              <span class="action-icon">📝</span>
              <span>添加任务</span>
            </button>
            <button class="action-btn" @click="router.push('/schedule')">
              <span class="action-icon">📅</span>
              <span>查看日程</span>
            </button>
            <button class="action-btn" @click="router.push('/analytics')">
              <span class="action-icon">📊</span>
              <span>数据分析</span>
            </button>
          </div>
        </div>
      </section>

      <!-- Tasks Timeline -->
      <section
        class="timeline-section"
        v-motion="cardVariants"
        :delay="500"
      >
        <div class="timeline-card">
          <div class="card-header">
            <h3>📋 今日任务</h3>
            <n-button text @click="router.push('/task-list')">
              查看全部 →
            </n-button>
          </div>

          <div class="timeline-container">
            <div v-for="slot in timeSlots" :key="slot.code" class="time-slot">
              <div class="slot-header">
                <span class="slot-icon">{{ slot.icon }}</span>
                <div class="slot-info">
                  <span class="slot-name">{{ slot.name }}</span>
                  <span class="slot-time">{{ slot.time }}</span>
                </div>
              </div>

              <div class="slot-tasks">
                <n-list v-if="getTasksBySlot(slot.code).length > 0" hoverable clickable>
                  <n-list-item
                    v-for="task in getTasksBySlot(slot.code)"
                    :key="task.id"
                    class="task-item"
                    :class="{ completed: task.status === 'completed' }"
                    @click="completeTask(task)"
                  >
                    <template #prefix>
                      <n-checkbox
                        :checked="task.status === 'completed'"
                        @click.stop="completeTask(task)"
                      />
                    </template>
                    <div class="task-content">
                      <p class="task-name">{{ task.name }}</p>
                      <p v-if="task.description" class="task-desc">{{ task.description }}</p>
                    </div>
                    <template #suffix>
                      <n-tag v-if="task.category" size="small" :type="getCategoryType(task.category)">
                        {{ task.category }}
                      </n-tag>
                    </template>
                  </n-list-item>
                </n-list>
                <div v-else class="empty-slot">
                  <p>暂无任务</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 1400px;
  margin: 0 auto;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  gap: 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.content-grid {
  display: grid;
  gap: 24px;
  grid-template-columns: 2fr 1fr;
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

/* === Header === */
.header {
  grid-column: 1 / -1;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  flex-wrap: wrap;
}

.header-left h1 {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 4px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 14px;
  color: #999;
  margin: 0;
}

/* === Baby Card === */
.baby-section {
  grid-column: 1 / -1;
}

.baby-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
}

.baby-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.avatar-text {
  font-size: 28px;
  font-weight: 700;
  color: white;
}

.baby-info {
  flex: 1;
}

.baby-info h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 700;
}

.baby-meta {
  display: flex;
  gap: 12px;
}

.age-badge,
.gender-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

.age-badge {
  background: #e0f2fe;
  color: #0284c7;
}

.gender-badge {
  background: #fce7f3;
  color: #db2777;
}

/* === Stats Section === */
.stats-section {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}

.stat-card {
  padding: 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
  display: flex;
  gap: 16px;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
}

.stat-primary .stat-icon {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
}

.stat-warning .stat-icon {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
}

.stat-info .stat-icon {
  background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
}

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-label {
  font-size: 13px;
  color: #999;
  margin: 0 0 8px 0;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 12px 0;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.stat-percent {
  font-size: 12px;
  color: #999;
  margin: 0;
  text-align: right;
}

/* === Actions Section === */
.actions-section {
  grid-column: 1 / -1;
}

.actions-card {
  padding: 24px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
}

.actions-card h3 {
  margin: 0 0 20px 0;
  font-size: 18px;
  font-weight: 600;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 20px;
  background: #f9fafb;
  border: 2px solid #f3f4f6;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.action-btn:hover {
  background: white;
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.action-btn:active {
  transform: scale(0.96);
}

.action-icon {
  font-size: 32px;
}

/* === Timeline Section === */
.timeline-section {
  grid-column: 1 / -1;
}

.timeline-card {
  padding: 24px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.timeline-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.time-slot {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.slot-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f3f4f6;
}

.slot-icon {
  font-size: 24px;
}

.slot-info {
  display: flex;
  flex-direction: column;
}

.slot-name {
  font-weight: 600;
  font-size: 16px;
}

.slot-time {
  font-size: 12px;
  color: #999;
}

.slot-tasks {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.task-item {
  transition: all 0.2s;
}

.task-item:hover {
  background: #f9fafb;
}

.task-item.completed {
  opacity: 0.6;
}

.task-item.completed .task-name {
  text-decoration: line-through;
}

.task-content {
  flex: 1;
}

.task-name {
  margin: 0 0 4px 0;
  font-weight: 500;
}

.task-desc {
  margin: 0;
  font-size: 13px;
  color: #999;
}

.empty-slot {
  text-align: center;
  padding: 20px;
  color: #ccc;
  font-style: italic;
  background: #f9fafb;
  border-radius: 10px;
  font-size: 14px;
}

/* === Mobile Responsive === */
@media (max-width: 768px) {
  .content-grid {
    gap: 16px;
  }

  .header {
    flex-direction: column;
  }

  .header-left h1 {
    font-size: 24px;
  }

  .baby-card {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }

  .baby-meta {
    justify-content: center;
  }

  .stats-section {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
