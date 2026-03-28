import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/api/client'

export interface Task {
  id: number
  baby_id: number
  name: string
  category: string
  description?: string
  duration_minutes: number
  priority: number
  date: string
  time_slot: string
  assigned_to: number
  assigned_to_detail?: {
    id: number
    name: string
  }
  status: 'pending' | 'in_progress' | 'completed' | 'skipped' | 'cancelled'
}

export const useTaskStore = defineStore('task', () => {
  const tasks = ref<Task[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const completedTasks = computed(() =>
    tasks.value.filter(t => t.status === 'completed')
  )

  const pendingTasks = computed(() =>
    tasks.value.filter(t => t.status === 'pending')
  )

  async function fetchTasks(params?: any) {
    loading.value = true
    error.value = null
    try {
      const response = await api.tasks.list(params)
      tasks.value = response.data
    } catch (e: any) {
      error.value = e.message
      tasks.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchTask(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await api.tasks.get(id)
      return response.data
    } catch (e: any) {
      error.value = e.message
      return null
    } finally {
      loading.value = false
    }
  }

  async function createTask(data: Partial<Task>) {
    loading.value = true
    error.value = null
    try {
      const response = await api.tasks.create(data)
      tasks.value.push(response.data)
      return response.data
    } catch (e: any) {
      error.value = e.message
      return null
    } finally {
      loading.value = false
    }
  }

  async function updateTask(id: number, data: Partial<Task>) {
    loading.value = true
    error.value = null
    try {
      const response = await api.tasks.update(id, data)
      const index = tasks.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tasks.value[index] = response.data
      }
      return response.data
    } catch (e: any) {
      error.value = e.message
      return null
    } finally {
      loading.value = false
    }
  }

  async function completeTask(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await api.tasks.complete(id)
      const index = tasks.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tasks.value[index] = response.data
      }
      return response.data
    } catch (e: any) {
      error.value = e.message
      return null
    } finally {
      loading.value = false
    }
  }

  async function deleteTask(id: number) {
    loading.value = true
    error.value = null
    try {
      await api.tasks.delete(id)
      tasks.value = tasks.value.filter(t => t.id !== id)
      return true
    } catch (e: any) {
      error.value = e.message
      return false
    } finally {
      loading.value = false
    }
  }

  function getTasksByDate(date: string) {
    return tasks.value.filter(t => t.date === date)
  }

  function getTasksByTimeSlot(timeSlot: string) {
    return tasks.value.filter(t => t.time_slot === timeSlot)
  }

  return {
    tasks,
    loading,
    error,
    completedTasks,
    pendingTasks,
    fetchTasks,
    fetchTask,
    createTask,
    updateTask,
    completeTask,
    deleteTask,
    getTasksByDate,
    getTasksByTimeSlot
  }
})
