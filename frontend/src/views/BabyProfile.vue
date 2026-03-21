<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBabyStore } from '@/stores/baby'
import type { Baby, GrowthRecord } from '@/types'

const router = useRouter()
const babyStore = useBabyStore()

const baby = ref<Baby | null>(null)
const growthRecords = ref<GrowthRecord[]>([])
const loading = ref(false)

const form = ref({
  name: '',
  nickname: '',
  birthday: '',
  gender: 'male' as 'male' | 'female'
})

const showForm = ref(false)

onMounted(() => {
  const currentBaby = babyStore.currentBaby
  if (currentBaby) {
    baby.value = currentBaby
    loadGrowthRecords()
  } else {
    showForm.value = true
  }
})

function loadGrowthRecords() {
  if (!baby.value) return
  // TODO: API call
}

function createBaby() {
  if (!form.value.name || !form.value.birthday) {
    return
  }
  // TODO: API call
  showForm.value = false
}

function addGrowthRecord() {
  // TODO: API call
}
</script>

<template>
  <div class="profile-container">
    <!-- Baby Info -->
    <n-card v-if="baby && !showForm" class="baby-card">
      <template #header>
        <h2>👶 宝宝档案</h2>
        <n-button @click="showForm = true">编辑</n-button>
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
        <n-button v-if="baby" text @click="showForm = false">取消</n-button>
      </template>

      <n-form @submit.prevent="createBaby">
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
          <n-button type="primary" attr-type="submit" size="large">
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
</style>
