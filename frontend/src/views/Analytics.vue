<script setup lang="ts">
import { ref, computed } from 'vue'

const selectedPeriod = ref<'week' | 'month' | 'year'>('week')

// Mock analytics data - TODO: Replace with API calls
const taskStats = ref({
  total: 42,
  completed: 28,
  skipped: 3,
  onTimeRate: 85.7,
  avgCompletionTime: 18
})

const fatigueStats = ref([
  { name: '妈妈', current: 0.42, trend: 'up', history: [0.35, 0.38, 0.40, 0.42] },
  { name: '爸爸', current: 0.28, trend: 'down', history: [0.35, 0.32, 0.30, 0.28] }
])

const categoryStats = ref([
  { category: 'feeding', label: '喂奶', count: 12, completed: 11, avgDuration: 20 },
  { category: 'diaper', label: '换尿布', count: 14, completed: 14, avgDuration: 5 },
  { category: 'education', label: '早教', count: 6, completed: 4, avgDuration: 35 },
  { category: 'food', label: '辅食', count: 5, completed: 5, avgDuration: 25 },
  { category: 'outdoor', label: '户外', count: 3, completed: 2, avgDuration: 60 },
  { category: 'hygiene', label: '清洁', count: 4, completed: 4, avgDuration: 15 }
])

const dailyTrend = ref([
  { date: '03-14', completed: 5, total: 6, momFatigue: 0.38, dadFatigue: 0.30 },
  { date: '03-15', completed: 6, total: 6, momFatigue: 0.40, dadFatigue: 0.28 },
  { date: '03-16', completed: 4, total: 6, momFatigue: 0.42, dadFatigue: 0.25 },
  { date: '03-17', completed: 5, total: 7, momFatigue: 0.45, dadFatigue: 0.30 },
  { date: '03-18', completed: 6, total: 6, momFatigue: 0.40, dadFatigue: 0.28 },
  { date: '03-19', completed: 7, total: 7, momFatigue: 0.35, dadFatigue: 0.26 },
  { date: '03-20', completed: 5, total: 6, momFatigue: 0.42, dadFatigue: 0.28 }
])

const loadBalance = ref({
  balanceScore: 72,
  taskDistribution: {
    mom: 20,
    dad: 18,
    shared: 4
  },
  fairAllocation: 85
})

const completionRate = computed(() => {
  return Math.round((taskStats.value.completed / taskStats.value.total) * 100)
})

function getFatigueColor(score: number): string {
  if (score < 0.3) return '#10B981'
  if (score < 0.5) return '#F59E0B'
  if (score < 0.8) return '#F97316'
  return '#EF4444'
}

function getFatigueLabel(score: number): string {
  if (score < 0.3) return '良好'
  if (score < 0.5) return '轻度疲劳'
  if (score < 0.8) return '中度疲劳'
  return '重度疲劳'
}

function getTrendIcon(trend: string): string {
  return trend === 'up' ? '📈' : '📉'
}

function getCategoryColor(category: string): string {
  const colors: Record<string, string> = {
    feeding: '#10B981',
    diaper: '#3B82F6',
    education: '#F59E0B',
    food: '#EF4444',
    outdoor: '#8B5CF6',
    hygiene: '#06B6D4',
    medical: '#EC4899'
  }
  return colors[category] || '#6B7280'
}
</script>

<template>
  <div class="analytics-container">
    <!-- Header -->
    <header class="header">
      <h1>📈 数据分析</h1>
      <n-radio-group v-model:value="selectedPeriod">
        <n-radio-button value="week">本周</n-radio-button>
        <n-radio-button value="month">本月</n-radio-button>
        <n-radio-button value="year">全年</n-radio-button>
      </n-radio-group>
    </header>

    <!-- Overview Stats -->
    <div class="overview-grid">
      <n-card class="stat-card">
        <div class="stat-content">
          <span class="stat-label">任务完成率</span>
          <div class="stat-value primary">{{ completionRate }}%</div>
          <div class="stat-detail">
            {{ taskStats.completed }}/{{ taskStats.total }} 个任务
          </div>
        </div>
        <div class="stat-icon">✅</div>
      </n-card>

      <n-card class="stat-card">
        <div class="stat-content">
          <span class="stat-label">按时完成率</span>
          <div class="stat-value success">{{ taskStats.onTimeRate }}%</div>
          <div class="stat-detail">
            平均完成时间: {{ taskStats.avgCompletionTime }}分钟
          </div>
        </div>
        <div class="stat-icon">⏰</div>
      </n-card>

      <n-card class="stat-card">
        <div class="stat-content">
          <span class="stat-label">负载均衡度</span>
          <div class="stat-value">{{ loadBalance.balanceScore }}分</div>
          <div class="stat-detail">
            任务分配公平度: {{ loadBalance.fairAllocation }}%
          </div>
        </div>
        <div class="stat-icon">⚖️</div>
      </n-card>

      <n-card class="stat-card">
        <div class="stat-content">
          <span class="stat-label">跳过任务</span>
          <div class="stat-value warning">{{ taskStats.skipped }}个</div>
          <div class="stat-detail">
            占比 {{ Math.round((taskStats.skipped / taskStats.total) * 100) }}%
          </div>
        </div>
        <div class="stat-icon">⚠️</div>
      </n-card>
    </div>

    <!-- Fatigue Analysis -->
    <n-card class="section-card">
      <template #header>
        <h3>😴 疲劳度分析</h3>
      </template>
      <div class="fatigue-grid">
        <div
          v-for="person in fatigueStats"
          :key="person.name"
          class="fatigue-card"
        >
          <div class="fatigue-header">
            <h4>{{ person.name }}</h4>
            <span class="trend-icon">{{ getTrendIcon(person.trend) }}</span>
          </div>
          <div class="fatigue-value">
            <div
              class="fatigue-gauge"
              :style="{ backgroundColor: getFatigueColor(person.current) }"
            >
              {{ (person.current * 100).toFixed(0) }}%
            </div>
            <span class="fatigue-label" :style="{ color: getFatigueColor(person.current) }">
              {{ getFatigueLabel(person.current) }}
            </span>
          </div>
          <div class="fatigue-chart">
            <div class="chart-bars">
              <div
                v-for="(value, index) in person.history"
                :key="index"
                class="chart-bar"
                :style="{
                  height: `${value * 100}%`,
                  backgroundColor: getFatigueColor(value)
                }"
                :title="`疲劳度: ${(value * 100).toFixed(0)}%`"
              />
            </div>
            <span class="chart-label">近7天趋势</span>
          </div>
        </div>
      </div>
    </n-card>

    <!-- Task Categories -->
    <n-card class="section-card">
      <template #header>
        <h3>📊 任务分类统计</h3>
      </template>
      <div class="category-grid">
        <div
          v-for="cat in categoryStats"
          :key="cat.category"
          class="category-card"
          :style="{ borderTopColor: getCategoryColor(cat.category) }"
        >
          <div class="category-header">
            <span class="category-name">{{ cat.label }}</span>
            <span
              class="category-badge"
              :style="{ backgroundColor: getCategoryColor(cat.category) }"
            >
              {{ cat.completed }}/{{ cat.count }}
            </span>
          </div>
          <div class="category-stats">
            <span class="category-item">完成率: {{ Math.round((cat.completed / cat.count) * 100) }}%</span>
            <span class="category-item">平均时长: {{ cat.avgDuration }}分钟</span>
          </div>
          <div class="category-progress">
            <div
              class="progress-bar"
              :style="{
                width: `${(cat.completed / cat.count) * 100}%`,
                backgroundColor: getCategoryColor(cat.category)
              }"
            />
          </div>
        </div>
      </div>
    </n-card>

    <!-- Daily Trend -->
    <n-card class="section-card">
      <template #header>
        <h3>📅 每日趋势</h3>
      </template>
      <div class="trend-chart">
        <div class="trend-bars">
          <div
            v-for="day in dailyTrend"
            :key="day.date"
            class="trend-bar-wrapper"
          >
            <div class="trend-bar-group">
              <div
                class="trend-bar completion"
                :style="{ height: `${(day.completed / day.total) * 100}%` }"
                :title="`完成: ${day.completed}/${day.total}`"
              />
              <div
                class="trend-bar fatigue-mom"
                :style="{
                  height: `${day.momFatigue * 100}%`,
                  backgroundColor: getFatigueColor(day.momFatigue)
                }"
                :title="`妈妈疲劳度: ${(day.momFatigue * 100).toFixed(0)}%`"
              />
              <div
                class="trend-bar fatigue-dad"
                :style="{
                  height: `${day.dadFatigue * 100}%`,
                  backgroundColor: getFatigueColor(day.dadFatigue)
                }"
                :title="`爸爸疲劳度: ${(day.dadFatigue * 100).toFixed(0)}%`"
              />
            </div>
            <span class="trend-label">{{ day.date }}</span>
          </div>
        </div>
        <div class="trend-legend">
          <div class="legend-item">
            <span class="legend-color completion"></span>
            <span>任务完成率</span>
          </div>
          <div class="legend-item">
            <span class="legend-color fatigue-mom"></span>
            <span>妈妈疲劳度</span>
          </div>
          <div class="legend-item">
            <span class="legend-color fatigue-dad"></span>
            <span>爸爸疲劳度</span>
          </div>
        </div>
      </div>
    </n-card>

    <!-- Load Balance -->
    <n-card class="section-card">
      <template #header>
        <h3>⚖️ 负载分配</h3>
      </template>
      <div class="load-balance">
        <div class="balance-chart">
          <div class="balance-bar mom" :style="{ width: `${(loadBalance.taskDistribution.mom / 42) * 100}%` }">
            妈妈 {{ loadBalance.taskDistribution.mom }}个
          </div>
          <div class="balance-bar dad" :style="{ width: `${(loadBalance.taskDistribution.dad / 42) * 100}%` }">
            爸爸 {{ loadBalance.taskDistribution.dad }}个
          </div>
          <div class="balance-bar shared" :style="{ width: `${(loadBalance.taskDistribution.shared / 42) * 100}%` }">
            共同 {{ loadBalance.taskDistribution.shared }}个
          </div>
        </div>
        <div class="balance-tip">
          💡 提示: 建议保持双方任务数量接近，避免单方过度疲劳
        </div>
      </div>
    </n-card>
  </div>
</template>

<style scoped>
.analytics-container {
  padding: var(--spacing-md);
  max-width: 1400px;
  margin: 0 auto;
  min-height: 100vh;
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

.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.stat-card {
  position: relative;
  overflow: hidden;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.stat-value {
  font-size: 36px;
  font-weight: 700;
}

.stat-value.primary {
  color: var(--primary-color);
}

.stat-value.success {
  color: #10B981;
}

.stat-value.warning {
  color: #F59E0B;
}

.stat-detail {
  font-size: 14px;
  color: var(--text-tertiary);
}

.stat-icon {
  position: absolute;
  right: var(--spacing-md);
  top: 50%;
  transform: translateY(-50%);
  font-size: 48px;
  opacity: 0.2;
}

.section-card {
  margin-bottom: var(--spacing-lg);
}

.section-card h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.fatigue-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-md);
}

.fatigue-card {
  padding: var(--spacing-md);
  background: var(--bg-tertiary);
  border-radius: var(--radius-lg);
}

.fatigue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.fatigue-header h4 {
  font-size: 18px;
  margin: 0;
}

.trend-icon {
  font-size: 24px;
}

.fatigue-value {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.fatigue-gauge {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  color: white;
  font-size: 24px;
  font-weight: 700;
  min-width: 80px;
  text-align: center;
}

.fatigue-label {
  font-weight: 600;
}

.fatigue-chart {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  gap: var(--spacing-xs);
  height: 100px;
}

.chart-bar {
  flex: 1;
  border-radius: var(--radius-sm);
  transition: height var(--transition-fast);
  min-height: 4px;
}

.chart-label {
  font-size: 12px;
  color: var(--text-tertiary);
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
}

.category-card {
  padding: var(--spacing-md);
  border-top: 4px solid;
  background: var(--bg-tertiary);
  border-radius: var(--radius-lg);
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

.category-name {
  font-weight: 600;
  font-size: 16px;
}

.category-badge {
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  color: white;
  font-size: 12px;
  font-weight: 600;
}

.category-stats {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-sm);
  font-size: 14px;
  color: var(--text-secondary);
}

.category-progress {
  height: 6px;
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: var(--radius-sm);
  transition: width var(--transition-fast);
}

.trend-chart {
  padding: var(--spacing-md);
}

.trend-bars {
  display: flex;
  align-items: flex-end;
  gap: var(--spacing-sm);
  height: 200px;
  margin-bottom: var(--spacing-md);
}

.trend-bar-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
}

.trend-bar-group {
  display: flex;
  gap: 2px;
  height: 100%;
  align-items: flex-end;
}

.trend-bar {
  width: 12px;
  border-radius: var(--radius-sm);
  transition: height var(--transition-fast);
  min-height: 4px;
}

.trend-bar.completion {
  background: var(--primary-color);
}

.trend-bar.fatigue-mom {
  background: #EC4899;
}

.trend-bar.fatigue-dad {
  background: #3B82F6;
}

.trend-label {
  font-size: 12px;
  color: var(--text-tertiary);
}

.trend-legend {
  display: flex;
  justify-content: center;
  gap: var(--spacing-lg);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: 14px;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: var(--radius-sm);
}

.legend-color.completion {
  background: var(--primary-color);
}

.legend-color.fatigue-mom {
  background: #EC4899;
}

.legend-color.fatigue-dad {
  background: #3B82F6;
}

.load-balance {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.balance-chart {
  display: flex;
  height: 40px;
  border-radius: var(--radius-md);
  overflow: hidden;
}

.balance-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  font-weight: 600;
  transition: width var(--transition-fast);
  min-width: 60px;
}

.balance-bar.mom {
  background: #EC4899;
}

.balance-bar.dad {
  background: #3B82F6;
}

.balance-bar.shared {
  background: #10B981;
}

.balance-tip {
  padding: var(--spacing-md);
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  font-size: 14px;
  color: var(--text-secondary);
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .analytics-container {
    padding: 0; /* Remove padding since App.vue handles it */
  }

  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }

  .header h1 {
    font-size: 24px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }

  .task-category-list {
    flex-direction: column;
    gap: var(--spacing-sm);
  }

  .balance-visual {
    height: 24px;
  }
}
</style>
