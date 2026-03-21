<script setup lang="ts">
import { useBabyStore } from '@/stores/baby'

const babyStore = useBabyStore()

onMounted(() => {
  // TODO: Load current baby
})
</script>

<template>
  <div class="home-container">
    <!-- Header -->
    <header class="header">
      <h1>📊 今日看板</h1>
      <n-date-picker v-model:value="selectedDate" />
    </header>

    <!-- Baby Info Card -->
    <n-card v-if="currentBaby" class="baby-card">
      <div class="baby-header">
        <div class="baby-info">
          <h2>👶 {{ currentBaby.nickname || currentBaby.name }}</h2>
          <n-tag type="info">{{ currentBaby.age_months }} 个月</n-tag>
        </div>
        <n-button @click="switchBaby">切换宝宝</n-button>
      </div>
    </n-card>

    <!-- Today's Overview -->
    <n-card class="overview-card">
      <template #header>
        <h3>📊 今日概览</h3>
      </template>

      <div class="overview-stats">
        <div class="stat-item">
          <span class="stat-label">已完成</span>
          <span class="stat-value">{{ completedTasks }}/{{ totalTasks }}</span>
          <n-progress
            type="line"
            :percentage="completionRate"
            :show-indicator="false"
            :height="8"
          />
        </div>

        <div class="stat-item">
          <span class="stat-label">妈妈疲劳度</span>
          <n-progress
            type="line"
            :percentage="momFatigue * 100"
            :color="getFatigueColor(momFatigue)"
            :height="8"
          />
          <span class="stat-value">{{ momFatigue.toFixed(2) }}</span>
        </div>

        <div class="stat-item">
          <span class="stat-label">爸爸疲劳度</span>
          <n-progress
            type="line"
            :percentage="dadFatigue * 100"
            :color="getFatigueColor(dadFatigue)"
            :height="8"
          />
          <span class="stat-value">{{ dadFatigue.toFixed(2) }}</span>
        </div>
      </div>
    </n-card>

    <!-- Tasks by Time Slot -->
    <div class="time-slots">
      <n-card
        v-for="slot in timeSlots"
        :key="slot.code"
        class="time-slot-card"
      >
        <template #header>
          <h3>{{ slot.icon }} {{ slot.name }} ({{ slot.time }})</h3>
        </template>

        <div class="task-list">
          <div
            v-for="task in getTasksBySlot(slot.code)"
            :key="task.id"
            class="task-item"
            :class="{ completed: task.status === 'completed' }"
          >
            <div class="task-info">
              <span class="task-name">{{ task.name }}</span>
              <span class="task-meta">
                {{ task.category }} | {{ task.duration_minutes }}min
                <span v-if="task.assigned_to_detail">
                  | {{ task.assigned_to_detail.name }}
                </span>
              </span>
            </div>
            <div class="task-actions">
              <n-button
                v-if="task.status === 'pending'"
                size="small"
                type="success"
                @click="completeTask(task)"
              >
                ✓
              </n-button>
              <n-tag v-else type="success">已完成</n-tag>
            </div>
          </div>
        </div>
      </n-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useBabyStore } from '@/stores/baby'
import { useTaskStore } from '@/stores/task'
import { useRouter } from 'vue-router'
import type { Task, TimeSlot } from '@/types'
import api from '@/api/client'

const router = useRouter()
const babyStore = useBabyStore()
const taskStore = useTaskStore()

const currentBaby = computed(() => babyStore.currentBaby)
const loading = ref(false)

const selectedDate = ref(new Date().toISOString().split('T')[0])
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

// Using task store data
const allTasks = computed(() => taskStore.tasks)
const totalTasks = computed(() => allTasks.value.length)
const completedTasksCount = computed(() => taskStore.completedTasks.length)
const completionRate = computed(() => {
  if (totalTasks.value === 0) return 0
  return (completedTasksCount.value / totalTasks.value) * 100
})

onMounted(async () => {
  loading.value = true
  try {
    // Load babies if not loaded
    if (!babyStore.babies.length) {
      await babyStore.fetchBabies()
    }

    // Set current baby if not set
    if (!currentBaby.value && babyStore.babies.length > 0) {
      babyStore.setCurrentBaby(babyStore.babies[0])
    }

    // Load tasks for current baby
    if (currentBaby.value) {
      await taskStore.fetchTasks({
        baby_id: currentBaby.value.id,
        date: selectedDate.value
      })
    }

    // Load fatigue data (mock for now)
    // TODO: Implement real fatigue API call
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

function switchBaby() {
  router.push('/baby-profile')
}

async function completeTask(task: Task) {
  await taskStore.completeTask(task.id)
}
</script>

<style scoped>
.home-container {
  padding: var(--spacing-md);
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.header h1 {
  font-size: 28px;
  font-weight: 600;
}

.baby-card {
  margin-bottom: var(--spacing-md);
}

.baby-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.baby-info h2 {
  font-size: 24px;
  margin: 0;
}

.overview-card {
  margin-bottom: var(--spacing-md);
}

.overview-stats {
  display: grid;
  gap: var(--spacing-md);
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.stat-value {
  font-size: 18px;
  font-weight: 600;
}

.time-slots {
  display: grid;
  gap: var(--spacing-md);
}

.time-slot-card {
  margin-bottom: var(--spacing-md);
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm);
  border-radius: var(--radius-md);
  transition: background-color var(--transition-fast);
}

.task-item:hover {
  background-color: var(--bg-tertiary);
}

.task-item.completed {
  opacity: 0.6;
}

.task-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.task-name {
  font-weight: 600;
  font-size: 16px;
}

.task-meta {
  font-size: 14px;
  color: var(--text-secondary);
}

.task-actions {
  display: flex;
  gap: var(--spacing-sm);
}
</style>
