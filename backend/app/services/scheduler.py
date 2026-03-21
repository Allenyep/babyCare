from typing import List, Dict, Optional
from datetime import date, time, datetime
import random

from app.schemas.scheduler import (
    TimeSlot,
    ScheduledTask,
    DailySchedule,
    SchedulePreview,
    SchedulerPreference,
    GenerateScheduleRequest,
    RecurringTaskConfig,
    ScheduleStatistics
)
from app.services.knowledge_base import knowledge_base_service
from app.schemas.knowledge import EducationActivity


class SchedulerService:
    """任务调度服务 - 生成每日任务计划"""

    # 标准时间段定义
    TIME_SLOTS = {
        TimeSlot.EARLY: {"name": "早间", "hours": "06:00-09:00", "order": 1},
        TimeSlot.MORNING: {"name": "上午", "hours": "09:00-12:00", "order": 2},
        TimeSlot.NOON: {"name": "中午", "hours": "12:00-15:00", "order": 3},
        TimeSlot.AFTERNOON: {"name": "下午", "hours": "15:00-18:00", "order": 4},
        TimeSlot.EVENING: {"name": "晚上", "hours": "18:00-21:00", "order": 5},
        TimeSlot.NIGHT: {"name": "夜间", "hours": "21:00-06:00", "order": 6}
    }

    # 重复任务配置 (默认)
    DEFAULT_RECURRING_TASKS = [
        {
            "name": "晨间喂奶",
            "category": "feeding",
            "time_slot": TimeSlot.EARLY,
            "duration_minutes": 20,
            "priority": 9,
            "frequency": "daily",
            "assigned_to": 1  # 默认分配给妈妈
        },
        {
            "name": "晨间换尿布",
            "category": "diaper",
            "time_slot": TimeSlot.EARLY,
            "duration_minutes": 5,
            "priority": 9,
            "frequency": "daily",
            "assigned_to": 2  # 默认分配给爸爸
        },
        {
            "name": "上午喂奶",
            "category": "feeding",
            "time_slot": TimeSlot.MORNING,
            "duration_minutes": 20,
            "priority": 8,
            "frequency": "daily",
            "assigned_to": 1
        },
        {
            "name": "上午换尿布",
            "category": "diaper",
            "time_slot": TimeSlot.MORNING,
            "duration_minutes": 5,
            "priority": 8,
            "frequency": "daily",
            "assigned_to": 2
        },
        {
            "name": "午睡",
            "category": "hygiene",
            "time_slot": TimeSlot.NOON,
            "duration_minutes": 120,
            "priority": 8,
            "frequency": "daily",
            "assigned_to": 1
        },
        {
            "name": "下午喂奶",
            "category": "feeding",
            "time_slot": TimeSlot.AFTERNOON,
            "duration_minutes": 20,
            "priority": 8,
            "frequency": "daily",
            "assigned_to": 1
        },
        {
            "name": "下午换尿布",
            "category": "diaper",
            "time_slot": TimeSlot.AFTERNOON,
            "duration_minutes": 5,
            "priority": 7,
            "frequency": "daily",
            "assigned_to": 2
        },
        {
            "name": "傍晚喂奶",
            "category": "feeding",
            "time_slot": TimeSlot.EVENING,
            "duration_minutes": 20,
            "priority": 8,
            "frequency": "daily",
            "assigned_to": 1
        },
        {
            "name": "辅食喂养",
            "category": "food",
            "time_slot": TimeSlot.EVENING,
            "duration_minutes": 30,
            "priority": 8,
            "frequency": "daily",
            "assigned_to": 1
        },
        {
            "name": "晚间洗浴",
            "category": "hygiene",
            "time_slot": TimeSlot.EVENING,
            "duration_minutes": 30,
            "priority": 7,
            "frequency": "daily",
            "assigned_to": 2
        },
        {
            "name": "睡前喂奶",
            "category": "feeding",
            "time_slot": TimeSlot.NIGHT,
            "duration_minutes": 20,
            "priority": 9,
            "frequency": "daily",
            "assigned_to": 1
        },
        {
            "name": "夜间换尿布",
            "category": "diaper",
            "time_slot": TimeSlot.NIGHT,
            "duration_minutes": 5,
            "priority": 6,
            "frequency": "daily",
            "assigned_to": 2
        }
    ]

    def __init__(self):
        """初始化调度器"""
        self.recurring_tasks = self.DEFAULT_RECURRING_TASKS.copy()

    def generate_daily_schedule(
        self,
        baby_id: int,
        baby_name: str,
        baby_age_months: int,
        target_date: date,
        preferences: Optional[SchedulerPreference] = None,
        include_knowledge_tasks: bool = True,
        include_recurring_tasks: bool = True,
        custom_tasks: List[ScheduledTask] = None,
        parent_availability: Dict[int, Dict[str, str]] = None
    ) -> DailySchedule:
        """
        生成每日日程

        Args:
            baby_id: 宝宝ID
            baby_name: 宝宝名称
            baby_age_months: 宝宝月龄
            target_date: 目标日期
            preferences: 调度偏好
            include_knowledge_tasks: 是否包含知识库任务
            include_recurring_tasks: 是否包含重复任务
            custom_tasks: 自定义任务
            parent_availability: 父母可用性 {parent_id: {"work_hours": "09:00-18:00"}}
        """
        tasks: List[ScheduledTask] = []
        parent_availability = parent_availability or {
            1: {"name": "妈妈", "work_hours": "09:00-18:00"},
            2: {"name": "爸爸", "work_hours": "10:00-19:00"}
        }

        # 1. 添加重复任务
        if include_recurring_tasks:
            recurring = self._generate_recurring_tasks(parent_availability)
            tasks.extend(recurring)

        # 2. 添加知识库任务 (早教活动)
        if include_knowledge_tasks and baby_age_months >= 3:  # 3个月以上开始早教
            knowledge_tasks = self._generate_knowledge_tasks(
                baby_age_months,
                parent_availability,
                preferences
            )
            tasks.extend(knowledge_tasks)

        # 3. 添加自定义任务
        if custom_tasks:
            tasks.extend(custom_tasks)

        # 4. 按优先级和时间段排序
        tasks = self._sort_tasks(tasks)

        # 5. 计算统计信息
        total_duration = sum(t.duration_minutes for t in tasks)
        parent_distribution = self._calculate_parent_distribution(tasks)

        return DailySchedule(
            date=target_date,
            baby_id=baby_id,
            baby_name=baby_name,
            baby_age_months=baby_age_months,
            tasks=tasks,
            total_tasks=len(tasks),
            estimated_total_duration=total_duration,
            parent_distribution=parent_distribution
        )

    def _generate_recurring_tasks(
        self,
        parent_availability: Dict[int, Dict[str, str]]
    ) -> List[ScheduledTask]:
        """生成重复任务"""
        tasks = []

        for task_config in self.recurring_tasks:
            # 根据工作时间和负载均衡选择分配对象
            assigned_to = self._assign_task_to_parent(
                task_config["time_slot"],
                task_config["assigned_to"],
                parent_availability,
                [t["assigned_to"] for t in tasks]  # 已分配的任务
            )

            task = ScheduledTask(
                name=task_config["name"],
                category=task_config["category"],
                description="",
                duration_minutes=task_config["duration_minutes"],
                priority=task_config["priority"],
                time_slot=task_config["time_slot"],
                assigned_to=assigned_to,
                assigned_to_name=parent_availability[assigned_to]["name"],
                is_recurring=True,
                task_source="recurring"
            )
            tasks.append(task)

        return tasks

    def _generate_knowledge_tasks(
        self,
        baby_age_months: int,
        parent_availability: Dict[int, Dict[str, str]],
        preferences: Optional[SchedulerPreference]
    ) -> List[ScheduledTask]:
        """从知识库生成任务"""
        tasks = []
        activities = knowledge_base_service.get_activities_by_age(baby_age_months)

        # 选择1-2个适合的活动添加到日程
        selected_activities = self._select_activities_for_schedule(activities, 2)

        for activity in selected_activities:
            # 根据活动类别选择合适的时间段
            time_slot = self._select_time_slot_for_activity(activity.category, preferences)

            # 分配给父母（考虑时间和其他任务）
            assigned_to = self._assign_task_to_parent(
                time_slot,
                1,  # 默认妈妈
                parent_availability,
                []  # 暂时不考虑已有任务
            )

            task = ScheduledTask(
                name=activity.activity_name,
                category=activity.category,
                description=activity.description,
                duration_minutes=activity.duration_minutes,
                priority=5,  # 早教活动中等优先级
                time_slot=time_slot,
                assigned_to=assigned_to,
                assigned_to_name=parent_availability[assigned_to]["name"],
                is_recurring=False,
                task_source="knowledge"
            )
            tasks.append(task)

        return tasks

    def _select_activities_for_schedule(
        self,
        activities: List[EducationActivity],
        count: int
    ) -> List[EducationActivity]:
        """选择适合的活动添加到日程"""
        if len(activities) <= count:
            return activities

        # 优先选择不同类别的活动
        selected = []
        categories = set()

        # 先按类别筛选
        for activity in activities:
            if activity.category not in categories:
                selected.append(activity)
                categories.add(activity.category)
                if len(selected) >= count:
                    break

        # 如果还不够，随机添加
        if len(selected) < count:
            remaining = [a for a in activities if a not in selected]
            selected.extend(random.sample(remaining, min(count - len(selected), len(remaining))))

        return selected

    def _select_time_slot_for_activity(
        self,
        category: str,
        preferences: Optional[SchedulerPreference]
    ) -> TimeSlot:
        """根据活动类别选择合适的时间段"""
        # 早教活动适合的时间段
        activity_time_slots = {
            "motor": [TimeSlot.MORNING, TimeSlot.AFTERNOON],
            "cognitive": [TimeSlot.MORNING, TimeSlot.EVENING],
            "language": [TimeSlot.MORNING, TimeSlot.AFTERNOON, TimeSlot.EVENING],
            "social": [TimeSlot.AFTERNOON, TimeSlot.EVENING]
        }

        preferred_slots = activity_time_slots.get(category, [TimeSlot.MORNING, TimeSlot.AFTERNOON])
        return random.choice(preferred_slots)

    def _assign_task_to_parent(
        self,
        time_slot: TimeSlot,
        default_parent: int,
        parent_availability: Dict[int, Dict[str, str]],
        existing_assignments: List[int]
    ) -> int:
        """
        将任务分配给父母

        考虑因素：
        1. 工作时间（工作时间内的任务优先分配给非工作方）
        2. 负载均衡（尽量让双方任务数量接近）
        """
        # 简单策略：工作时间内，优先分配给非工作方
        work_hours_map = {
            1: parent_availability[1].get("work_hours", ""),
            2: parent_availability[2].get("work_hours", "")
        }

        # 判断时间段是否在工作时间内
        slot_hours = self.TIME_SLOTS[time_slot]["hours"]
        slot_start = int(slot_hours.split(":")[0])

        parent_working = {}
        for parent_id, work_hours in work_hours_map.items():
            if work_hours:
                work_start = int(work_hours.split(":")[0])
                work_end = int(work_hours.split("-")[1].split(":")[0])
                parent_working[parent_id] = work_start <= slot_start < work_end
            else:
                parent_working[parent_id] = False

        # 统计已分配的任务
        assignment_count = {
            1: sum(1 for a in existing_assignments if a == 1),
            2: sum(1 for a in existing_assignments if a == 2)
        }

        # 分配逻辑
        if parent_working[1] and not parent_working[2]:
            # 妈妈工作，爸爸不工作 -> 分配给爸爸
            return 2
        elif parent_working[2] and not parent_working[1]:
            # 爸爸工作，妈妈不工作 -> 分配给妈妈
            return 1
        else:
            # 都工作或都不工作 -> 负载均衡
            if assignment_count[1] <= assignment_count[2]:
                return 1
            else:
                return 2

    def _sort_tasks(self, tasks: List[ScheduledTask]) -> List[ScheduledTask]:
        """排序任务：先按时间段，再按优先级"""
        time_slot_order = {slot: data["order"] for slot, data in self.TIME_SLOTS.items()}

        return sorted(
            tasks,
            key=lambda t: (time_slot_order[t.time_slot], -t.priority)
        )

    def _calculate_parent_distribution(self, tasks: List[ScheduledTask]) -> Dict[str, int]:
        """计算父母任务分配统计"""
        distribution = {}
        for task in tasks:
            name = task.assigned_to_name
            distribution[name] = distribution.get(name, 0) + 1
        return distribution

    def preview_schedule(
        self,
        schedule: DailySchedule,
        preferences: Optional[SchedulerPreference] = None
    ) -> SchedulePreview:
        """预览日程并提供优化建议"""
        warnings = []
        suggestions = []

        # 检查负载均衡
        parent_counts = list(schedule.parent_distribution.values())
        if len(parent_counts) == 2 and abs(parent_counts[0] - parent_counts[1]) > 3:
            warnings.append(f"负载不均衡：{schedule.parent_distribution}")
            suggestions.append("建议调整部分任务分配以平衡父母负担")

        # 检查总时长
        if schedule.estimated_total_duration > 480:  # 8小时
            warnings.append(f"总时长过长：{schedule.estimated_total_duration}分钟")
            suggestions.append("建议移除或合并部分低优先级任务")

        # 检查时间段分布
        slot_counts = {}
        for task in schedule.tasks:
            slot_counts[task.time_slot] = slot_counts.get(task.time_slot, 0) + 1

        max_slot = max(slot_counts, key=slot_counts.get)
        min_slot = min(slot_counts, key=slot_counts.get)
        if slot_counts[max_slot] - slot_counts[min_slot] > 4:
            suggestions.append(f"建议调整任务分布，{max_slot}时段任务过多")

        # 检查午睡时间
        if preferences and preferences.nap_time:
            nap_tasks = [t for t in schedule.tasks if t.time_slot == TimeSlot.NOON]
            if len(nap_tasks) > 2:
                suggestions.append("午睡时间段任务较多，可能影响休息")

        return SchedulePreview(
            schedule=schedule,
            warnings=warnings,
            suggestions=suggestions
        )

    def adjust_schedule(
        self,
        schedule: DailySchedule,
        adjustments: List  # ScheduleAdjustment objects
    ) -> DailySchedule:
        """调整日程"""
        # 创建任务副本
        updated_tasks = schedule.tasks.copy()

        for adjustment in adjustments:
            # 这里简化处理，实际应该根据task_id查找
            # 由于任务可能还没有ID，使用名称匹配
            if hasattr(adjustment, 'remove') and adjustment.remove:
                updated_tasks = [t for t in updated_tasks if t.name != adjustment.task_id]
            else:
                for task in updated_tasks:
                    if task.name == adjustment.task_id or task.id == adjustment.task_id:
                        if adjustment.new_time_slot:
                            task.time_slot = adjustment.new_time_slot
                        if adjustment.new_assignee:
                            task.assigned_to = adjustment.new_assignee
                        break

        # 重新排序
        updated_tasks = self._sort_tasks(updated_tasks)

        # 更新统计
        return DailySchedule(
            date=schedule.date,
            baby_id=schedule.baby_id,
            baby_name=schedule.baby_name,
            baby_age_months=schedule.baby_age_months,
            tasks=updated_tasks,
            total_tasks=len(updated_tasks),
            estimated_total_duration=sum(t.duration_minutes for t in updated_tasks),
            parent_distribution=self._calculate_parent_distribution(updated_tasks)
        )

    def get_schedule_statistics(self, schedule: DailySchedule) -> ScheduleStatistics:
        """获取日程统计信息"""
        tasks_by_slot = {}
        tasks_by_category = {}
        tasks_by_parent = {}

        for task in schedule.tasks:
            # 按时间段统计
            slot = task.time_slot.value
            tasks_by_slot[slot] = tasks_by_slot.get(slot, 0) + 1

            # 按类别统计
            tasks_by_category[task.category] = tasks_by_category.get(task.category, 0) + 1

            # 按父母统计
            tasks_by_parent[task.assigned_to_name] = tasks_by_parent.get(task.assigned_to_name, 0) + 1

        avg_priority = sum(t.priority for t in schedule.tasks) / len(schedule.tasks) if schedule.tasks else 0

        return ScheduleStatistics(
            total_tasks=schedule.total_tasks,
            tasks_by_slot=tasks_by_slot,
            tasks_by_category=tasks_by_category,
            tasks_by_parent=tasks_by_parent,
            total_duration=schedule.estimated_total_duration,
            average_priority=round(avg_priority, 2)
        )

    def set_recurring_tasks(self, tasks: List[RecurringTaskConfig]):
        """设置重复任务配置"""
        self.recurring_tasks = [
            {
                "name": t.name,
                "category": t.category,
                "time_slot": t.time_slot,
                "duration_minutes": t.duration_minutes,
                "priority": t.priority,
                "frequency": t.frequency,
                "assigned_to": t.assigned_to
            }
            for t in tasks if t.enabled
        ]


# 全局实例
scheduler_service = SchedulerService()
