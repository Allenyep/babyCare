<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBabyStore } from '@/stores/baby'
import { useMessage } from 'naive-ui'
import type { Baby, GrowthRecord } from '@/types'

const router = useRouter()
const babyStore = useBabyStore()
const message = useMessage()

const baby = ref<Baby | null>(null)
const growthRecords = ref<GrowthRecord[]>([])
const loading = ref(false)
const isEditing = ref(false)

const form = ref({
  name: '',
  nickname: '',
  birthday: null as number | null,
  gender: 'male' as 'male' | 'female'
})

const showForm = computed(() => {
  return !baby.value || isEditing.value
})

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

function loadGrowthRecords() {
  if (!baby.value) return
  // TODO: API call
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

    if (newBaby) {
      // Set as current baby
      babyStore.setCurrentBaby(newBaby)
      baby.value = newBaby

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
      message.error('创建失败，请重试')
    }
  } catch (error: any) {
    console.error('Failed to create baby:', error)
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
  // TODO: API call
}
</script>

<template>
  <div class="profile-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <n-spin size="large" />
      <p>加载中...</p>
    </div>

    <!-- Baby Info -->
    <n-card v-if="baby && !showForm" class="baby-card">
      <template #header>
        <h2>👶 宝宝档案</h2>
        <n-button @click="editBaby">编辑</n-button>
      </template>

      <div class="baby-detail">
        <div class="detail-row">
          <span class="label">姓名:</span>
          <span>{{ baby.name }}</span>
        </div>
        <div class="detail-row">
          <span class="label">小名:</span>
          <span>{{ baby.nickname || '-' }}</span>
        </div>
        <div class="detail-row">
          <span class="label">生日:</span>
          <span>{{ baby.birthday }}</span>
        </div>
        <div class="detail-row">
          <span class="label">性别:</span>
          <span>{{ baby.gender === 'male' ? '男宝宝' : '女宝宝' }}</span>
        </div>
        <div class="detail-row">
          <span class="label">月龄:</span>
          <span>{{ baby.age_months }} 个月</span>
        </div>
      </div>
    </n-card>

    <!-- Create/Edit Form -->
    <n-card v-if="showForm" class="form-card">
      <template #header>
        <h2>{{ baby ? '编辑' : '添加' }}宝宝信息</h2>
        <n-button v-if="baby" text @click="cancelEdit">取消</n-button>
      </template>

      <n-form @submit.prevent="baby ? updateBaby() : createBaby()">
        <n-form-item label="姓名">
          <n-input v-model:value="form.name" placeholder="请输入宝宝姓名" />
        </n-form-item>

        <n-form-item label="小名">
          <n-input v-model:value="form.nickname" placeholder="选填" />
        </n-form-item>

        <n-form-item label="生日">
          <n-date-picker v-model:value="form.birthday" type="date" />
        </n-form-item>

        <n-form-item label="性别">
          <n-radio-group v-model:value="form.gender">
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
            @click="() => {
              console.log('Button clicked', form.value)
              if (!form.value.name) {
                message.warning('请输入宝宝姓名')
              }
              if (!form.value.birthday) {
                message.warning('请选择宝宝生日')
              }
            }"
          >
            {{ baby ? '保存' : '创建' }}
          </n-button>
        </n-form-item>
      </n-form>
    </n-card>

    <!-- Growth Records -->
    <n-card v-if="baby" class="growth-card">
      <template #header>
        <h3>📏 生长记录</h3>
        <n-button size="small" @click="addGrowthRecord">
          + 添加记录
        </n-button>
      </template>

      <div v-if="growthRecords.length === 0" class="empty-state">
        <p>暂无生长记录</p>
      </div>

      <div v-else class="records-list">
        <div
          v-for="record in growthRecords"
          :key="record.id"
          class="record-item"
        >
          <span class="record-date">{{ record.record_date }}</span>
          <div class="record-values">
            <span v-if="record.weight">体重: {{ record.weight }}kg</span>
            <span v-if="record.height">身高: {{ record.height }}cm</span>
            <span v-if="record.head_circumference">
              头围: {{ record.head_circumference }}cm
            </span>
          </div>
        </div>
      </div>
    </n-card>

    <!-- Family Members -->
    <n-card v-if="baby" class="family-card">
      <template #header>
        <h3>👨‍👩‍👧 家庭成员</h3>
        <n-button size="small" type="primary">+ 添加成员</n-button>
      </template>

      <div class="parents-list">
        <div class="parent-card">
          <div class="parent-info">
            <h4>👩 妈妈</h4>
            <p>工作时间: 09:00-18:00</p>
            <p>目标睡眠: 7.5小时</p>
            <p>疲劳度: 0.35 <span class="fatigue-label">⚠️</span></p>
          </div>
        </div>

        <div class="parent-card">
          <div class="parent-info">
            <h4>👨 爸爸</h4>
            <p>工作时间: 10:00-19:00</p>
            <p>目标睡眠: 7.5小时</p>
            <p>疲劳度: 0.25 <span class="fatigue-label">✅</span></p>
          </div>
        </div>
      </div>
    </n-card>
  </div>
</template>

<style scoped>
.profile-container {
  padding: var(--spacing-md);
  max-width: 1000px;
  margin: 0 auto;
  min-height: 100vh;
}

.baby-card,
.form-card,
.growth-card,
.family-card {
  margin-bottom: var(--spacing-lg);
}

.baby-detail {
  display: grid;
  gap: var(--spacing-md);
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: var(--spacing-sm) 0;
  border-bottom: 1px solid var(--border-color);
}

.detail-row .label {
  font-weight: 600;
  color: var(--text-secondary);
}

.records-list {
  display: grid;
  gap: var(--spacing-sm);
}

.record-item {
  padding: var(--spacing-md);
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
}

.record-date {
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
}

.record-values {
  display: flex;
  gap: var(--spacing-md);
  font-size: 14px;
}

.parents-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-md);
}

.parent-card {
  padding: var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
}

.parent-info h4 {
  margin: 0 0 var(--spacing-xs) 0;
}

.fatigue-label {
  margin-left: var(--spacing-xs);
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: var(--spacing-md);
  color: var(--text-secondary);
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .profile-container {
    padding: 0; /* Remove padding since App.vue handles it */
  }

  .parents-list {
    grid-template-columns: 1fr;
  }

  .record-values {
    flex-direction: column;
    gap: var(--spacing-xs);
  }

  .detail-row {
    font-size: 14px;
  }
}
</style>
