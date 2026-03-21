# 前端功能规范

## 一、技术架构

### 1.1 技术栈
```
Vue 3.4+              # 渐进式框架
TypeScript 5.0+       # 类型系统
Vite 5.0+             # 构建工具
Naive UI              # UI组件库（大屏友好）
Pinia                 # 状态管理
VueRouter 4.x         # 路由管理
VueUse                # 组合式工具集
ECharts               # 数据可视化（可选）
```

### 1.2 项目结构
```
frontend/
├── src/
│   ├── main.ts              # 应用入口
│   ├── App.vue              # 根组件
│   │
│   ├── views/               # 页面组件
│   │   ├── Home.vue              # 首页/今日看板
│   │   ├── BabyProfile.vue       # 宝宝档案
│   │   ├── ParentManage.vue      # 家庭成员
│   │   ├── TaskList.vue          # 任务列表
│   │   ├── Schedule.vue          # 日程视图
│   │   ├── Analytics.vue         # 数据分析
│   │   └── Settings.vue          # 设置
│   │
│   ├── components/          # 通用组件
│   │   ├── layout/
│   │   │   ├── AppHeader.vue     # 顶部栏
│   │   │   ├── AppSidebar.vue    # 侧边栏
│   │   │   └── AppFooter.vue     # 底部栏
│   │   ├── baby/
│   │   │   ├── BabyCard.vue      # 宝宝卡片
│   │   │   ├── GrowthChart.vue   # 成长曲线
│   │   │   └── BabyForm.vue      # 宝宝表单
│   │   ├── task/
│   │   │   ├── TaskCard.vue      # 任务卡片
│   │   │   ├── TaskTimeline.vue  # 任务时间轴
│   │   │   ├── TaskForm.vue      # 任务表单
│   │   │   └── TaskModal.vue     # 任务弹窗
│   │   ├── parent/
│   │   │   ├── ParentCard.vue    # 父母卡片
│   │   │   ├── FatigueMeter.vue  # 疲劳度仪表
│   │   │   └── ParentForm.vue    # 父母表单
│   │   └── common/
│   │       ├── TimeSlot.vue      # 时间段选择
│   │       ├── DatePicker.vue    # 日期选择
│   │       └── ConfirmDialog.vue # 确认对话框
│   │
│   ├── stores/              # Pinia状态管理
│   │   ├── baby.ts               # 宝宝状态
│   │   ├── parent.ts             # 父母状态
│   │   ├── task.ts               # 任务状态
│   │   ├── schedule.ts           # 日程状态
│   │   └── app.ts                # 应用状态
│   │
│   ├── api/                # API调用
│   │   ├── baby.ts
│   │   ├── parent.ts
│   │   ├── task.ts
│   │   ├── schedule.ts
│   │   └── analytics.ts
│   │
│   ├── types/              # TypeScript类型
│   │   ├── baby.ts
│   │   ├── parent.ts
│   │   ├── task.ts
│   │   └── common.ts
│   │
│   ├── composables/        # 组合式函数
│   │   ├── useBaby.ts             # 宝宝相关逻辑
│   │   ├── useTask.ts             # 任务相关逻辑
│   │   ├── useFatigue.ts          # 疲劳度计算
│   │   └── useSchedule.ts         # 日程相关逻辑
│   │
│   ├── utils/              # 工具函数
│   │   ├── date.ts               # 日期处理
│   │   ├── format.ts             # 格式化
│   │   └── validation.ts         # 验证
│   │
│   └── assets/             # 静态资源
│       ├── styles/
│       │   ├── main.css       # 全局样式
│       │   ├── variables.css  # CSS变量
│       │   └── tablet.css     # 平板适配
│       └── images/
│
├── public/                     # 静态文件
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```

---

## 二、页面设计

### 2.1 首页/今日看板 (Home.vue)

**功能描述**
- 显示今日任务概览
- 按时间段展示任务
- 显示疲劳度和睡眠统计
- 快速操作入口

**布局结构**
```
┌─────────────────────────────────────────┐
│ 🏠 BabyCare        2026年3月20日 周四  │
├─────────────────────────────────────────┤
│                                         │
│ 👶 小宝 (9个月)    [切换宝宝 ▼]         │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 📊 今日概览                          │ │
│ │ ├ 已完成 5/12 任务  ███████░░ 42%   │ │
│ │ ├ 妈妈疲劳度: ██████░░░ 0.35 ⚠️     │ │
│ │ ├ 爸爸疲劳度: ████░░░░░ 0.25 ✅     │ │
│ │ ├ 妈妈睡眠: 6.5h (目标7.5h)        │ │
│ │ └ 爸爸睡眠: 7.5h (目标7.5h) ✅    │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ 🌅 早间 (06:00-09:00)                  │
│ ┌─────────────────────────────────────┐ │
│ │ ✅ 喂奶              妈妈  06:30   │ │
│ │ ✅ 换尿布            爸爸  06:45   │ │
│ │ ⏳ 晨间互动          爸爸  进行中  │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ☀️ 上午 (09:00-12:00)                  │
│ ┌─────────────────────────────────────┐ │
│ │ 📝 积木游戏          爸爸  未开始  │ │
│ │ 🥣 蔬菜泥            妈妈  未开始  │ │
│ │ 🚶 户外活动          爸爸  未开始  │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ... (其他时间段)                        │
│                                         │
│ 🌙 夜间值班                             │
│ ┌─────────────────────────────────────┐ │
│ │ 🌛 22:00-02:00  爸爸  值班中       │ │
│ │ 🌜 02:00-06:00  妈妈  待值班       │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ [查看完整日程] [➕ 快速添加任务]         │
└─────────────────────────────────────────┘
```

**核心功能**
- 切换宝宝（多宝宝支持）
- 查看今日概览统计
- 按时间段查看任务
- 快速完成任务（点击打勾）
- 任务拖拽重新分配
- 查看完整日程

**状态管理**
```typescript
interface HomeState {
  currentBaby: Baby | null
  todaySchedule: Schedule | null
  loading: boolean
  error: string | null
}
```

---

### 2.2 宝宝档案 (BabyProfile.vue)

**功能描述**
- 创建和编辑宝宝信息
- 记录生长数据
- 查看成长曲线
- 管理家庭成员

**布局结构**
```
┌─────────────────────────────────────────┐
│ ← 宝宝档案                               │
├─────────────────────────────────────────┤
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │          👶 小宝 (9个月)             │ │
│ │     [上传照片]                       │ │
│ │                                     │ │
│ │ 生日: 2025-06-15                    │ │
│ │ 性别: ♂ 男孩                        │ │
│ │                                     │ │
│ │ [编辑信息] [添加家庭成员]           │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 📏 成长记录                          │ │
│ │                                     │ │
│ │ 体重曲线图（ECharts）               │ │
│ │ 身高曲线图                          │ │
│ │                                     │ │
│ │ [+ 添加记录]                        │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 👨‍👩‍👧 家庭成员                          │ │
│ │                                     │ │
│ │ 👩 妈妈 (主要照护者)                │ │
│ │ ├ 工作时间: 09:00-18:00             │ │
│ │ ├ 目标睡眠: 7.5小时                │ │
│ │ └ 当前疲劳度: 0.35 ⚠️              │ │
│ │                                     │ │
│ │ 👨 爸爸 (主要照护者)                │ │
│ │ ├ 工作时间: 10:00-19:00             │ │
│ │ ├ 目标睡眠: 7.5小时                │ │
│ │ └ 当前疲劳度: 0.25 ✅              │ │
│ │                                     │ │
│ │ [+ 添加成员]                        │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**核心功能**
- 创建/编辑宝宝信息
- 上传/更换头像
- 添加生长记录
- 可视化成长曲线
- 添加/编辑家庭成员
- 查看成员疲劳度

**表单字段**
```typescript
interface BabyForm {
  name: string
  nickname: string
  birthday: Date
  gender: 'male' | 'female'
  avatar?: string
}

interface GrowthForm {
  record_date: Date
  weight?: number
  height?: number
  head_circumference?: number
  notes?: string
}
```

---

### 2.3 任务管理 (TaskList.vue)

**功能描述**
- 查看所有任务（按日期筛选）
- 手动创建自定义任务
- 编辑任务详情
- 删除任务
- 批量操作

**布局结构**
```
┌─────────────────────────────────────────┐
│ ← 任务管理                               │
├─────────────────────────────────────────┤
│                                         │
│ [今天] [本周] [本月] [全部] ▼           │
│                                         │
│ [搜索任务...]  [➕ 添加任务]            │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 📅 今天 3月20日                      │ │
│ │                                     │ │
│ │ ✅ 喂奶        早间  妈妈  06:30    │ │
│ │ ✅ 换尿布      早间  爸爸  06:45    │ │
│ │ 📝 积木游戏    上午  爸爸           │ │
│ │ 🥣 蔬菜泥      上午  妈妈           │ │
│ │ 🚶 户外活动    下午  爸爸           │ │
│ │ 🛁 给宝宝洗澡  晚上  爸爸           │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 📅 明天 3月21日                      │ │
│ │                                     │ │
│ │ 📝 早餐奶      早间  待分配         │ │
│ │ 📝 手指食物    中午  待分配         │ │
│ │ 📝 翻身练习    下午  待分配         │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ [显示更多...]                           │
└─────────────────────────────────────────┘
```

**核心功能**
- 按日期查看任务
- 筛选任务状态（全部/待完成/已完成）
- 快速添加任务
- 编辑任务（点击进入详情）
- 批量删除
- 任务导出（未来）

**任务详情弹窗**
```
┌─────────────────────────────────────┐
│ 任务详情                      [关闭]│
├─────────────────────────────────────┤
│                                     │
│ 📝 积木游戏                          │
│ 分类: 早教游戏                       │
│ 时长: 30分钟                         │
│                                     │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                     │
│ 📅 时间: 今天 上午 (09:00-12:00)    │
│ 👤 分配给: 爸爸                      │
│ 📊 优先级: 中等 (5/10)               │
│                                     │
│ 描述:                                │
│ 堆积木游戏，锻炼宝宝精细动作和空间  │
│ 感知。可以使用软体积木，确保安全。  │
│                                     │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                     │
│ [编辑] [删除] [标记完成]            │
└─────────────────────────────────────┘
```

---

### 2.4 日程视图 (Schedule.vue)

**功能描述**
- 日历视图查看日程
- 周视图/月视图切换
- 快速跳转到指定日期
- 查看每日统计

**布局结构**
```
┌─────────────────────────────────────────┐
│ ← 日历                                   │
├─────────────────────────────────────────┤
│                                         │
│ [< 2026年3月 >]  [周视图 ▼] [今天]      │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 周一 周二 周三 周四 周五 周六 周日   │ │
│ │  14   15   16   17   18   19   20    │ │
│ │                                     │ │
│ │  ✅   ✅   ✅   ✅   ✅   ⏳   ⏳    │ │
│ │                                     │ │
│ │  12   13   14   12   13   15   15    │ │
│ │ 任务 任务 任务 任务 任务 任务 任务  │ │
│ │                                     │ │
│ │  ⚠️  ✅  ⚠️  ⚠️  ⚠️  ⚠️  ⚠️        │ │
│ │  均衡 均衡 疲劳 疲劳 疲劳 疲劳 疲劳  │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 📅 今天 3月20日 周四                 │ │
│ │                                     │ │
│ │ 总任务: 12  |  已完成: 5  |  待完成:7│ │
│ │ 完成率: 42%  |  均衡度: 0.1 ✅     │ │
│ │                                     │ │
│ │ [查看详细任务] [生成明日日程]       │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**核心功能**
- 日历视图（周/月）
- 每日任务数量和均衡度
- 点击日期查看详情
- 自动生成明日日程
- 调整历史日程

---

### 2.5 数据分析 (Analytics.vue)

**功能描述**
- 疲劳度趋势图
- 睡眠时间统计
- 任务完成率
- 洞察与建议

**布局结构**
```
┌─────────────────────────────────────────┐
│ ← 数据分析                               │
├─────────────────────────────────────────┤
│                                         │
│ [近7天] [近30天] [近3月] ▼             │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 📊 疲劳度趋势                        │ │
│ │                                     │ │
│ │   1.0 ┤                              │ │
│ │   0.8 ┤  ●                           │ │
│ │   0.6 ┤      ●    ●                 │ │
│ │   0.4 ┤  ●         ●     ●          │ │
│ │   0.2 ┤                  ●     ●     │ │
│ │   0.0 ┼──────────────────────────  │ │
│ │        14  15  16  17  18  19  20    │ │
│ │                                     │ │
│ │ ── 妈妈  ── 爸爸                    │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 😴 睡眠统计                          │ │
│ │                                     │ │
│ │ 妈妈: 平均 6.8h (目标7.5h) ⚠️       │ │
│ │ 爸爸: 平均 7.2h (目标7.5h) ✅       │ │
│ │                                     │ │
│ │ [查看详细记录]                      │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ ✅ 任务完成率                        │ │
│ │                                     │ │
│ │ 本周: 85%  ├──────── 85% ────────   │ │
│ │ 上周: 78%  ├──────── 78% ────      │ │
│ │                                     │ │
│ │ [分类统计]                          │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 💡 洞察与建议                        │ │
│ │                                     │ │
│ │ ⚠️ 警告                            │ │
│ │ • 妈妈连续3天睡眠不足7小时          │ │
│ │                                     │ │
│ │ 💡 建议                            │ │
│ │ • 今晚早点休息，夜间值班交给爸爸    │ │
│ │ • 周末可以考虑让奶奶帮忙            │ │
│ │                                     │ │
│ │ 🏆 成就                            │ │
│ │ • 连续7天按时接种疫苗 ✅            │ │
│ │ • 爸爸本周承担夜间任务50% 🌟        │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**核心功能**
- 疲劳度趋势图（ECharts）
- 睡眠时间统计
- 任务完成率对比
- 系统建议展示
- 导出报告

---

### 2.6 设置 (Settings.vue)

**功能描述**
- 应用设置
- 数据管理
- 关于

**布局结构**
```
┌─────────────────────────────────────────┐
│ ← 设置                                   │
├─────────────────────────────────────────┤
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ ⚙️ 应用设置                          │ │
│ │                                     │ │
│ │ 主题: [浅色 ▼]                       │ │
│ │ 语言: [简体中文 ▼]                   │ │
│ │ 时间格式: [24小时 ▼]                 │ │
│ │                                     │ │
│ │ [保存设置]                           │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 👨‍👩‍👧 家庭成员                          │ │
│ │                                     │ │
│ │ 👩 妈妈 (编辑)                       │ │
│ │ 👨 爸爸 (编辑)                       │ │
│ │ [+ 添加成员]                        │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 💾 数据管理                          │ │
│ │                                     │ │
│ │ [导出数据] [备份数据]               │ │
│ │ [恢复数据] [清空数据]               │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ ℹ️ 关于                              │ │
│ │                                     │ │
│ │ BabyCare v1.0.0                     │ │
│ │ 智能家庭育儿助手                     │ │
│ │                                     │ │
│ │ [用户协议] [隐私政策]               │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**核心功能**
- 主题切换（浅色/深色）
- 语言选择
- 数据导出/备份
- 恢复数据
- 清空数据（需确认）

---

## 三、核心组件设计

### 3.1 TaskCard（任务卡片）

**功能**
- 显示任务信息
- 快速操作（完成/编辑/删除）
- 状态指示
- 拖拽支持

**Props**
```typescript
interface Props {
  task: Task
  showActions?: boolean    // 是否显示操作按钮
  draggable?: boolean      // 是否可拖拽
  readonly?: boolean       // 只读模式
}
```

**Events**
```typescript
const emit = defineEmits<{
  complete: [task: Task]
  edit: [task: Task]
  delete: [task: Task]
  assign: [task: Task, parentId: number]
  dragStart: [task: Task]
  dragEnd: []
}>()
```

**UI设计**
```
┌─────────────────────────────────────┐
│ 📝 积木游戏              [⋮]        │
│                                     │
│ 📊 早教  |  ⏱ 30min  |  ⭐ 5        │
│                                     │
│ 👤 爸爸  |  🕒 09:00-12:00           │
│                                     │
│ [✓ 完成] [编辑] [删除]              │
└─────────────────────────────────────┘
```

---

### 3.2 FatigueMeter（疲劳度仪表）

**功能**
- 可视化显示疲劳度
- 颜色编码（绿/黄/橙/红）
- 数值显示

**Props**
```typescript
interface Props {
  value: number           // 0.0 - 1.0+
  showLabel?: boolean
  size?: 'small' | 'medium' | 'large'
}
```

**UI设计**
```
小尺寸:
  0.35 ⚠️

中等尺寸:
┌─────────────┐
│  0.35 ⚠️   │
│  ██████░░░░ │
│  轻度疲劳   │
└─────────────┘

大尺寸:
  ┌─────────────────┐
  │     0.35        │
  │   ███████░░░    │
  │                 │
  │   ⚠️ 轻度疲劳   │
  │   建议适当休息   │
  └─────────────────┘
```

---

### 3.3 TaskTimeline（任务时间轴）

**功能**
- 按时间段展示任务
- 支持拖拽排序
- 支持拖拽分配

**Props**
```typescript
interface Props {
  tasks: Task[]
  date: Date
  editable?: boolean
}
```

**UI设计**
```
┌─────────────────────────────────────┐
│ 🌅 早间 (06:00-09:00)               │
│ ├─ ✅ 喂奶         妈妈  06:30      │
│ ├─ ✅ 换尿布       爸爸  06:45      │
│ └─ ⏳ 晨间互动     爸爸  进行中     │
│                                     │
│ ☀️ 上午 (09:00-12:00)               │
│ ├─ 📝 积木游戏     爸爸            │
│ ├─ 📝 蔬菜泥       妈妈            │
│ └─ 📝 户外活动     爸爸            │
│                                     │
│ ...                                 │
└─────────────────────────────────────┘
```

---

### 3.4 TimeSlotSelector（时间段选择）

**功能**
- 选择时间段
- 显示时间范围
- 支持自定义

**Props**
```typescript
interface Props {
  modelValue: string      // early/morning/noon/afternoon/evening/night
  showTime?: boolean      // 是否显示时间范围
  editable?: boolean
}
```

**UI设计**
```
下拉选择:
[早间 ▼]
├─ 早间 (06:00-09:00)
├─ 上午 (09:00-12:00)
├─ 中午 (12:00-15:00)
├─ 下午 (15:00-18:00)
├─ 晚上 (18:00-21:00)
└─ 夜间 (21:00-06:00)

按钮选择:
[早间] [上午] [中午] [下午] [晚上] [夜间]
```

---

## 四、状态管理

### 4.1 Store结构

```typescript
// stores/baby.ts
export const useBabyStore = defineStore('baby', {
  state: (): BabyState => ({
    currentBaby: null,
    babies: [],
    loading: false,
    error: null
  }),

  getters: {
    currentBabyAge: (state) => {
      if (!state.currentBaby) return 0
      return calculateAge(state.currentBaby.birthday)
    }
  },

  actions: {
    async fetchBabies() {},
    async createBaby(data) {},
    async updateBaby(id, data) {},
    async deleteBaby(id) {},
    setCurrentBaby(baby) {}
  }
})

// stores/task.ts
export const useTaskStore = defineStore('task', {
  state: (): TaskState => ({
    tasks: [],
    todaySchedule: null,
    loading: false,
    error: null
  }),

  getters: {
    todayTasks: (state) => {
      if (!state.todaySchedule) return []
      return state.todaySchedule.tasks
    },

    pendingTasks: (state) => {
      return state.todaySchedule?.tasks.filter(t => t.status === 'pending') || []
    },

    completedTasks: (state) => {
      return state.todaySchedule?.tasks.filter(t => t.status === 'completed') || []
    }
  },

  actions: {
    async fetchTodaySchedule(babyId) {},
    async completeTask(taskId, data) {},
    async createTask(babyId, data) {},
    async updateTask(taskId, data) {},
    async deleteTask(taskId) {},
    async rebalanceTasks(babyId, options) {}
  }
})

// stores/parent.ts
export const useParentStore = defineStore('parent', {
  state: (): ParentState => ({
    parents: [],
    fatigueScores: {},
    loading: false
  }),

  getters: {
    momFatigue: (state) => state.fatigueScores['mom'],
    dadFatigue: (state) => state.fatigueScores['dad'],
    balanceScore: (state) => {
      const scores = Object.values(state.fatigueScores)
      return Math.abs(scores[0] - scores[1])
    }
  },

  actions: {
    async fetchParents(babyId) {},
    async createParent(babyId, data) {},
    async updateParent(id, data) {},
    async deleteParent(id) {},
    async calculateFatigue(babyId, date) {}
  }
})
```

---

## 五、组合式函数

### 5.1 useTask（任务操作）

```typescript
export function useTask() {
  const taskStore = useTaskStore()

  const completeTask = async (task: Task, notes?: string) => {
    try {
      await taskStore.completeTask(task.id, {
        completed_by: getCurrentUserId(),
        notes
      })

      // 重新计算疲劳度
      await taskStore.fetchTodaySchedule(task.baby_id)

      // 显示成功提示
      message.success('任务已完成！')
    } catch (error) {
      message.error('操作失败')
      console.error(error)
    }
  }

  const rebalance = async (babyId: number, reason?: string) => {
    const dialog = useDialog()
    const confirmed = await dialog.confirm({
      title: '重新分配任务',
      content: '确定要重新分配今天的所有任务吗？'
    })

    if (confirmed) {
      await taskStore.rebalanceTasks(babyId, { reason })
      message.success('任务已重新分配')
    }
  }

  return {
    completeTask,
    rebalance,
    ...toRefs(taskStore)
  }
}
```

### 5.2 useFatigue（疲劳度计算）

```typescript
export function useFatigue() {
  const parentStore = useParentStore()

  const getFatigueLevel = (score: number) => {
    if (score < 0.3) return { level: 'easy', label: '轻松', color: 'success' }
    if (score < 0.5) return { level: 'moderate', label: '适中', color: 'warning' }
    if (score < 0.8) return { level: 'high', label: '疲劳', color: 'error' }
    return { level: 'severe', label: '过度疲劳', color: 'error' }
  }

  const getBalanceLevel = (score: number) => {
    if (score < 0.2) return { level: 'balanced', label: '很均衡', color: 'success' }
    if (score < 0.4) return { level: 'acceptable', label: '基本均衡', color: 'warning' }
    return { level: 'unbalanced', label: '不均衡', color: 'error' }
  }

  return {
    getFatigueLevel,
    getBalanceLevel,
    fatigueScores: computed(() => parentStore.fatigueScores),
    balanceScore: computed(() => parentStore.balanceScore)
  }
}
```

---

## 六、API调用封装

```typescript
// api/task.ts
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
})

export const taskApi = {
  // 获取今日日程
  getTodaySchedule: (babyId: number) =>
    api.get(`/api/babies/${babyId}/schedules/today`),

  // 完成任务
  completeTask: (taskId: number, data: any) =>
    api.patch(`/api/tasks/${taskId}/complete`, data),

  // 创建任务
  createTask: (babyId: number, data: any) =>
    api.post(`/api/babies/${babyId}/tasks`, data),

  // 分配任务
  assignTask: (taskId: number, parentId: number) =>
    api.patch(`/api/tasks/${taskId}/assign`, { parent_id: parentId }),

  // 重新分配
  rebalanceTasks: (babyId: number, options: any) =>
    api.post(`/api/babies/${babyId}/schedules/today/rebalance`, options),

  // 删除任务
  deleteTask: (taskId: number) =>
    api.delete(`/api/tasks/${taskId}`)
}
```

---

## 七、路由配置

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '今日看板' }
  },
  {
    path: '/baby',
    name: 'baby-profile',
    component: () => import('@/views/BabyProfile.vue'),
    meta: { title: '宝宝档案' }
  },
  {
    path: '/tasks',
    name: 'task-list',
    component: () => import('@/views/TaskList.vue'),
    meta: { title: '任务管理' }
  },
  {
    path: '/schedule',
    name: 'schedule',
    component: () => import('@/views/Schedule.vue'),
    meta: { title: '日程' }
  },
  {
    path: '/analytics',
    name: 'analytics',
    component: () => import('@/views/Analytics.vue'),
    meta: { title: '数据分析' }
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('@/views/Settings.vue'),
    meta: { title: '设置' }
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
```

---

## 八、平板/大屏适配

### 8.1 响应式断点

```css
/* styles/variables.css */
:root {
  --breakpoint-tablet: 768px;
  --breakpoint-desktop: 1024px;
  --breakpoint-large: 1280px;
}

/* 大屏优化 */
@media (min-width: 1280px) {
  .task-card {
    padding: 20px;
    font-size: 18px;
  }

  .fatigue-meter {
    transform: scale(1.2);
  }
}

/* 平板横屏 */
@media (min-width: 1024px) and (max-width: 1279px) {
  .time-slot {
    grid-template-columns: 1fr 1fr;
  }
}

/* 平板竖屏 */
@media (min-width: 768px) and (max-width: 1023px) {
  .task-list {
    font-size: 16px;
  }
}
```

### 8.2 触摸优化

```typescript
// 增加触摸目标尺寸
const minTouchSize = 44 // dp

// 长按操作
const handleLongPress = (callback: () => void) => {
  let timer: NodeJS.Timeout

  return {
    onTouchStart: () => {
      timer = setTimeout(callback, 500)
    },
    onTouchEnd: () => {
      clearTimeout(timer)
    }
  }
}

// 滑动手势
import { useSwipe } from '@vueuse/core'

const { direction } = useSwipe(element, {
  onSwipe() {
    if (direction.value === 'left') {
      // 下一页
    } else if (direction.value === 'right') {
      // 上一页
    }
  }
})
```
