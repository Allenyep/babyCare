# 后端功能规范

## 一、技术架构

### 1.1 技术栈
```
FastAPI 0.100+         # Web框架
Python 3.9+           # 编程语言
SQLAlchemy 2.0+       # ORM
Pydantic 2.0+         # 数据验证
SQLite / PostgreSQL   # 数据库
APScheduler           # 定时任务
PuLP / OR-Tools       # 优化算法（可选）
```

### 1.2 项目结构
```
backend/
├── app/
│   ├── main.py              # 应用入口
│   ├── config.py            # 配置管理
│   ├── dependencies.py      # 依赖注入
│   │
│   ├── api/                 # API路由
│   │   ├── __init__.py
│   │   ├── babies.py        # 宝宝档案
│   │   ├── parents.py       # 父母管理
│   │   ├── tasks.py         # 任务管理
│   │   ├── schedules.py     # 日程管理
│   │   └── analytics.py     # 数据分析
│   │
│   ├── models/              # SQLAlchemy模型
│   │   ├── baby.py
│   │   ├── parent.py
│   │   ├── task.py
│   │   ├── schedule.py
│   │   └── analytics.py
│   │
│   ├── schemas/             # Pydantic schemas
│   │   ├── baby.py
│   │   ├── parent.py
│   │   ├── task.py
│   │   └── schedule.py
│   │
│   ├── services/            # 业务逻辑
│   │   ├── knowledge_base.py    # 知识库引擎
│   │   ├── scheduler.py          # 任务调度器
│   │   ├── optimizer.py          # 优化算法
│   │   ├── fatigue_calculator.py # 疲劳度计算
│   │   └── ai_service.py         # AI服务（可选）
│   │
│   ├── core/               # 核心功能
│   │   ├── auth.py          # 认证（未来）
│   │   └── security.py      # 安全
│   │
│   └── db/                 # 数据库
│       ├── base.py
│       ├── session.py
│       └── init_db.py
│
├── data/                   # 预设数据
│   ├── vaccines.json       # 疫苗指南
│   ├── food.json           # 辅食指南
│   ├── education.json      # 早教指南
│   └── routines.json       # 日常活动
│
├── tests/                  # 测试
│   ├── api/
│   ├── services/
│   └── conftest.py
│
├── alembic/                # 数据库迁移（未来）
├── .env.example
├── requirements.txt
└── run.sh
```

---

## 二、数据模型设计

### 2.1 核心实体

#### Baby（宝宝）
```python
class Baby(Base):
    id: int
    name: str                    # 姓名
    nickname: str                # 小名
    birthday: date               # 生日
    gender: enum                 # 性别：male/female
    avatar: str?                 # 头像URL

    # 关系
    parents: List[Parent]
    growth_records: List[GrowthRecord]
    tasks: List[Task]
    schedules: List[Schedule]

    # 索引
    __table_args__ = (
        Index('idx_baby_birthday', 'birthday'),
    )
```

#### GrowthRecord（生长记录）
```python
class GrowthRecord(Base):
    id: int
    baby_id: int                 # 外键
    record_date: date            # 记录日期
    weight: float?               # 体重(kg)
    height: float?               # 身高(cm)
    head_circumference: float?   # 头围(cm)
    notes: str?                  # 备注
    created_at: datetime
```

#### Parent（父母/照护者）
```python
class Parent(Base):
    id: int
    baby_id: int                 # 外键
    name: str                    # 姓名
    relationship: enum           # 关系：mother/father/grandparent/nanny
    avatar: str?                 # 头像URL
    phone: str?                  # 电话

    # 时间约束
    work_start_time: time?       # 工作开始时间
    work_end_time: time?         # 工作结束时间
    sleep_start_time: time?      # 睡眠开始时间
    sleep_end_time: time?        # 睡眠结束时间
    unavailable_slots: JSON      # 不可用时段 [{"day": 1, "start": "09:00", "end": "12:00"}]

    # 能力标签
    capabilities: List[str]      # ["diaper", "feeding", "cooking", "bathing"]

    # 目标
    target_sleep_hours: float    # 目标睡眠时长

    # 关系
    tasks: List[Task]
    completions: List[TaskCompletion]
```

#### TaskTemplate（任务模板）
```python
class TaskTemplate(Base):
    id: int
    name: str                    # 任务名称
    category: enum               # 分类：feeding/diaper/education/food/outdoor/hygiene/medical
    description: str?            # 描述
    duration_minutes: int        # 预计时长

    # 触发条件
    min_age_months: int?         # 最小月龄
    max_age_months: int?         # 最大月龄
    frequency: enum              # 频率：daily/weekly/monthly/once

    # 时间约束
    preferred_time_slots: List[str]  # ["early", "morning", "noon", "afternoon", "evening", "night"]
    required: bool               # 是否必须完成

    # 优先级
    priority: int                # 1-10，数字越大优先级越高

    # 知识库来源
    source: str?                 # "CDC", "营养学会", "自定义"
    source_url: str?             # 参考链接
```

#### Task（任务实例）
```python
class Task(Base):
    id: int
    baby_id: int                 # 外键
    template_id: int?            # 外键（从模板生成）
    schedule_id: int             # 外键（所属日程）

    # 基本信息
    name: str
    category: enum
    description: str?
    duration_minutes: int
    priority: int

    # 时间信息
    date: date                   # 日期
    time_slot: enum              # 时间段
    assigned_to: int?            # 分配给谁（parent_id）

    # 状态
    status: enum                 # pending/in_progress/completed/skipped/cancelled

    # 完成信息
    completed_at: datetime?
    completed_by: int?           # 实际完成人
    completion_notes: str?       # 完成备注

    # 关系
    completion_records: List[TaskCompletion]
```

#### TaskCompletion（完成记录）
```python
class TaskCompletion(Base):
    id: int
    task_id: int                 # 外键
    parent_id: int               # 外键

    completed_at: datetime
    notes: str?
    rating: int?                 # 完成质量评分 1-5
```

#### Schedule（日程）
```python
class Schedule(Base):
    id: int
    baby_id: int                 # 外键
    date: date                   # 日期

    # 统计
    total_tasks: int             # 总任务数
    completed_tasks: int         # 已完成任务数
    completion_rate: float       # 完成率

    # 疲劳度
    fatigue_scores: JSON         # {parent_id: fatigue_score}
    balance_score: float         # 负载均衡度

    # 特殊标记
    is_special_day: bool         # 是否特殊日（宝宝不舒服等）
    special_notes: str?

    # 关系
    tasks: List[Task]
```

#### SleepLog（睡眠记录）
```python
class SleepLog(Base):
    id: int
    baby_id: int                 # 外键
    parent_id: int?              # 记录人

    sleep_type: enum             # nap/night
    start_time: datetime         # 开始时间
    end_time: datetime?          # 结束时间（可能还没醒）
    duration_minutes: int?       # 时长（分钟）

    notes: str?                  # 备注（如：闹觉、容易醒等）
```

---

### 2.2 关系图

```
Baby (1) ──< (N) GrowthRecord
  |
  +── (1) ──< (N) Parent
  |             |
  |             +── (1) ──< (N) Task ──< (N) TaskCompletion
  |             |
  |             +── (1) ──< (N) SleepLog
  |
  +── (1) ──< (N) Schedule ──< (N) Task
                    |
                    └── (N) ──< TaskTemplate
```

---

## 三、API接口设计

### 3.1 宝宝档案管理

#### 创建宝宝
```
POST /api/babies

Request:
{
  "name": "小明",
  "nickname": "明明",
  "birthday": "2025-06-15",
  "gender": "male"
}

Response 201:
{
  "data": {
    "id": 1,
    "name": "小明",
    "nickname": "明明",
    "birthday": "2025-06-15",
    "gender": "male",
    "age_months": 9,  # 自动计算
    "created_at": "2026-03-20T10:00:00Z"
  }
}
```

#### 获取宝宝列表
```
GET /api/babies

Response 200:
{
  "data": [
    {
      "id": 1,
      "name": "小明",
      "nickname": "明明",
      "age_months": 9,
      "avatar": "/static/babies/1.jpg"
    }
  ]
}
```

#### 获取宝宝详情
```
GET /api/babies/{baby_id}

Response 200:
{
  "data": {
    "id": 1,
    "name": "小明",
    "nickname": "明明",
    "birthday": "2025-06-15",
    "gender": "male",
    "age_months": 9,
    "avatar": "/static/babies/1.jpg",
    "parents": [
      {
        "id": 1,
        "name": "妈妈",
        "relationship": "mother"
      },
      {
        "id": 2,
        "name": "爸爸",
        "relationship": "father"
      }
    ],
    "latest_growth": {
      "weight": 9.2,
      "height": 72.5,
      "record_date": "2026-03-15"
    }
  }
}
```

#### 添加生长记录
```
POST /api/babies/{baby_id}/growth

Request:
{
  "record_date": "2026-03-20",
  "weight": 9.5,
  "height": 73.0,
  "head_circumference": 45.5,
  "notes": "宝宝长得很好"
}

Response 201:
{
  "data": {
    "id": 1,
    "baby_id": 1,
    "record_date": "2026-03-20",
    "weight": 9.5,
    "height": 73.0,
    "head_circumference": 45.5
  }
}
```

---

### 3.2 家庭成员管理

#### 添加家庭成员
```
POST /api/babies/{baby_id}/parents

Request:
{
  "name": "妈妈",
  "relationship": "mother",
  "phone": "13800138000",
  "work_start_time": "09:00",
  "work_end_time": "18:00",
  "sleep_start_time": "23:00",
  "sleep_end_time": "07:00",
  "target_sleep_hours": 7.5,
  "capabilities": ["feeding", "diaper", "cooking", "education"],
  "unavailable_slots": [
    {"day": 1, "start": "19:00", "end": "21:00"}  # 周一晚上瑜伽课
  ]
}

Response 201:
{
  "data": {
    "id": 1,
    "name": "妈妈",
    "relationship": "mother",
    "avatar": null,
    "fatigue_score": 0.0,  # 当前疲劳度
    "today_completed": 0   # 今日已完成任务数
  }
}
```

#### 更新成员信息
```
PATCH /api/parents/{parent_id}

Request:
{
  "work_start_time": "10:00",  # 修改工作时间
  "unavailable_slots": []       # 清除不可用时段
}

Response 200:
{
  "data": {
    "id": 1,
    "name": "妈妈",
    "work_start_time": "10:00",
    ...
  }
}
```

---

### 3.3 任务管理

#### 获取今日任务
```
GET /api/babies/{baby_id}/schedules/today

Response 200:
{
  "data": {
    "date": "2026-03-20",
    "baby": {
      "id": 1,
      "name": "小明",
      "age_months": 9
    },
    "time_slots": [
      {
        "name": "早间",
        "code": "early",
        "time_range": "06:00-09:00",
        "tasks": [
          {
            "id": 1,
            "name": "喂奶",
            "category": "feeding",
            "assigned_to": {
              "id": 1,
              "name": "妈妈",
              "avatar": "/static/parents/1.jpg"
            },
            "status": "completed",
            "completed_at": "2026-03-20T06:30:00Z"
          },
          {
            "id": 2,
            "name": "换尿布",
            "category": "diaper",
            "assigned_to": {
              "id": 2,
              "name": "爸爸"
            },
            "status": "pending"
          }
        ]
      },
      {
        "name": "上午",
        "code": "morning",
        "time_range": "09:00-12:00",
        "tasks": [...]
      }
    ],
    "summary": {
      "total_tasks": 12,
      "completed_tasks": 5,
      "completion_rate": 0.42,
      "fatigue_scores": {
        "1": 0.35,  # 妈妈
        "2": 0.25   # 爸爸
      },
      "balance_score": 0.1,  # 很均衡
      "sleep_hours": {
        "1": 6.5,  # 妈妈
        "2": 7.5   # 爸爸
      }
    }
  }
}
```

#### 手动创建任务
```
POST /api/babies/{baby_id}/tasks

Request:
{
  "name": "去公园晒太阳",
  "category": "outdoor",
  "description": "天气好，带宝宝去公园",
  "duration_minutes": 60,
  "date": "2026-03-20",
  "time_slot": "afternoon",
  "priority": 7
}

Response 201:
{
  "data": {
    "id": 15,
    "name": "去公园晒太阳",
    "category": "outdoor",
    "assigned_to": null,  # 未分配
    "status": "pending"
  }
}
```

#### 分配任务
```
PATCH /api/tasks/{task_id}/assign

Request:
{
  "parent_id": 2
}

Response 200:
{
  "data": {
    "id": 15,
    "assigned_to": {
      "id": 2,
      "name": "爸爸"
    }
  }
}
```

#### 完成任务
```
PATCH /api/tasks/{task_id}/complete

Request:
{
  "completed_by": 1,
  "notes": "宝宝很配合",
  "rating": 5
}

Response 200:
{
  "data": {
    "id": 15,
    "status": "completed",
    "completed_at": "2026-03-20T15:30:00Z",
    "completed_by": {
      "id": 1,
      "name": "妈妈"
    }
  }
}
```

#### 重新分配任务
```
POST /api/babies/{baby_id}/schedules/today/rebalance

Request:
{
  "reason": "爸爸突然加班",  # 可选
  "unavailable_parent_id": 2
}

Response 200:
{
  "data": {
    "message": "已重新分配5个任务",
    "affected_tasks": [3, 4, 8, 9, 10],
    "new_fatigue_scores": {
      "1": 0.55,  # 妈妈疲劳度上升
      "2": 0.25   # 爸爸不变
    },
    "summary": "由于爸爸临时有事，其下午和晚间的任务已转移给妈妈"
  }
}
```

---

### 3.4 智能调度

#### 生成每日日程
```
POST /api/babies/{baby_id}/schedules/generate

Request:
{
  "date": "2026-03-21",
  "auto_assign": true  # 是否自动分配
}

Response 201:
{
  "data": {
    "id": 100,
    "date": "2026-03-21",
    "total_tasks": 15,
    "tasks": [
      {
        "id": 101,
        "name": "早餐奶",
        "template": {
          "source": "知识库",
          "category": "feeding"
        },
        "time_slot": "early",
        "assigned_to": 1,
        "priority": 9
      },
      {
        "id": 102,
        "name": "尝试手指食物",
        "template": {
          "source": "中国营养学会",
          "category": "food"
        },
        "time_slot": "noon",
        "assigned_to": 2,
        "priority": 6
      }
    ],
    "optimization_summary": {
      "balance_score": 0.15,
      "estimated_sleep": {
        "1": 7.0,
        "2": 7.5
      }
    }
  }
}
```

---

### 3.5 数据分析

#### 获取疲劳度趋势
```
GET /api/babies/{baby_id}/analytics/fatigue?days=7

Response 200:
{
  "data": {
    "period": "2026-03-13 to 2026-03-20",
    "parents": [
      {
        "id": 1,
        "name": "妈妈",
        "daily_scores": [
          {"date": "2026-03-13", "score": 0.3},
          {"date": "2026-03-14", "score": 0.45},
          {"date": "2026-03-15", "score": 0.6},
          {"date": "2026-03-16", "score": 0.35},
          {"date": "2026-03-17", "score": 0.4},
          {"date": "2026-03-18", "score": 0.55},
          {"date": "2026-03-19", "score": 0.5},
          {"date": "2026-03-20", "score": 0.35}
        ],
        "average": 0.44,
        "max": 0.6,
        "min": 0.3
      },
      {
        "id": 2,
        "name": "爸爸",
        "daily_scores": [...],
        "average": 0.35,
        "max": 0.5,
        "min": 0.2
      }
    ]
  }
}
```

#### 获取睡眠统计
```
GET /api/babies/{baby_id}/analytics/sleep?days=7

Response 200:
{
  "data": {
    "period": "2026-03-13 to 2026-03-20",
    "baby": {
      "average_nap_hours": 3.2,
      "average_night_hours": 10.5,
      "total_sleep_hours": 13.7
    },
    "parents": [
      {
        "id": 1,
        "name": "妈妈",
        "average_sleep_hours": 6.8,
        "target_sleep_hours": 7.5,
        "deficit_days": 5,
        "trend": "slightly_improving"
      },
      {
        "id": 2,
        "name": "爸爸",
        "average_sleep_hours": 7.2,
        "target_sleep_hours": 7.5,
        "deficit_days": 3,
        "trend": "stable"
      }
    ]
  }
}
```

#### 获取洞察与建议
```
GET /api/babies/{baby_id}/analytics/insights

Response 200:
{
  "data": {
    "overall_wellbeing": "good",  // excellent/good/fair/poor
    "alerts": [
      {
        "level": "warning",
        "message": "妈妈连续3天睡眠不足7小时",
        "recommendation": "建议今晚早点休息，可以将夜间值班交给爸爸",
        "priority": "high"
      },
      {
        "level": "info",
        "message": "本周户外活动仅2次",
        "recommendation": "建议增加户外活动时间，有益宝宝发育",
        "priority": "medium"
      }
    ],
    "achievements": [
      "连续7天按时接种疫苗任务",
      "爸爸本周承担夜间任务50%，很棒！"
    ],
    "suggestions": [
      "周末可以考虑让奶奶帮忙，给夫妻双方放个假",
      "宝宝的辅食可以尝试更多种类的蔬菜"
    ]
  }
}
```

---

## 四、业务逻辑服务

### 4.1 知识库引擎 (knowledge_base.py)

```python
class KnowledgeBaseEngine:
    """根据月龄生成任务模板"""

    def get_tasks_for_age(self, age_months: int) -> List[TaskTemplate]:
        """获取指定月龄的任务模板"""
        pass

    def get_vaccination_tasks(self, age_months: int) -> List[TaskTemplate]:
        """疫苗接种任务"""
        pass

    def get_food_tasks(self, age_months: int) -> List[TaskTemplate]:
        """辅食添加任务"""
        pass

    def get_education_tasks(self, age_months: int) -> List[TaskTemplate]:
        """早教游戏任务"""
        pass

    def get_daily_routines(self, age_months: int) -> List[TaskTemplate]:
        """日常互动任务"""
        pass
```

### 4.2 任务调度器 (scheduler.py)

```python
class TaskScheduler:
    """生成每日任务列表"""

    def generate_daily_schedule(
        self,
        baby: Baby,
        date: date,
        include_recurring: bool = True
    ) -> Schedule:
        """生成指定日期的日程"""
        # 1. 获取该月龄的任务模板
        templates = self.kb.get_tasks_for_age(baby.age_months)

        # 2. 过滤一次性任务（疫苗、体检等）
        onetime_tasks = self._get_onetime_tasks(baby, date)

        # 3. 合并任务
        all_templates = templates + onetime_tasks

        # 4. 创建任务实例
        tasks = [self._create_task(t, baby, date) for t in all_templates]

        # 5. 分配时间段
        self._assign_time_slots(tasks)

        # 6. 创建日程
        schedule = Schedule(baby_id=baby.id, date=date)
        schedule.tasks = tasks

        return schedule
```

### 4.3 优化算法 (optimizer.py)

```python
class TaskOptimizer:
    """任务分配优化"""

    def optimize_assignment(
        self,
        schedule: Schedule,
        parents: List[Parent]
    ) -> Dict[int, int]:
        """
        优化任务分配

        返回: {task_id: parent_id}
        """
        # 构建优化问题
        problem = pulp.LpProblem("TaskAssignment", pulp.LpMinimize)

        # 决策变量：x[i,j] = 1 表示任务i分配给父母j
        x = {}
        for task in schedule.tasks:
            for parent in parents:
                x[(task.id, parent.id)] = pulp.LpVariable(
                    f"x_{task.id}_{parent.id}",
                    cat='Binary'
                )

        # 目标函数：最小化疲劳度不均衡
        fatigue_diff = self._calculate_fatigue_diff(x, schedule, parents)
        problem += fatigue_diff

        # 约束条件
        # 1. 每个任务必须分配给一个人
        for task in schedule.tasks:
            problem += pulp.lpSum(x[(task.id, p.id)] for p in parents) == 1

        # 2. 时间冲突约束（一个人不能同时做两个任务）
        self._add_time_conflict_constraints(problem, x, schedule, parents)

        # 3. 技能约束（某些任务需要特定技能）
        self._add_skill_constraints(problem, x, schedule, parents)

        # 4. 工作时间约束
        self._add_work_time_constraints(problem, x, schedule, parents)

        # 5. 睡眠约束
        self._add_sleep_constraints(problem, x, schedule, parents)

        # 求解
        problem.solve()

        # 返回分配结果
        assignment = {}
        for task in schedule.tasks:
            for parent in parents:
                if pulp.value(x[(task.id, parent.id)]) == 1:
                    assignment[task.id] = parent.id
                    break

        return assignment
```

### 4.4 疲劳度计算 (fatigue_calculator.py)

```python
class FatigueCalculator:
    """疲劳度计算器"""

    def calculate_fatigue(
        self,
        parent: Parent,
        date: date,
        completed_tasks: List[Task],
        sleep_logs: List[SleepLog]
    ) -> float:
        """
        计算疲劳度分数 (0.0 - 1.0+)

        公式：
        疲劳度 = 基础分 + 连续工作惩罚 + 睡眠不足惩罚
        """
        # 1. 基础分：已完成任务 / 预分配任务
        base_score = self._get_base_score(parent, date)

        # 2. 连续工作惩罚
        continuous_penalty = self._get_continuous_penalty(parent, date)

        # 3. 睡眠不足惩罚
        sleep_penalty = self._get_sleep_penalty(parent, date, sleep_logs)

        return base_score + continuous_penalty + sleep_penalty

    def get_balance_score(
        self,
        fatigue_scores: Dict[int, float]
    ) -> float:
        """
        计算负载均衡度

        返回：|fatigue_mom - fatigue_dad|
        """
        scores = list(fatigue_scores.values())
        return abs(scores[0] - scores[1])
```

---

## 五、数据库设计

### 5.1 表结构SQL

```sql
-- 宝宝表
CREATE TABLE babies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    nickname VARCHAR(50),
    birthday DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    avatar VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_baby_birthday ON babies(birthday);

-- 生长记录表
CREATE TABLE growth_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    baby_id INTEGER NOT NULL,
    record_date DATE NOT NULL,
    weight FLOAT,
    height FLOAT,
    head_circumference FLOAT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (baby_id) REFERENCES babies(id) ON DELETE CASCADE
);

-- 父母/照护者表
CREATE TABLE parents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    baby_id INTEGER NOT NULL,
    name VARCHAR(50) NOT NULL,
    relationship VARCHAR(20) NOT NULL,
    avatar VARCHAR(255),
    phone VARCHAR(20),
    work_start_time TIME,
    work_end_time TIME,
    sleep_start_time TIME,
    sleep_end_time TIME,
    unavailable_slots JSON,  -- [{"day": 1, "start": "09:00", "end": "12:00"}]
    capabilities JSON,        -- ["diaper", "feeding", ...]
    target_sleep_hours FLOAT DEFAULT 7.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (baby_id) REFERENCES babies(id) ON DELETE CASCADE
);

-- 任务模板表
CREATE TABLE task_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(20) NOT NULL,
    description TEXT,
    duration_minutes INTEGER NOT NULL,
    min_age_months INTEGER,
    max_age_months INTEGER,
    frequency VARCHAR(20) NOT NULL,
    preferred_time_slots JSON,  -- ["early", "morning", ...]
    required BOOLEAN DEFAULT FALSE,
    priority INTEGER DEFAULT 5,
    source VARCHAR(50),
    source_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 日程表
CREATE TABLE schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    baby_id INTEGER NOT NULL,
    date DATE NOT NULL,
    total_tasks INTEGER DEFAULT 0,
    completed_tasks INTEGER DEFAULT 0,
    completion_rate FLOAT DEFAULT 0.0,
    fatigue_scores JSON,
    balance_score FLOAT DEFAULT 0.0,
    is_special_day BOOLEAN DEFAULT FALSE,
    special_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (baby_id) REFERENCES babies(id) ON DELETE CASCADE,
    UNIQUE(baby_id, date)
);

-- 任务表
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    baby_id INTEGER NOT NULL,
    template_id INTEGER,
    schedule_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(20) NOT NULL,
    description TEXT,
    duration_minutes INTEGER NOT NULL,
    priority INTEGER DEFAULT 5,
    date DATE NOT NULL,
    time_slot VARCHAR(20) NOT NULL,
    assigned_to INTEGER,
    status VARCHAR(20) DEFAULT 'pending',
    completed_at TIMESTAMP,
    completed_by INTEGER,
    completion_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (baby_id) REFERENCES babies(id) ON DELETE CASCADE,
    FOREIGN KEY (template_id) REFERENCES task_templates(id),
    FOREIGN KEY (schedule_id) REFERENCES schedules(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES parents(id),
    FOREIGN KEY (completed_by) REFERENCES parents(id)
);

-- 任务完成记录表
CREATE TABLE task_completions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    parent_id INTEGER NOT NULL,
    completed_at TIMESTAMP NOT NULL,
    notes TEXT,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES parents(id) ON DELETE CASCADE
);

-- 睡眠记录表
CREATE TABLE sleep_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    baby_id INTEGER NOT NULL,
    parent_id INTEGER,
    sleep_type VARCHAR(10) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    duration_minutes INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (baby_id) REFERENCES babies(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES parents(id)
);
```

---

## 六、测试策略

### 6.1 单元测试
- 知识库引擎：验证各月龄任务生成
- 疲劳度计算：验证各种场景的计算结果
- 优化算法：验证任务分配的合理性

### 6.2 集成测试
- API端点测试
- 数据库操作测试
- 业务流程测试

### 6.3 性能测试
- 任务生成性能（< 2秒）
- 优化算法求解性能（< 5秒）
- 并发请求处理
