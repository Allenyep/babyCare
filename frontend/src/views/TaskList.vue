<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Task, TaskStatus } from '@/types'
import { h } from 'vue'

// Mock data - TODO: Replace with API calls
const tasks = ref<Task[]>([
  {
    id: 1,
    baby_id: 1,
    name: '喂奶',
    category: 'feeding' as any,
    description: '早餐奶',
    duration_minutes: 20,
    priority: 9,
    date: '2026-03-20',
    time_slot: 'early' as any,
    assigned_to: 1,
    assigned_to_detail: { id: 1, name: '妈妈' },
    status: 'completed' as any
  },
  {
    id: 2,
    baby_id: 1,
    name: '积木游戏',
    category: 'education' as any,
    description: '堆积木，锻炼精细动作',
    duration_minutes: 30,
    priority: 6,
    date: '2026-03-20',
    time_slot: 'morning' as any,
    assigned_to: 2,
    assigned_to_detail: { id: 2, name: '爸爸' },
    status: 'pending' as any
  }
])

// Store timestamp for DatePicker
const selectedDateTimestamp = ref(new Date().getTime())
const selectedDateString = computed(() => {
  return new Date(selectedDateTimestamp.value).toISOString().split('T')[0]
})

// Filters
const statusFilter = ref<TaskStatus | 'all'>('all')

const filteredTasks = computed(() => {
  if (statusFilter.value === 'all') return tasks.value
  return tasks.value.filter(t => t.status === statusFilter.value)
})

// Animation variants
const headerVariants = {
  initial: { opacity: 0, y: -20 },
  enter: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 400,
      ease: 'easeOut'
    }
  }
}

const taskVariants = {
  initial: { opacity: 0, y: 20 },
  enter: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 300,
      ease: 'easeOut'
    }
  }
}

function completeTask(task: Task) {
  task.status = 'completed' as TaskStatus
  // TODO: API call
}

function deleteTask(task: Task) {
  // TODO: API call
}

function createTask() {
  // TODO: Open task creation modal
}

function getCategoryTag(category: string) {
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

function getCategoryIcon(category: string): string {
  const icons: Record<string, string> = {
    feeding: '🍼',
    diaper: '👶',
    education: '📚',
    food: '🥣',
    outdoor: '🌳',
    hygiene: '🛁',
    medical: '💊'
  }
  return icons[category] || '📋'
}

function getPriorityColor(priority: number): string {
  if (priority >= 8) return '#ef4444'
  if (priority >= 5) return '#f59e0b'
  return '#10b981'
}
</script>

<template>
  <div class="tasks-container">
    <!-- Header -->
    <header
      class="header"
      v-motion="headerVariants"
    >
      <div class="header-left">
        <h1>📝 任务管理</h1>
        <p class="subtitle">管理宝宝日常护理任务</p>
      </div>
      <n-button type="primary" size="large" @click="createTask">
        + 添加任务
      </n-button>
    </header>

    <!-- Filters -->
    <n-card class="filters-card" v-motion="taskVariants" :delay="100">
      <div class="filters-content">
        <div class="filter-group">
          <span class="filter-label">📅 日期</span>
          <n-date-picker v-model:value="selectedDateTimestamp" type="date" size="large" />
        </div>
        <div class="filter-group">
          <span class="filter-label">📊 状态</span>
          <n-select
            v-model:value="statusFilter"
            :options="[
              { value: 'all', label: '全部任务' },
              { value: 'pending', label: '待完成' },
              { value: 'completed', label: '已完成' }
            ]"
            style="width: 150px"
            size="large"
          />
        </div>
      </div>
    </n-card>

    <!-- Task List -->
    <n-card class="tasks-card" v-motion="taskVariants" :delay="200">
      <div v-if="filteredTasks.length === 0" class="empty-state">
        <span class="empty-icon">📋</span>
        <p>暂无任务</p>
        <n-button @click="createTask" type="primary" ghost>
          + 创建第一个任务
        </n-button>
      </div>

      <div v-else class="tasks-list">
        <div
          v-for="(task, index) in filteredTasks"
          :key="task.id"
          class="task-card"
          :class="{ completed: task.status === 'completed' }"
          v-motion="taskVariants"
          :delay="index * 80"
        >
          <div class="task-main">
            <div class="task-icon">
              {{ getCategoryIcon(task.category) }}
            </div>

            <div class="task-content">
              <div class="task-header">
                <div class="task-title">
                  <h3>{{ task.name }}</h3>
                  <span class="task-date">{{ task.date }}</span>
                </div>
                <n-tag :type="getCategoryTag(task.category)" size="small">
                  {{ getCategoryLabel(task.category) }}
                </n-tag>
              </div>

              <div v-if="task.description" class="task-description">
                {{ task.description }}
              </div>

              <div class="task-meta">
                <div class="meta-item">
                  <span class="meta-icon">⏱</span>
                  <span>{{ task.duration_minutes }} 分钟</span>
                </div>
                <div class="meta-item">
                  <span class="meta-icon">⭐</span>
                  <span class="priority-badge" :style="{ color: getPriorityColor(task.priority) }">
                    优先级 {{ task.priority }}
                  </span>
                </div>
                <div class="meta-item">
                  <span class="meta-icon">👤</span>
                  <span>{{ task.assigned_to_detail?.name || '未分配' }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="task-actions">
            <n-button
              v-if="task.status === 'pending'"
              type="success"
              size="medium"
              @click="completeTask(task)"
              ghost
            >
              ✓ 完成
            </n-button>
            <n-button size="medium" @click="deleteTask(task)" text>
              删除
            </n-button>
          </div>
        </div>
      </div>
    </n-card>
  </div>
</template>

<style scoped>
.tasks-container {
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 24px;
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

.filters-card {
  margin-bottom: 24px;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
}

.filters-content {
  display: flex;
  gap: 32px;
  align-items: center;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-label {
  font-size: 14px;
  font-weight: 600;
  color: #666;
  white-space: nowrap;
}

.tasks-card {
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.empty-icon {
  font-size: 64px;
  opacity: 0.5;
}

.empty-state p {
  font-size: 16px;
  color: #999;
  margin: 0;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.task-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
  border: 1px solid #f0f0f0;
  border-radius: 16px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.task-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  background: white;
}

.task-card.completed {
  opacity: 0.6;
  background: #f9fafb;
}

.task-card.completed .task-title h3 {
  text-decoration: line-through;
}

.task-main {
  display: flex;
  gap: 16px;
  flex: 1;
  align-items: flex-start;
}

.task-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
}

.task-content {
  flex: 1;
  min-width: 0;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 8px;
}

.task-title {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.task-title h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.task-date {
  font-size: 13px;
  color: #999;
}

.task-description {
  margin: 8px 0 12px 0;
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.task-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #666;
  padding: 4px 12px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.meta-icon {
  font-size: 14px;
}

.priority-badge {
  font-weight: 600;
}

.task-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

/* === Mobile Responsive === */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: stretch;
  }

  .header h1 {
    font-size: 24px;
  }

  .header-left {
    text-align: center;
  }

  .filters-content {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .filter-group {
    flex-direction: column;
    align-items: stretch;
  }

  .task-card {
    flex-direction: column;
    padding: 16px;
  }

  .task-main {
    width: 100%;
  }

  .task-icon {
    width: 48px;
    height: 48px;
    font-size: 24px;
  }

  .task-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .task-meta {
    flex-direction: column;
    gap: 8px;
  }

  .meta-item {
    justify-content: flex-start;
  }

  .task-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
