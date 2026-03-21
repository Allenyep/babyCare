// Common types
export type TimeSlot = 'early' | 'morning' | 'noon' | 'afternoon' | 'evening' | 'night'

export type TaskCategory = 'feeding' | 'diaper' | 'education' | 'food' | 'outdoor' | 'hygiene' | 'medical'

export type TaskStatus = 'pending' | 'in_progress' | 'completed' | 'skipped' | 'cancelled'

export type Relationship = 'mother' | 'father' | 'grandparent' | 'nanny'

// Baby
export interface Baby {
  id: number
  name: string
  nickname?: string
  birthday: string
  gender: 'male' | 'female'
  avatar?: string
  age_months?: number
}

// Parent
export interface Parent {
  id: number
  baby_id: number
  name: string
  relationship: Relationship
  avatar?: string
  phone?: string
  work_start_time?: string
  work_end_time?: string
  sleep_start_time?: string
  sleep_end_time?: string
  unavailable_slots?: any[]
  capabilities?: string[]
  target_sleep_hours: number
  fatigue_score?: number
}

// Task
export interface Task {
  id: number
  baby_id: number
  template_id?: number
  schedule_id: number
  name: string
  category: TaskCategory
  description?: string
  duration_minutes: number
  priority: number
  date: string
  time_slot: TimeSlot
  assigned_to?: number
  status: TaskStatus
  completed_at?: string
  completed_by?: number
  completion_notes?: string
  assigned_to_detail?: Parent
}

// Schedule
export interface Schedule {
  id: number
  baby_id: number
  date: string
  total_tasks: number
  completed_tasks: number
  completion_rate: number
  fatigue_scores: Record<number, number>
  balance_score: number
  is_special_day: boolean
  special_notes?: string
  tasks: Task[]
}

// Growth Record
export interface GrowthRecord {
  id: number
  baby_id: number
  record_date: string
  weight?: number
  height?: number
  head_circumference?: number
  notes?: string
}
