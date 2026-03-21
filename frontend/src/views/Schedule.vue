<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Task, TimeSlot } from '@/types'

const selectedDate = ref(new Date().toISOString().split('T')[0])
const viewMode = ref<'day' | 'week'>('day')

const timeSlots: { code: TimeSlot; name: string; icon: string; time: string }[] = [
  { code: 'early', name: '早间', icon: '🌅', time: '06:00-09:00' },
  { code: 'morning', name: '上午', icon: '☀️', time: '09:00-12:00' },
  { code: 'noon', name: '中午', icon: '🌞', time: '12:00-15:00' },
  { code: 'afternoon', name: '下午', icon: '🌤', time: '15:00-18:00' },
  { code: 'evening', name: '晚上', icon: '🌆', time: '18:00-21:00' },
  { code: 'night', name: '夜间', icon: '🌙', time: '21:00-06:00' }
]

// Mock schedule data - TODO: Replace with API calls
const scheduleTasks = ref<Task[]>([
  {
    id: 1,
    baby_id: 1,
    name: '喂奶',
    category: 'feeding' as any,
    description: '早餐奶',
    duration_minutes: 20,
    priority: 9,
    date: new Date().toISOString().split('T')[0],
    time_slot: 'early' as any,
    assigned_to: 1,
    assigned_to_detail: { id: 1, name: '妈妈' },
    status: 'completed' as any
  },
  {
    id: 2,
    baby_id: 1,
    name: '换尿布',
    category: 'diaper' as any,
    description: '晨间换尿布',
    duration_minutes: 5,
    priority: 9,
    date: new Date().toISOString().split('T')[0],
    time_slot: 'early' as any,
    assigned_to: 2,
    assigned_to_detail: { id: 2, name: '爸爸' },
    status: 'completed' as any
  },
  {
    id: 3,
    baby_id: 1,
    name: '积木游戏',
    category: 'education' as any,
    description: '堆积木，锻炼精细动作',
    duration_minutes: 30,
    priority: 6,
    date: new Date().toISOString().split('T')[0],
    time_slot: 'morning' as any,
    assigned_to: 2,
    assigned_to_detail: { id: 2, name: '爸爸' },
    status: 'pending' as any
  },
  {
    id: 4,
    baby_id: 1,
    name: '午睡',
    category: 'hygiene' as any,
    description: '中午午睡2小时',
    duration_minutes: 120,
    priority: 8,
    date: new Date().toISOString().split('T')[0],
    time_slot: 'noon' as any,
    assigned_to: 1,
    assigned_to_detail: { id: 1, name: '妈妈' },
    status: 'pending' as any
  },
  {
    id: 5,
    baby_id: 1,
    name: '户外活动',
    category: 'outdoor' as any,
    description: '公园散步，晒太阳',
    duration_minutes: 60,
    priority: 5,
    date: new Date().toISOString().split('T')[0],
    time_slot: 'afternoon' as any,
    assigned_to: 2,
    assigned_to_detail: { id: 2, name: '爸爸' },
    status: 'pending' as any
  },
  {
    id: 6,
    baby_id: 1,
    name: '辅食喂养',
    category: 'food' as any,
    description: '蔬菜泥',
    duration_minutes: 30,
    priority: 8,
    date: new Date().toISOString().split('T')[0],
    time_slot: 'evening' as any,
    assigned_to: 1,
    assigned_to_detail: { id: 1, name: '妈妈' },
    status: 'pending' as any
  }
])

const tasksBySlot = computed(() => {
  const result: Record<TimeSlot, Task[]> = {
    early: [],
    morning: [],
    noon: [],
    afternoon: [],
    evening: [],
    night: []
  }

  scheduleTasks.value.forEach(task => {
    if (task.time_slot) {
      result[task.time_slot].push(task)
    }
  })

  return result
})

function getSlotProgress(slotCode: TimeSlot): number {
  const tasks = tasksBySlot.value[slotCode]
  if (tasks.length === 0) return 0
  const completed = tasks.filter(t => t.status === 'completed').length
  return (completed / tasks.length) * 100
}

function getSlotColor(slotCode: TimeSlot): string {
  const progress = getSlotProgress(slotCode)
  if (progress === 100) return '#10B981'
  if (progress > 0) return '#F59E0B'
  return '#E5E7EB'
}

function completeTask(task: Task) {
  task.status = 'completed' as any
  // TODO: API call
}

function editTask(task: Task) {
  console.log('Edit task:', task)
  // TODO: Open edit modal
}

function getAssigneeColor(name: string): string {
  return name === '妈妈' ? '#EC4899' : '#3B82F6'
}
</script>

<template>
  <div class="schedule-container">
    <!-- Header -->
    <header class="header">
      <h1>📅 日程安排</h1>
      <n-space>
        <n-radio-group v-model:value="viewMode">
          <n-radio-button value="day">日视图</n-radio-button>
          <n-radio-button value="week">周视图</n-radio-button>
        </n-radio-group>
        <n-date-picker v-model:value="selectedDate" />
      </n-space>
    </header>

    <!-- Day View -->
    <div v-if="viewMode === 'day'" class="day-view">
      <n-card
        v-for="slot in timeSlots"
        :key="slot.code"
        class="time-slot-card"
        :class="{
          'has-tasks': tasksBySlot[slot.code].length > 0,
          'completed': getSlotProgress(slot.code) === 100
        }"
      >
        <template #header>
          <div class="slot-header">
            <div class="slot-title">
              <span class="slot-icon">{{ slot.icon }}</span>
              <div>
                <h3>{{ slot.name }}</h3>
                <span class="slot-time">{{ slot.time }}</span>
              </div>
            </div>
            <div class="slot-progress">
              <n-progress
                type="circle"
                :percentage="getSlotProgress(slot.code)"
                :color="getSlotColor(slot.code)"
                :stroke-width="6"
                :show-indicator="false"
                :width="40"
              />
              <span class="progress-text">{{ Math.round(getSlotProgress(slot.code)) }}%</span>
            </div>
          </div>
        </template>

        <div v-if="tasksBySlot[slot.code].length === 0" class="empty-slot">
          <span class="empty-icon">💤</span>
          <span class="empty-text">暂无安排</span>
        </div>

        <div v-else class="slot-tasks">
          <div
            v-for="task in tasksBySlot[slot.code]"
            :key="task.id"
            class="schedule-task"
            :class="{ completed: task.status === 'completed' }"
            :style="{ borderLeftColor: getAssigneeColor(task.assigned_to_detail?.name || '') }"
          >
            <div class="task-header">
              <div class="task-title">
                <span class="task-name">{{ task.name }}</span>
                <n-tag :type="getCategoryTag(task.category)" size="small">
                  {{ getCategoryLabel(task.category) }}
                </n-tag>
              </div>
              <div class="task-actions">
                <n-button
                  v-if="task.status === 'pending'"
                  size="tiny"
                  type="success"
                  @click="completeTask(task)"
                >
                  ✓
                </n-button>
                <n-button
                  size="tiny"
                  text
                  @click="editTask(task)"
                >
                  ✏️
                </n-button>
              </div>
            </div>

            <div v-if="task.description" class="task-description">
              {{ task.description }}
            </div>

            <div class="task-footer">
              <div class="task-meta">
                <span>⏱ {{ task.duration_minutes }}分钟</span>
                <span>⭐ {{ task.priority }}</span>
              </div>
              <div class="task-assignee">
                <span
                  class="assignee-badge"
                  :style="{ backgroundColor: getAssigneeColor(task.assigned_to_detail?.name || '') }"
                >
                  {{ task.assigned_to_detail?.name || '未分配' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </n-card>
    </div>

    <!-- Week View -->
    <div v-else class="week-view">
      <n-card class="week-overview">
        <template #header>
          <h3>本周概览</h3>
        </template>
        <div class="week-stats">
          <div class="stat-card">
            <span class="stat-label">本周任务</span>
            <span class="stat-value">42</span>
          </div>
          <div class="stat-card">
            <span class="stat-label">已完成</span>
            <span class="stat-value success">18</span>
          </div>
          <div class="stat-card">
            <span class="stat-label">待完成</span>
            <span class="stat-value warning">24</span>
          </div>
        </div>
      </n-card>
      <div class="week-placeholder">
        <p>周视图开发中...</p>
        <p class="placeholder-tip">将显示周历视图和任务统计</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
function getCategoryTag(category: string): string {
  const tags: Record<string, string> = {
    feeding: 'success',
    diaper: 'info',
    education: 'warning',
    food: 'error',
    outdoor: 'default',
    hygiene: 'info',
    medical: 'error'
  }
  return tags[category] || 'default'
}

function getCategoryLabel(category: string): string {
  const labels: Record<string, string> = {
    feeding: '喂奶',
    diaper: '换尿布',
    education: '早教',
    food: '辅食',
    outdoor: '户外',
    hygiene: '清洁',
    medical: '医疗'
  }
  return labels[category] || category
}
</script>

<style scoped>
.schedule-container {
  padding: var(--spacing-md);
  max-width: 1400px;
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
  margin: 0;
}

.day-view {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: var(--spacing-md);
}

.time-slot-card {
  transition: all var(--transition-fast);
}

.time-slot-card:hover {
  box-shadow: var(--shadow-md);
}

.time-slot-card.completed {
  opacity: 0.7;
  background: var(--bg-secondary);
}

.slot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.slot-title {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

.slot-icon {
  font-size: 32px;
}

.slot-title h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.slot-time {
  font-size: 14px;
  color: var(--text-tertiary);
}

.slot-progress {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.progress-text {
  font-size: 14px;
  font-weight: 600;
}

.empty-slot {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xl) 0;
  color: var(--text-tertiary);
}

.empty-icon {
  font-size: 48px;
  opacity: 0.5;
}

.empty-text {
  font-size: 14px;
}

.slot-tasks {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.schedule-task {
  padding: var(--spacing-md);
  border-left: 4px solid;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.schedule-task:hover {
  background: var(--bg-secondary);
}

.schedule-task.completed {
  opacity: 0.6;
  text-decoration: line-through;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-sm);
}

.task-title {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.task-name {
  font-weight: 600;
  font-size: 16px;
}

.task-actions {
  display: flex;
  gap: var(--spacing-xs);
}

.task-description {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-sm);
}

.task-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-meta {
  display: flex;
  gap: var(--spacing-md);
  font-size: 14px;
  color: var(--text-tertiary);
}

.assignee-badge {
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  color: white;
  font-size: 12px;
  font-weight: 600;
}

.week-view {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.week-overview {
  margin-bottom: var(--spacing-md);
}

.week-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-md);
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  padding: var(--spacing-md);
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
}

.stat-value.success {
  color: #10B981;
}

.stat-value.warning {
  color: #F59E0B;
}

.week-placeholder {
  text-align: center;
  padding: var(--spacing-xxl) 0;
  color: var(--text-tertiary);
}

.placeholder-tip {
  font-size: 14px;
  margin-top: var(--spacing-sm);
}
</style>
