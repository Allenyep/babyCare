import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/client'

export interface Baby {
  id: number
  name: string
  nickname?: string
  birthday: string
  gender: 'male' | 'female'
  avatar?: string
  age_months?: number
}

export const useBabyStore = defineStore('baby', () => {
  const currentBaby = ref<Baby | null>(null)
  const babies = ref<Baby[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  function setCurrentBaby(baby: Baby) {
    currentBaby.value = baby
  }

  async function fetchBabies() {
    loading.value = true
    error.value = null
    try {
      const response = await api.babies.list()
      babies.value = response.data
    } catch (e: any) {
      error.value = e.message
      babies.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchBaby(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await api.babies.get(id)
      return response.data
    } catch (e: any) {
      error.value = e.message
      return null
    } finally {
      loading.value = false
    }
  }

  async function createBaby(data: Partial<Baby>) {
    loading.value = true
    error.value = null
    try {
      const response = await api.babies.create(data)
      babies.value.push(response.data)
      return response.data
    } catch (e: any) {
      error.value = e.message
      return null
    } finally {
      loading.value = false
    }
  }

  async function updateBaby(id: number, data: Partial<Baby>) {
    loading.value = true
    error.value = null
    try {
      const response = await api.babies.update(id, data)
      const index = babies.value.findIndex(b => b.id === id)
      if (index !== -1) {
        babies.value[index] = response.data
      }
      if (currentBaby.value?.id === id) {
        currentBaby.value = response.data
      }
      return response.data
    } catch (e: any) {
      error.value = e.message
      return null
    } finally {
      loading.value = false
    }
  }

  return {
    currentBaby,
    babies,
    loading,
    error,
    setCurrentBaby,
    fetchBabies,
    fetchBaby,
    createBaby,
    updateBaby
  }
})
