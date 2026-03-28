<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBabyStore } from '@/stores/baby'
import { useMessage } from 'naive-ui'
import { api } from '@/api/client'
import type { Baby, GrowthRecord } from '@/types'

const router = useRouter()
const babyStore = useBabyStore()
const message = useMessage()

const baby = ref<Baby | null>(null)
const growthRecords = ref<GrowthRecord[]>([])
const loading = ref(false)
const isEditing = ref(false)
const showGrowthModal = ref(false)
const showParentModal = ref(false)

const form = ref({
  name: '',
  nickname: '',
  birthday: null as number | null,
  gender: 'male' as 'male' | 'female'
})

const growthForm = ref({
  record_date: null as number | null,
  weight: null as number | null,
  height: null as number | null,
  head_circumference: null as number | null,
  notes: ''
})

const showForm = computed(() => {
  return !baby.value || isEditing.value
})

// Animation variants
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

const recordVariants = {
  initial: { opacity: 0, x: -20 },
  enter: {
    opacity: 1,
    x: 0,
    transition: {
      duration: 300,
      ease: 'easeOut'
    }
  }
}

onMounted(async () => {
  loading.value = true
  try {
    // Try to get current baby from store
    let currentBaby = babyStore.currentBaby

    // If no current baby, try to load babies
    if (!currentBaby) {
      try {
        await babyStore.fetchBabies()
      } catch (apiError) {
        console.warn('Failed to fetch babies from API:', apiError)
        // Continue anyway - will show create form
      }
      currentBaby = babyStore.currentBaby

      // If still no baby, set the first one as current
      if (!currentBaby && babyStore.babies.length > 0) {
        babyStore.setCurrentBaby(babyStore.babies[0])
        currentBaby = babyStore.babies[0]
      }
    }

    if (currentBaby) {
      baby.value = currentBaby
      loadGrowthRecords()
    }
  } catch (error) {
    console.error('Failed to load baby data:', error)
  } finally {
    loading.value = false
  }
})

async function loadGrowthRecords() {
  if (!baby.value) return
  try {
    const response = await api.babies.getGrowth(baby.value.id)
    growthRecords.value = response.data
  } catch (error: any) {
    console.error('Failed to load growth records:', error)
  }
}

async function createBaby() {
  console.log('createBaby called', form.value)

  if (!form.value.name || !form.value.birthday) {
    message.warning('请填写宝宝姓名和生日')
    return
  }

  loading.value = true
  try {
    // Convert timestamp to date string for API
    const birthday = new Date(form.value.birthday).toISOString().split('T')[0]
    const payload = {
      name: form.value.name,
      nickname: form.value.nickname || undefined,
      birthday: birthday,
      gender: form.value.gender
    }

    console.log('Creating baby with payload:', payload)

    // Create baby via API
    const newBaby = await babyStore.createBaby(payload)

    console.log('API response:', newBaby)
    console.log('API response type:', typeof newBaby)
    console.log('Is response null?', newBaby === null)
    console.log('Baby store error state:', babyStore.error)

    if (newBaby) {
      // Set as current baby
      babyStore.setCurrentBaby(newBaby)
      baby.value = newBaby

      console.log('Baby value after setting:', baby.value)

      // Reset form
      form.value = {
        name: '',
        nickname: '',
        birthday: null,
        gender: 'male'
      }

      // Close form
      isEditing.value = false

      // Load growth records
      loadGrowthRecords()

      // Show success message
      message.success('宝宝信息创建成功！')
    } else {
      console.error('Failed to create baby: response is null. Store error:', babyStore.error)
      message.error(`创建失败: ${babyStore.error || '未知错误'}`)
    }
  } catch (error: any) {
    console.error('Failed to create baby:', error)
    console.error('Error response:', error.response)
    console.error('Error message:', error.message)
    message.error(error.response?.data?.detail || error.message || '创建失败，请重试')
  } finally {
    loading.value = false
  }
}

async function updateBaby() {
  if (!baby.value || !form.value.name || !form.value.birthday) {
    message.warning('请填写宝宝姓名和生日')
    return
  }

  loading.value = true
  try {
    // Convert timestamp to date string for API
    const birthday = new Date(form.value.birthday).toISOString().split('T')[0]

    // Update baby via API
    const updatedBaby = await babyStore.updateBaby(baby.value.id, {
      name: form.value.name,
      nickname: form.value.nickname || undefined,
      birthday: birthday,
      gender: form.value.gender
    })

    if (updatedBaby) {
      // Update local state
      baby.value = updatedBaby

      // Reset form
      form.value = {
        name: '',
        nickname: '',
        birthday: null,
        gender: 'male'
      }

      // Close form
      isEditing.value = false

      message.success('宝宝信息更新成功！')
    } else {
      message.error('更新失败，请重试')
    }
  } catch (error: any) {
    console.error('Failed to update baby:', error)
    message.error(error.response?.data?.detail || '更新失败，请重试')
  } finally {
    loading.value = false
  }
}

function editBaby() {
  if (baby.value) {
    form.value = {
      name: baby.value.name,
      nickname: baby.value.nickname || '',
      birthday: new Date(baby.value.birthday).getTime(),
      gender: baby.value.gender
    }
    isEditing.value = true
  }
}

function cancelEdit() {
  isEditing.value = false
  // Reset form
  form.value = {
    name: '',
    nickname: '',
    birthday: null,
    gender: 'male'
  }
}

function addGrowthRecord() {
  if (!baby.value) {
    message.warning('请先创建宝宝档案')
    return
  }
  // Reset form
  growthForm.value = {
    record_date: new Date().getTime(),
    weight: null,
    height: null,
    head_circumference: null,
    notes: ''
  }
  showGrowthModal.value = true
}

async function saveGrowthRecord() {
  if (!baby.value || !growthForm.value.record_date) {
    message.warning('请填写记录日期')
    return
  }

  loading.value = true
  try {
    const record_date = new Date(growthForm.value.record_date).toISOString().split('T')[0]
    const payload = {
      record_date,
      weight: growthForm.value.weight || undefined,
      height: growthForm.value.height || undefined,
      head_circumference: growthForm.value.head_circumference || undefined,
      notes: growthForm.value.notes || undefined
    }

    const response = await api.babies.addGrowth(baby.value.id, payload)
    growthRecords.value.unshift(response.data)
    message.success('生长记录添加成功！')
    showGrowthModal.value = false
  } catch (error: any) {
    console.error('Failed to add growth record:', error)
    message.error(error.response?.data?.detail || '添加失败，请重试')
  } finally {
    loading.value = false
  }
}

function addParentMember() {
  message.info('家庭成员功能即将推出')
}

function getFatigueColor(fatigue: number) {
  if (fatigue < 0.3) return '#10B981'
  if (fatigue < 0.5) return '#F59E0B'
  if (fatigue < 0.8) return '#F97316'
  return '#EF4444'
}
</script>

<template>
  <div class="profile-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else class="content-grid">
      <!-- Baby Info -->
      <n-card
        v-if="baby && !showForm"
        class="baby-card"
        v-motion="cardVariants"
      >
        <template #header>
          <div class="card-header">
            <h2>👶 宝宝档案</h2>
            <n-button @click="editBaby" secondary>编辑</n-button>
          </div>
        </template>

        <div class="baby-detail">
          <div class="baby-avatar-large">
            <span class="avatar-text">{{ (baby.nickname || baby.name).charAt(0) }}</span>
          </div>

          <div class="detail-info">
            <div class="detail-row">
              <span class="label">姓名</span>
              <span class="value">{{ baby.name }}</span>
            </div>
            <div class="detail-row">
              <span class="label">小名</span>
              <span class="value">{{ baby.nickname || '-' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">生日</span>
              <span class="value">{{ baby.birthday }}</span>
            </div>
            <div class="detail-row">
              <span class="label">性别</span>
              <span class="value gender-badge" :class="baby.gender">
                {{ baby.gender === 'male' ? '男宝宝' : '女宝宝' }}
              </span>
            </div>
            <div class="detail-row">
              <span class="label">月龄</span>
              <span class="value age-badge">{{ baby.age_months }} 个月</span>
            </div>
          </div>
        </div>
      </n-card>

      <!-- Create/Edit Form -->
      <n-card
        v-if="showForm"
        class="form-card"
        v-motion="cardVariants"
      >
        <template #header>
          <div class="card-header">
            <h2>{{ baby ? '编辑' : '添加' }}宝宝信息</h2>
            <n-button v-if="baby" text @click="cancelEdit">取消</n-button>
          </div>
        </template>

        <n-form @submit.prevent="baby ? updateBaby() : createBaby()">
          <n-form-item label="姓名">
            <n-input v-model:value="form.name" placeholder="请输入宝宝姓名" size="large" />
          </n-form-item>

          <n-form-item label="小名">
            <n-input v-model:value="form.nickname" placeholder="选填" size="large" />
          </n-form-item>

          <n-form-item label="生日">
            <n-date-picker
              v-model:value="form.birthday"
              type="date"
              value-format="timestamp"
              :format="'yyyy-MM-dd'"
              size="large"
              style="width: 100%"
            />
          </n-form-item>

          <n-form-item label="性别">
            <n-radio-group v-model:value="form.gender" size="large">
              <n-radio value="male">男宝宝</n-radio>
              <n-radio value="female">女宝宝</n-radio>
            </n-radio-group>
          </n-form-item>

          <n-form-item :show-label="false">
            <n-button
              type="primary"
              attr-type="submit"
              size="large"
              :loading="loading"
              :disabled="loading"
              style="width: 100%"
            >
              {{ baby && baby.id ? '保存' : '创建' }}
            </n-button>
          </n-form-item>
        </n-form>
      </n-card>

      <!-- Growth Records -->
      <n-card
        v-if="baby"
        class="growth-card"
        v-motion="cardVariants"
        :delay="200"
      >
        <template #header>
          <div class="card-header">
            <h3>📏 生长记录</h3>
            <n-button size="small" @click="addGrowthRecord">
              + 添加记录
            </n-button>
          </div>
        </template>

        <div v-if="growthRecords.length === 0" class="empty-state">
          <span class="empty-icon">📝</span>
          <p>暂无生长记录</p>
        </div>

        <div v-else class="records-list">
          <div
            v-for="(record, index) in growthRecords"
            :key="record.id"
            class="record-item"
            v-motion="recordVariants"
            :delay="index * 50"
          >
            <div class="record-header">
              <span class="record-date">{{ record.record_date }}</span>
            </div>
            <div class="record-values">
              <div v-if="record.weight" class="record-value">
                <span class="value-icon">⚖️</span>
                <span class="value-text">{{ record.weight }}kg</span>
              </div>
              <div v-if="record.height" class="record-value">
                <span class="value-icon">📏</span>
                <span class="value-text">{{ record.height }}cm</span>
              </div>
              <div v-if="record.head_circumference" class="record-value">
                <span class="value-icon">🎯</span>
                <span class="value-text">{{ record.head_circumference }}cm</span>
              </div>
            </div>
          </div>
        </div>
      </n-card>

      <!-- Family Members -->
      <n-card
        v-if="baby"
        class="family-card"
        v-motion="cardVariants"
        :delay="400"
      >
        <template #header>
          <div class="card-header">
            <h3>👨‍👩‍👧 家庭成员</h3>
            <n-button size="small" type="primary" @click="addParentMember">
              + 添加成员
            </n-button>
          </div>
        </template>

        <div class="parents-list">
          <div class="parent-card">
            <div class="parent-avatar">👩</div>
            <div class="parent-info">
              <h4>妈妈</h4>
              <p class="info-item">⏰ 工作时间: 09:00-18:00</p>
              <p class="info-item">😴 目标睡眠: 7.5小时</p>
              <div class="fatigue-bar">
                <span class="fatigue-label">疲劳度</span>
                <div class="fatigue-progress">
                  <div
                    class="fatigue-fill"
                    :style="{ width: '35%', background: getFatigueColor(0.35) }"
                  ></div>
                </div>
                <span class="fatigue-value">35%</span>
              </div>
            </div>
          </div>

          <div class="parent-card">
            <div class="parent-avatar">👨</div>
            <div class="parent-info">
              <h4>爸爸</h4>
              <p class="info-item">⏰ 工作时间: 10:00-19:00</p>
              <p class="info-item">😴 目标睡眠: 7.5小时</p>
              <div class="fatigue-bar">
                <span class="fatigue-label">疲劳度</span>
                <div class="fatigue-progress">
                  <div
                    class="fatigue-fill"
                    :style="{ width: '25%', background: getFatigueColor(0.25) }"
                  ></div>
                </div>
                <span class="fatigue-value">25%</span>
              </div>
            </div>
          </div>
        </div>
      </n-card>
    </div>

    <!-- Growth Record Modal -->
    <n-modal v-model:show="showGrowthModal" preset="card" title="添加生长记录" style="width: 500px">
      <n-form @submit.prevent="saveGrowthRecord">
        <n-form-item label="记录日期">
          <n-date-picker
            v-model:value="growthForm.record_date"
            type="date"
            value-format="timestamp"
            style="width: 100%"
            size="large"
          />
        </n-form-item>

        <n-form-item label="体重 (kg)">
          <n-input-number
            v-model:value="growthForm.weight"
            :min="0"
            :max="100"
            :precision="2"
            :step="0.1"
            placeholder="选填"
            style="width: 100%"
            size="large"
          />
        </n-form-item>

        <n-form-item label="身高 (cm)">
          <n-input-number
            v-model:value="growthForm.height"
            :min="0"
            :max="200"
            :precision="1"
            :step="0.5"
            placeholder="选填"
            style="width: 100%"
            size="large"
          />
        </n-form-item>

        <n-form-item label="头围 (cm)">
          <n-input-number
            v-model:value="growthForm.head_circumference"
            :min="0"
            :max="100"
            :precision="1"
            :step="0.1"
            placeholder="选填"
            style="width: 100%"
            size="large"
          />
        </n-form-item>

        <n-form-item label="备注">
          <n-input
            v-model:value="growthForm.notes"
            type="textarea"
            placeholder="选填"
            :rows="3"
          />
        </n-form-item>

        <n-form-item :show-label="false">
          <n-space>
            <n-button type="primary" attr-type="submit" :loading="loading" :disabled="loading">
              保存
            </n-button>
            <n-button @click="showGrowthModal = false">取消</n-button>
          </n-space>
        </n-form-item>
      </n-form>
    </n-modal>
  </div>
</template>

<style scoped>
.profile-container {
  max-width: 1200px;
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
  grid-template-columns: 1fr;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2,
.card-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

/* === Baby Card === */
.baby-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
}

.baby-detail {
  display: grid;
  gap: 24px;
  text-align: center;
}

.baby-avatar-large {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
}

.avatar-text {
  font-size: 48px;
  font-weight: 700;
  color: white;
}

.detail-info {
  display: grid;
  gap: 16px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #fafafa;
  border-radius: 12px;
  transition: all 0.2s;
}

.detail-row:hover {
  background: #f5f5f5;
  transform: translateX(4px);
}

.detail-row .label {
  font-weight: 600;
  color: #666;
}

.detail-row .value {
  font-weight: 500;
  color: #333;
}

.gender-badge {
  padding: 4px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.gender-badge.male {
  background: #e0f2fe;
  color: #0284c7;
}

.gender-badge.female {
  background: #fce7f3;
  color: #db2777;
}

.age-badge {
  padding: 4px 16px;
  border-radius: 20px;
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #0284c7;
  font-size: 14px;
  font-weight: 600;
}

/* === Form Card === */
.form-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
}

/* === Growth Card === */
.growth-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.empty-icon {
  font-size: 48px;
  display: block;
  margin-bottom: 12px;
  opacity: 0.5;
}

.records-list {
  display: grid;
  gap: 12px;
}

.record-item {
  padding: 20px;
  background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
  border-radius: 16px;
  border: 1px solid #f0f0f0;
  transition: all 0.3s;
  cursor: pointer;
}

.record-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  background: white;
}

.record-header {
  margin-bottom: 12px;
}

.record-date {
  font-weight: 700;
  font-size: 16px;
  color: #667eea;
}

.record-values {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.record-value {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: white;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.value-icon {
  font-size: 18px;
}

.value-text {
  color: #333;
}

/* === Family Card === */
.family-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
}

.parents-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.parent-card {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
  border-radius: 16px;
  border: 1px solid #f0f0f0;
  transition: all 0.3s;
}

.parent-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  background: white;
}

.parent-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  flex-shrink: 0;
}

.parent-info {
  flex: 1;
}

.parent-info h4 {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 600;
}

.info-item {
  margin: 6px 0;
  font-size: 14px;
  color: #666;
}

.fatigue-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
}

.fatigue-label {
  font-size: 13px;
  color: #666;
  font-weight: 500;
}

.fatigue-progress {
  flex: 1;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.fatigue-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.fatigue-value {
  font-size: 13px;
  font-weight: 600;
  color: #333;
  min-width: 40px;
  text-align: right;
}

/* === Mobile Responsive === */
@media (max-width: 768px) {
  .content-grid {
    gap: 16px;
  }

  .parents-list {
    grid-template-columns: 1fr;
  }

  .record-values {
    flex-direction: column;
    gap: 8px;
  }

  .parent-card {
    flex-direction: column;
    text-align: center;
  }

  .baby-avatar-large {
    width: 80px;
    height: 80px;
  }

  .avatar-text {
    font-size: 36px;
  }
}
</style>
