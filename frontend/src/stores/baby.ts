import { defineStore } from 'pinia'
import { ref } from 'vue'

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
      // TODO: API call
      babies.value = []
    } catch (e: any) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  return { currentBaby, babies, loading, error, setCurrentBaby, fetchBabies }
})
