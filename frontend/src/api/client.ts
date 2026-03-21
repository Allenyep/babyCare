import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Wrapper functions for API calls
export const api = {
  // Babies
  babies: {
    list: () => apiClient.get('/babies/'),
    get: (id: number) => apiClient.get(`/babies/${id}`),
    create: (data: any) => apiClient.post('/babies/', data),
    update: (id: number, data: any) => apiClient.patch(`/babies/${id}`, data),
    delete: (id: number) => apiClient.delete(`/babies/${id}`),
    addGrowth: (id: number, data: any) => apiClient.post(`/babies/${id}/growth`, data),
    getGrowth: (id: number) => apiClient.get(`/babies/${id}/growth`)
  },

  // Parents
  parents: {
    list: () => apiClient.get('/parents/'),
    get: (id: number) => apiClient.get(`/parents/${id}`),
    create: (data: any) => apiClient.post('/parents/', data),
    update: (id: number, data: any) => apiClient.patch(`/parents/${id}`, data),
    delete: (id: number) => apiClient.delete(`/parents/${id}`)
  },

  // Tasks
  tasks: {
    list: (params?: any) => apiClient.get('/tasks/', { params }),
    get: (id: number) => apiClient.get(`/tasks/${id}`),
    create: (data: any) => apiClient.post('/tasks/', data),
    update: (id: number, data: any) => apiClient.patch(`/tasks/${id}`, data),
    delete: (id: number) => apiClient.delete(`/tasks/${id}`),
    complete: (id: number) => apiClient.patch(`/tasks/${id}`, { status: 'completed' })
  },

  // Knowledge Base
  knowledge: {
    getVaccines: (ageMonths: number, upcoming?: boolean) =>
      apiClient.get('/knowledge/vaccines', { params: { age_months: ageMonths, upcoming } }),
    getFoods: (ageMonths: number) =>
      apiClient.get('/knowledge/foods', { params: { age_months: ageMonths } }),
    getActivities: (ageMonths: number, category?: string) =>
      apiClient.get('/knowledge/activities', { params: { age_months: ageMonths, category } }),
    getMilestones: (ageMonths: number, category?: string) =>
      apiClient.get('/knowledge/milestones', { params: { age_months: ageMonths, category } }),
    getComprehensive: (ageMonths: number) =>
      apiClient.get('/knowledge/comprehensive', { params: { age_months: ageMonths } }),
    getCategories: () => apiClient.get('/knowledge/categories')
  },

  // Scheduler
  scheduler: {
    generate: (data: any) => apiClient.post('/scheduler/generate', data),
    preview: (data: any) => apiClient.post('/scheduler/preview', data),
    adjust: (babyId: number, date: string, adjustments: any[]) =>
      apiClient.put('/scheduler/adjust', null, {
        params: { baby_id: babyId, target_date: date },
        data: { adjustments }
      }),
    getStatistics: (babyId: number, date: string) =>
      apiClient.get('/scheduler/statistics', {
        params: { baby_id: babyId, target_date: date }
      }),
    getRecurringTasks: () => apiClient.get('/scheduler/recurring-tasks'),
    updateRecurringTasks: (tasks: any[]) => apiClient.put('/scheduler/recurring-tasks', tasks),
    getTimeSlots: () => apiClient.get('/scheduler/time-slots'),
    optimize: (babyId: number, date: string, optimizeFor: string) =>
      apiClient.post('/scheduler/optimize', null, {
        params: { baby_id: babyId, target_date: date, optimize_for: optimizeFor }
      })
  },

  // Fatigue
  fatigue: {
    calculate: (data: any) => apiClient.post('/fatigue/calculate', data),
    getRecord: (parentId: number, recordDate: string) =>
      apiClient.get(`/fatigue/record/${parentId}`, { params: { record_date: recordDate } }),
    getTrend: (parentId: number, days?: number) =>
      apiClient.get(`/fatigue/trend/${parentId}`, { params: { days } }),
    analyze: (parentId: number, recordDate: string) =>
      apiClient.get(`/fatigue/analyze/${parentId}`, { params: { record_date: recordDate } }),
    compare: (parentIds: number[], recordDate: string) =>
      apiClient.get('/fatigue/compare', { params: { parent_ids: parentIds, record_date: recordDate } }),
    recordSleep: (data: any) => apiClient.post('/fatigue/sleep', data),
    getSleepRecords: (parentId: number, startDate?: string, endDate?: string) =>
      apiClient.get(`/fatigue/sleep/${parentId}`, {
        params: { start_date: startDate, end_date: endDate }
      }),
    getStatistics: (parentId: number, days?: number) =>
      apiClient.get(`/fatigue/statistics/${parentId}`, { params: { days } })
  }
}

export default apiClient
