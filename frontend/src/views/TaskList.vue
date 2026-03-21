<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Task, TaskStatus } from '@/types'

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

const selectedDate = ref(new Date().toISOString().split('T')[0])

// Filters
const statusFilter = ref<TaskStatus | 'all'>('all')

const filteredTasks = computed(() => {
  if (statusFilter.value === 'all') return tasks.value
  return tasks.value.filter(t => t.status === statusFilter.value)
})

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
</script>

<template>
  <div class="tasks-container">
    <!-- Header -->
    <header class="header">
      <h1>📝 任务管理</h1>
      <n-button type="primary" @click="createTask">
        + 添加任务
      </n-button>
    </header>

    <!-- Filters -->
    <n-card class="filters-card">
      <n-space>
        <span>日期:</span>
        <n-date-picker v-model:value="selectedDate" />
        <n-divider vertical />
        <span>状态:</span>
        <n-select v-model:value="statusFilter" style="width: 150px">
          <n-option value="all">全部</n-option>
          <n-option value="pending">待完成</n-option>
          <n-option value="completed">已完成</n-option>
        </n-select>
      </n-space>
    </n-card>

    <!-- Task List -->
    <n-card class="tasks-card">
      <div v-if="filteredTasks.length === 0" class="empty-state">
        <p>暂无任务</p>
      </div>

      <div v-else class="tasks-list">
        <div
          v-for="task in filteredTasks"
          :key="task.id"
          class="task-card"
          :class="{ completed: task.status === 'completed' }"
        >
          <div class="task-header">
            <div class="task-title">
              <span class="task-name">{{ task.name }}</span>
              <span class="task-date">{{ task.date }}</span>
            </div>
            <div class="task-meta">
              <n-tag :type="getCategoryTag(task.category)">
                {{ getCategoryLabel(task.category) }}
              </n-tag>
              <span>⏱ {{ task.duration_minutes }}min</span>
              <span>⭐ {{ task.priority }}</span>
            </div>
          </div>

          <div v-if="task.description" class="task-description">
            {{ task.description }}
          </div>

          <div class="task-assignment">
            <span class="label">分配给:</span>
            <span v-if="task.assigned_to_detail">
              {{ task.assigned_to_detail.name }}
            </span>
            <span v-else>未分配</span>
          </div>

          <div class="task-actions">
            <n-button
              v-if="task.status === 'pending'"
              type="success"
              size="small"
              @click="completeTask(task)"
            >
              ✓ 完成
            </n-button>
            <n-button size="small" @click="deleteTask(task)">
              删除
            </n-button>
          </div>
        </div>
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
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
</script>

<style scoped>
.tasks-container {
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
  margin: 0;
}

.filters-card,
.tasks-card {
  margin-bottom: var(--spacing-lg);
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.task-card {
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-md);
  transition: all var(--transition-fast);
}

.task-card:hover {
  box-shadow: var(--shadow-md);
}

.task-card.completed {
  opacity: 0.6;
  background: var(--bg-secondary);
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
  font-size: 18px;
}

.task-date {
  font-size: 14px;
  color: var(--text-tertiary);
}

.task-meta {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
  font-size: 14px;
  color: var(--text-secondary);
}

.task-description {
  margin: var(--spacing-sm) 0;
  color: var(--text-secondary);
}

.task-assignment {
  display: flex;
  gap: var(--spacing-xs);
  margin: var(--spacing-sm) 0;
  font-size: 14px;
}

.label {
  font-weight: 600;
}

.task-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.empty-state {
  text-align: center;
  padding: var(--spacing-xxl) 0;
  color: var(--text-tertiary);
}
</style>
