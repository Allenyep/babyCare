<script setup lang="ts">
import { ref } from 'vue'

const activeTab = ref('general')

// General settings
const generalSettings = ref({
  language: 'zh-CN',
  theme: 'light',
  notifications: true,
  reminderTime: 15,
  autoSchedule: true
})

// Schedule settings
const scheduleSettings = ref({
  startEarly: '06:00',
  endNight: '22:00',
  napTime: '12:00-14:00',
  optimizeFor: 'balance' as 'balance' | 'sleep',
  strictMode: false
})

// Family settings
const familyMembers = ref([
  { id: 1, name: '妈妈', role: 'primary', workHours: '09:00-18:00', targetSleep: 7.5 },
  { id: 2, name: '爸爸', role: 'secondary', workHours: '10:00-19:00', targetSleep: 7.5 }
])

// Knowledge base settings
const knowledgeSettings = ref({
  vaccineReminders: true,
  foodRecommendations: true,
  educationTips: true,
  customKnowledge: [] as string[]
})

// Data settings
const dataSettings = ref({
  autoBackup: true,
  backupFrequency: 'daily' as 'daily' | 'weekly',
  retentionDays: 90,
  exportFormat: 'json' as 'json' | 'csv'
})

function saveGeneralSettings() {
  console.log('Saving general settings:', generalSettings.value)
  // TODO: API call
}

function saveScheduleSettings() {
  console.log('Saving schedule settings:', scheduleSettings.value)
  // TODO: API call
}

function saveFamilySettings() {
  console.log('Saving family settings:', familyMembers.value)
  // TODO: API call
}

function saveKnowledgeSettings() {
  console.log('Saving knowledge settings:', knowledgeSettings.value)
  // TODO: API call
}

function saveDataSettings() {
  console.log('Saving data settings:', dataSettings.value)
  // TODO: API call
}

function exportData() {
  console.log('Exporting data')
  // TODO: API call
}

function importData() {
  console.log('Importing data')
  // TODO: Open file picker and API call
}

function clearCache() {
  console.log('Clearing cache')
  // TODO: API call
}
</script>

<template>
  <div class="settings-container">
    <!-- Header -->
    <header class="header">
      <h1>⚙️ 设置</h1>
    </header>

    <n-card class="settings-card">
      <n-tabs v-model:value="activeTab" type="line">
        <!-- General Settings -->
        <n-tab-pane name="general" tab="通用设置">
          <div class="settings-section">
            <div class="setting-item">
              <div class="setting-label">
                <span class="label">语言</span>
                <span class="description">选择应用显示语言</span>
              </div>
              <n-select v-model:value="generalSettings.language" style="width: 200px">
                <n-option value="zh-CN" label="简体中文" />
                <n-option value="en-US" label="English" />
              </n-select>
            </div>

            <n-divider />

            <div class="setting-item">
              <div class="setting-label">
                <span class="label">主题</span>
                <span class="description">选择应用外观主题</span>
              </div>
              <n-radio-group v-model:value="generalSettings.theme">
                <n-radio value="light">浅色</n-radio>
                <n-radio value="dark">深色</n-radio>
                <n-radio value="auto">跟随系统</n-radio>
              </n-radio-group>
            </div>

            <n-divider />

            <div class="setting-item">
              <div class="setting-label">
                <span class="label">通知提醒</span>
                <span class="description">启用任务提醒通知</span>
              </div>
              <n-switch v-model:value="generalSettings.notifications" />
            </div>

            <n-divider />

            <div class="setting-item">
              <div class="setting-label">
                <span class="label">提醒时间</span>
                <span class="description">任务开始前多少分钟提醒</span>
              </div>
              <n-input-number
                v-model:value="generalSettings.reminderTime"
                :min="5"
                :max="60"
                :step="5"
                style="width: 150px"
              >
                <template #suffix>
                  分钟
                </template>
              </n-input-number>
            </div>

            <n-divider />

            <div class="setting-item">
              <div class="setting-label">
                <span class="label">自动排程</span>
                <span class="description">自动生成每日任务计划</span>
              </div>
              <n-switch v-model:value="generalSettings.autoSchedule" />
            </div>

            <div class="settings-actions">
              <n-button type="primary" @click="saveGeneralSettings">
                保存设置
              </n-button>
            </div>
          </div>
        </n-tab-pane>

        <!-- Schedule Settings -->
        <n-tab-pane name="schedule" tab="排程设置">
          <div class="settings-section">
            <div class="setting-item">
              <div class="setting-label">
                <span class="label">早间开始时间</span>
                <span class="description">一天中第一个时段的开始时间</span>
              </div>
              <n-time-picker v-model:value="scheduleSettings.startEarly" format="HH:mm" />
            </div>

            <n-divider />

            <div class="setting-item">
              <div class="setting-label">
                <span class="label">夜间结束时间</span>
                <span class="description">夜间时段的结束时间</span>
              </div>
              <n-time-picker v-model:value="scheduleSettings.endNight" format="HH:mm" />
            </div>

            <n-divider />

            <div class="setting-item">
              <div class="setting-label">
                <span class="label">午休时间</span>
                <span class="description">宝宝的固定午睡时间</span>
              </div>
              <n-input
                v-model:value="scheduleSettings.napTime"
                placeholder="例如: 12:00-14:00"
                style="width: 200px"
              />
            </div>

            <n-divider />

            <div class="setting-item">
              <div class="setting-label">
                <span class="label">优化目标</span>
                <span class="description">任务分配的主要优化目标</span>
              </div>
              <n-radio-group v-model:value="scheduleSettings.optimizeFor">
                <n-radio value="balance">负载均衡</n-radio>
                <n-radio value="sleep">睡眠优先</n-radio>
              </n-radio-group>
            </div>

            <n-divider />

            <div class="setting-item">
              <div class="setting-label">
                <span class="label">严格模式</span>
                <span class="description">严格按照时间表执行任务</span>
              </div>
              <n-switch v-model:value="scheduleSettings.strictMode" />
            </div>

            <div class="settings-actions">
              <n-button type="primary" @click="saveScheduleSettings">
                保存设置
              </n-button>
            </div>
          </div>
        </n-tab-pane>

        <!-- Family Settings -->
        <n-tab-pane name="family" tab="家庭成员">
          <div class="settings-section">
            <div class="members-list">
              <div
                v-for="member in familyMembers"
                :key="member.id"
                class="member-card"
              >
                <div class="member-header">
                  <h3>{{ member.name }}</h3>
                  <n-button size="small" text>编辑</n-button>
                </div>
                <div class="member-details">
                  <div class="detail-row">
                    <span class="label">角色:</span>
                    <span>{{ member.role === 'primary' ? '主要照顾者' : '辅助照顾者' }}</span>
                  </div>
                  <div class="detail-row">
                    <span class="label">工作时间:</span>
                    <span>{{ member.workHours }}</span>
                  </div>
                  <div class="detail-row">
                    <span class="label">目标睡眠:</span>
                    <span>{{ member.targetSleep }} 小时</span>
                  </div>
                </div>
              </div>
            </div>

            <n-button type="primary" style="width: 100%; margin-top: var(--spacing-md)">
              + 添加成员
            </n-button>

            <div class="settings-actions">
              <n-button type="primary" @click="saveFamilySettings">
                保存设置
              </n-button>
            </div>
          </div>
        </n-tab-pane>

        <!-- Knowledge Settings -->
        <n-tab-pane name="knowledge" tab="知识库">
          <div class="settings-section">
            <div class="setting-item">
              <div class="setting-label">
                <span class="label">疫苗提醒</span>
                <span class="description">根据宝宝年龄提醒疫苗接种时间</span>
              </div>
              <n-switch v-model:value="knowledgeSettings.vaccineReminders" />
            </div>

            <n-divider />

            <div class="setting-item">
              <div class="setting-label">
                <span class="label">辅食推荐</span>
                <span class="description">根据月龄推荐合适的辅食</span>
              </div>
              <n-switch v-model:value="knowledgeSettings.foodRecommendations" />
            </div>

            <n-divider />

            <div class="setting-item">
              <div class="setting-label">
                <span class="label">早教建议</span>
                <span class="description">提供适龄的早教活动建议</span>
              </div>
              <n-switch v-model:value="knowledgeSettings.educationTips" />
            </div>

            <n-divider />

            <div class="setting-item full-width">
              <div class="setting-label">
                <span class="label">自定义知识</span>
                <span class="description">添加自定义的育儿知识和经验</span>
              </div>
              <n-input
                type="textarea"
                placeholder="输入自定义知识内容..."
                :rows="4"
                style="margin-top: var(--spacing-sm)"
              />
            </div>

            <div class="settings-actions">
              <n-button type="primary" @click="saveKnowledgeSettings">
                保存设置
              </n-button>
            </div>
          </div>
        </n-tab-pane>

        <!-- Data Settings -->
        <n-tab-pane name="data" tab="数据管理">
          <div class="settings-section">
            <div class="setting-item">
              <div class="setting-label">
                <span class="label">自动备份</span>
                <span class="description">定期自动备份数据</span>
              </div>
              <n-switch v-model:value="dataSettings.autoBackup" />
            </div>

            <n-divider />

            <div class="setting-item">
              <div class="setting-label">
                <span class="label">备份频率</span>
                <span class="description">数据备份的频率</span>
              </div>
              <n-radio-group v-model:value="dataSettings.backupFrequency">
                <n-radio value="daily">每天</n-radio>
                <n-radio value="weekly">每周</n-radio>
              </n-radio-group>
            </div>

            <n-divider />

            <div class="setting-item">
              <div class="setting-label">
                <span class="label">数据保留</span>
                <span class="description">保留数据的天数</span>
              </div>
              <n-input-number
                v-model:value="dataSettings.retentionDays"
                :min="30"
                :max="365"
                :step="30"
                style="width: 150px"
              >
                <template #suffix>
                  天
                </template>
              </n-input-number>
            </div>

            <n-divider />

            <div class="setting-item">
              <div class="setting-label">
                <span class="label">导出格式</span>
                <span class="description">数据导出的文件格式</span>
              </div>
              <n-radio-group v-model:value="dataSettings.exportFormat">
                <n-radio value="json">JSON</n-radio>
                <n-radio value="csv">CSV</n-radio>
              </n-radio-group>
            </div>

            <n-divider />

            <div class="setting-item full-width">
              <div class="setting-label">
                <span class="label">数据操作</span>
                <span class="description">导出、导入或清除数据</span>
              </div>
              <n-space style="margin-top: var(--spacing-sm)">
                <n-button @click="exportData">
                  📤 导出数据
                </n-button>
                <n-button @click="importData">
                  📥 导入数据
                </n-button>
                <n-button type="warning" @click="clearCache">
                  🗑️ 清除缓存
                </n-button>
              </n-space>
            </div>

            <div class="settings-actions">
              <n-button type="primary" @click="saveDataSettings">
                保存设置
              </n-button>
            </div>
          </div>
        </n-tab-pane>
      </n-tabs>
    </n-card>

    <!-- About -->
    <n-card class="about-card">
      <div class="about-content">
        <h3>关于 BabyCare</h3>
        <p>版本: 1.0.0</p>
        <p>智能家庭育儿助手 - 基于智能分配和负载均衡的育儿管理平台</p>
        <n-space style="margin-top: var(--spacing-md)">
          <n-button text>使用文档</n-button>
          <n-button text>隐私政策</n-button>
          <n-button text>开源许可</n-button>
          <n-button text type="error">反馈问题</n-button>
        </n-space>
      </div>
    </n-card>
  </div>
</template>

<style scoped>
.settings-container {
  padding: var(--spacing-md);
  max-width: 1000px;
  margin: 0 auto;
}

.header {
  margin-bottom: var(--spacing-lg);
}

.header h1 {
  font-size: 28px;
  font-weight: 600;
  margin: 0;
}

.settings-card {
  margin-bottom: var(--spacing-lg);
}

.settings-section {
  padding: var(--spacing-md);
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) 0;
}

.setting-item.full-width {
  flex-direction: column;
  align-items: flex-start;
}

.setting-label {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.label {
  font-weight: 600;
  font-size: 16px;
}

.description {
  font-size: 14px;
  color: var(--text-tertiary);
}

.settings-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}

.members-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.member-card {
  padding: var(--spacing-md);
  background: var(--bg-tertiary);
  border-radius: var(--radius-lg);
}

.member-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.member-header h3 {
  font-size: 18px;
  margin: 0;
}

.member-details {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.detail-row {
  display: flex;
  gap: var(--spacing-sm);
  font-size: 14px;
}

.detail-row .label {
  font-weight: 600;
  color: var(--text-secondary);
}

.about-card {
  margin-bottom: var(--spacing-lg);
}

.about-content {
  text-align: center;
}

.about-content h3 {
  font-size: 18px;
  margin-bottom: var(--spacing-sm);
}

.about-content p {
  font-size: 14px;
  color: var(--text-secondary);
  margin: var(--spacing-xs) 0;
}
</style>
