# BabyCare MVP - 快速启动指南

## MVP 核心功能概览

✅ **已实现的核心功能：**

### 1. 用户界面 (Frontend)
- 📊 **今日看板** - 时间段任务视图、疲劳度仪表盘
- 👶 **宝宝档案** - 宝宝信息管理、生长记录
- 📝 **任务管理** - 任务CRUD、状态过滤
- 📅 **日程安排** - 日/周视图、进度追踪
- 📈 **数据分析** - 疲劳度分析、任务统计
- ⚙️ **系统设置** - 全面配置管理

### 2. 后端服务 (Backend)
- 🗄️ **数据库模型** - Baby, Parent, Task, FatigueRecord, SleepRecord
- 📚 **知识库服务** - 疫苗、辅食、早教、发育里程碑
- 📋 **任务调度器** - 自动生成每日SOP、智能任务分配
- 😴 **疲劳度计算** - 多因素疲劳评分算法
- ⚖️ **负载均衡优化** - 任务分配优化建议

### 3. API 集成
- 🔌 **完整REST API** - 35+ 个端点
- 📡 **API Client** - Axios封装、拦截器、错误处理
- 💾 **状态管理** - Pinia stores (baby, task)

## 快速启动

### 前置要求
- Python 3.9+
- Node.js 16+
- SQLite (自带)

### 后端启动

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端文档：http://localhost:8000/docs

### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端访问：http://localhost:5173

## API 端点概览

### 宝宝管理
- `POST /api/v1/babies/` - 创建宝宝档案
- `GET /api/v1/babies/` - 获取所有宝宝
- `GET /api/v1/babies/{id}` - 获取宝宝详情
- `PATCH /api/v1/babies/{id}` - 更新宝宝信息
- `DELETE /api/v1/babies/{id}` - 删除宝宝

### 任务管理
- `POST /api/v1/tasks/` - 创建任务
- `GET /api/v1/tasks/` - 获取任务列表
- `PATCH /api/v1/tasks/{id}` - 更新任务
- `DELETE /api/v1/tasks/{id}` - 删除任务

### 知识库
- `GET /api/v1/knowledge/vaccines` - 获取疫苗推荐
- `GET /api/v1/knowledge/foods` - 获取辅食推荐
- `GET /api/v1/knowledge/activities` - 获取早教活动
- `GET /api/v1/knowledge/comprehensive` - 综合知识查询

### 调度器
- `POST /api/v1/scheduler/generate` - 生成每日日程
- `POST /api/v1/scheduler/preview` - 预览日程
- `GET /api/v1/scheduler/statistics` - 获取统计信息
- `POST /api/v1/scheduler/optimize` - 优化负载均衡

### 疲劳度
- `POST /api/v1/fatigue/calculate` - 计算疲劳度
- `GET /api/v1/fatigue/trend/{parent_id}` - 获取疲劳度趋势
- `GET /api/v1/fatigue/analyze/{parent_id}` - 分析疲劳度
- `GET /api/v1/fatigue/compare` - 对比父母疲劳度

## MVP 测试流程

### 1. 创建宝宝档案

```bash
curl -X POST "http://localhost:8000/api/v1/babies/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "宝宝",
    "nickname": "小宝",
    "birthday": "2025-03-20",
    "gender": "male"
  }'
```

### 2. 生成每日日程

```bash
curl -X POST "http://localhost:8000/api/v1/scheduler/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "baby_id": 1,
    "date": "2026-03-20",
    "include_knowledge_tasks": true,
    "include_recurring_tasks": true
  }'
```

### 3. 获取知识库推荐

```bash
# 获取6月龄宝宝的辅食推荐
curl "http://localhost:8000/api/v1/knowledge/foods?age_months=6"

# 获取6月龄宝宝的早教活动
curl "http://localhost:8000/api/v1/knowledge/activities?age_months=6"
```

### 4. 计算疲劳度

```bash
curl -X POST "http://localhost:8000/api/v1/fatigue/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "parent_id": 1,
    "record_date": "2026-03-20",
    "total_tasks": 8,
    "total_task_duration": 180,
    "actual_sleep": 6.5,
    "target_sleep": 8.0,
    "work_hours": 8
  }'
```

### 5. 优化负载均衡

```bash
curl -X POST "http://localhost:8000/api/v1/scheduler/optimize?baby_id=1&target_date=2026-03-20&optimize_for=balance"
```

## 核心算法说明

### 疲劳度计算公式

```
fatigue_score = 0.4 * task_load + 0.4 * sleep_deficit + 0.2 * work_impact

其中：
- task_load = min(task_hours * 0.15, 1.0)          # 任务负载
- sleep_deficit = min(sleep_gap * 0.12, 1.0)       # 睡眠不足
- work_impact = min(work_hours * 0.05, 1.0)        # 工作影响

结果范围: 0.0 (精力充沛) - 1.0 (极度疲劳)
```

### 负载均衡评分

```
balance_score = 1.0 - |ratio_1 - 0.5| - |ratio_2 - 0.5|

其中：
- ratio_1 = parent_1_tasks / total_tasks
- ratio_2 = parent_2_tasks / total_tasks

结果范围: 0.0 (完全不均衡) - 1.0 (完全均衡)
```

## 项目结构

```
babyCare/
├── backend/
│   ├── app/
│   │   ├── api/              # API端点
│   │   ├── models/           # 数据库模型
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # 业务逻辑
│   │   │   ├── knowledge_base.py    # 知识库
│   │   │   ├── scheduler.py         # 调度器
│   │   │   ├── fatigue_calculator.py # 疲劳度计算
│   │   │   └── optimizer.py          # 优化器
│   │   └── core/             # 配置
│   └── main.py
│
└── frontend/
    ├── src/
    │   ├── api/              # API client
    │   ├── stores/           # Pinia stores
    │   ├── views/            # 页面组件
    │   └── types/            # TypeScript类型
    └── .env.development      # 环境变量
```

## MVP 限制

当前MVP版本的已知限制：

1. **数据持久化**
   - 使用SQLite，生产环境建议使用PostgreSQL
   - 部分数据仍为mock（如parent详情）

2. **认证授权**
   - 未实现用户认证
   - 未实现权限控制

3. **优化算法**
   - 负载均衡使用简化启发式算法
   - 未实现复杂的线性规划优化

4. **实时更新**
   - 使用轮询而非WebSocket
   - 无实时通知

## 下一步计划

- [ ] 实现用户认证 (JWT)
- [ ] 添加WebSocket实时通知
- [ ] 实现复杂的优化算法 (PuLP)
- [ ] 添加数据导出功能
- [ ] 完善单元测试
- [ ] Docker容器化部署

## 技术栈

**后端:**
- FastAPI 0.115.6
- SQLAlchemy 2.0.37
- Pydantic 2.10.5
- Python 3.9+

**前端:**
- Vue 3.4+
- TypeScript 5.0+
- Vite 5.0+
- Naive UI
- Pinia
- Axios

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License
