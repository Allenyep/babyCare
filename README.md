# BabyCare - 智能家庭育儿助手

> 基于时间线优化和智能分配的家庭育儿管理平台

## 项目简介

BabyCare 是一个面向家庭的智能育儿管理应用，通过自动化任务分配和动态负载均衡，帮助夫妻双方高效协作，最大化家庭整体 wellbeing。

### 核心价值

- 🤖 **智能SOP生成**：根据宝宝月龄自动生成每日育儿任务清单
- ⚖️ **智能负载均衡**：结合时间线自动分配任务，避免一方过度劳累
- 🔄 **动态调整**：根据实际情况灵活调整任务分配
- 📊 **可视化追踪**：睡眠时间、任务完成率、疲劳度一目了然

### 使用场景

- **设备类型**：共享设备（平板/大屏）
- **放置位置**：客厅、卧室等家庭公共区域
- **用户群体**：夫妻双方共同使用

---

## 技术栈

| 分类 | 技术选型 |
|------|---------|
| 前端 | Vue 3 + TypeScript + Vite + Naive UI + Pinia |
| 后端 | FastAPI + Python + SQLAlchemy |
| 数据库 | SQLite (开发) / PostgreSQL (生产) |
| AI | OpenAI API (可选) |
| 部署 | Docker Compose (未来) |

---

## 快速开始

### 环境要求

- Node.js 18+
- Python 3.9+
- SQLite 3

### 本地开发

```bash
# 后端
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload

# 前端
cd frontend
npm install
npm run dev
```

---

## 文档导航

- [产品设计方案](./docs/product-design.md) - 产品定位、功能模块、用户故事
- [后端功能规范](./docs/backend-spec.md) - API设计、数据模型、业务逻辑
- [前端功能规范](./docs/frontend-spec.md) - 页面结构、组件设计、状态管理
- [UI设计方案](./docs/ui-design.md) - 视觉设计、交互规范、布局系统
- [数据模型设计](./docs/data-model.md) - 数据库表结构、关系设计
- [API接口文档](./docs/api-contract.md) - 接口定义、请求响应格式

---

## 项目结构

```
babyCare/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # 业务逻辑
│   │   │   ├── scheduler.py      # 任务调度引擎
│   │   │   ├── knowledge_base.py # 知识库引擎
│   │   │   └── optimizer.py      # 优化算法
│   │   ├── core/           # 核心配置
│   │   └── db/             # 数据库操作
│   ├── tests/              # 测试
│   └── data/               # 预设知识库数据
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   ├── components/     # 通用组件
│   │   ├── stores/         # Pinia状态管理
│   │   ├── api/            # API调用
│   │   ├── types/          # TypeScript类型
│   │   └── assets/         # 静态资源
│   └── public/
└── docs/                   # 文档
```

---

## 功能概览

### MVP功能

- ✅ 宝宝档案管理
- ✅ 家庭成员管理
- ✅ 时间段配置
- ✅ 预设知识库（疫苗、辅食、早教）
- ✅ 手动任务创建和分配
- ✅ 今日任务看板
- ✅ 任务完成记录
- ✅ 睡眠时间追踪
- ✅ 疲劳度计算
- ✅ 简单规则引擎分配任务

### Phase 2 功能

- ⏳ 根据月龄自动生成每日SOP
- ⏳ 智能任务分配算法
- ⏳ 一键重新分配
- ⏳ 疲劳度预警

### Phase 3 功能（可选）

- ⏳ AI个性化建议
- ⏳ 育儿知识问答
- ⏳ 高级优化算法

---

## 开发路线图

### Week 1-2: 基础架构
- [ ] 项目初始化
- [ ] 数据库设计
- [ ] 基础API框架
- [ ] 前端页面框架

### Week 3-4: 核心功能
- [ ] 宝宝档案管理
- [ ] 家庭成员管理
- [ ] 预设知识库
- [ ] 任务CRUD

### Week 5-6: 智能分配
- [ ] 时间线管理
- [ ] 规则引擎
- [ ] 任务分配算法
- [ ] 疲劳度计算

### Week 7-8: 优化完善
- [ ] UI/UX优化
- [ ] 测试覆盖
- [ ] 性能优化
- [ ] 部署准备

---

## 贡献指南

欢迎贡献代码、提出建议或报告问题！

---

## 许可证

MIT License
