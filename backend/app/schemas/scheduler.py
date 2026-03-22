from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import date as date_type, time, datetime
from enum import Enum


class TimeSlot(str, Enum):
    """时间段"""
    EARLY = "early"      # 06:00-09:00
    MORNING = "morning"   # 09:00-12:00
    NOON = "noon"         # 12:00-15:00
    AFTERNOON = "afternoon"  # 15:00-18:00
    EVENING = "evening"   # 18:00-21:00
    NIGHT = "night"       # 21:00-06:00


class TaskPriority(str, Enum):
    """任务优先级"""
    HIGH = "high"         # 8-10
    MEDIUM = "medium"     # 5-7
    LOW = "low"           # 1-4


class SchedulerPreference(BaseModel):
    """调度偏好设置"""
    start_time: time = Field(default=time(6, 0), description="一天开始时间")
    end_time: time = Field(default=time(22, 0), description="一天结束时间")
    nap_time: Optional[str] = Field(None, description="午睡时间，如'12:00-14:00'")
    optimize_for: str = Field(default="balance", description="优化目标: balance/sleep")
    strict_mode: bool = Field(default=False, description="严格模式")
    custom_time_slots: Optional[Dict[str, str]] = Field(None, description="自定义时间段")


class ScheduledTask(BaseModel):
    """已安排的任务"""
    id: Optional[int] = None
    name: str = Field(..., description="任务名称")
    category: str = Field(..., description="任务类别")
    description: Optional[str] = Field(None, description="任务描述")
    duration_minutes: int = Field(..., description="预计时长(分钟)")
    priority: int = Field(..., ge=1, le=10, description="优先级(1-10)")
    time_slot: TimeSlot = Field(..., description="时间段")
    assigned_to: int = Field(..., description="分配给(parent ID)")
    assigned_to_name: str = Field(..., description="分配给(姓名)")
    is_recurring: bool = Field(default=False, description="是否重复任务")
    task_source: str = Field(..., description="任务来源: knowledge/custom/recurring")


class DailySchedule(BaseModel):
    """每日日程"""
    schedule_date: date_type = Field(..., alias="date", description="日期")
    baby_id: int = Field(..., description="宝宝ID")
    baby_name: str = Field(..., description="宝宝名称")
    baby_age_months: int = Field(..., description="宝宝月龄")
    tasks: List[ScheduledTask] = Field(default_factory=list, description="任务列表")
    total_tasks: int = Field(default=0, description="总任务数")
    estimated_total_duration: int = Field(default=0, description="预计总时长(分钟)")
    parent_distribution: Dict[str, int] = Field(default_factory=dict, description="父母任务分配")


class SchedulePreview(BaseModel):
    """日程预览"""
    schedule: DailySchedule
    warnings: List[str] = Field(default_factory=list, description="警告信息")
    suggestions: List[str] = Field(default_factory=list, description="优化建议")


class ScheduleAdjustment(BaseModel):
    """日程调整"""
    task_id: int = Field(..., description="任务ID")
    new_time_slot: Optional[TimeSlot] = Field(None, description="新时间段")
    new_assignee: Optional[int] = Field(None, description="新分配给")
    remove: bool = Field(default=False, description="是否移除任务")


class GenerateScheduleRequest(BaseModel):
    """生成日程请求"""
    baby_id: int = Field(..., description="宝宝ID")
    target_date: date_type = Field(..., alias="date", description="目标日期")
    preferences: Optional[SchedulerPreference] = Field(None, description="调度偏好")
    include_knowledge_tasks: bool = Field(default=True, description="是否包含知识库任务")
    include_recurring_tasks: bool = Field(default=True, description="是否包含重复任务")
    custom_tasks: List[ScheduledTask] = Field(default_factory=list, description="自定义任务")


class RecurringTaskConfig(BaseModel):
    """重复任务配置"""
    id: Optional[int] = None
    name: str = Field(..., description="任务名称")
    category: str = Field(..., description="任务类别")
    time_slot: TimeSlot = Field(..., description="时间段")
    duration_minutes: int = Field(..., description="时长")
    priority: int = Field(..., ge=1, le=10, description="优先级")
    frequency: str = Field(..., description="频率: daily/weekly")
    assigned_to: int = Field(..., description="默认分配给")
    enabled: bool = Field(default=True, description="是否启用")


class ScheduleStatistics(BaseModel):
    """日程统计"""
    total_tasks: int = Field(..., description="总任务数")
    tasks_by_slot: Dict[str, int] = Field(..., description="各时间段任务数")
    tasks_by_category: Dict[str, int] = Field(..., description="各类别任务数")
    tasks_by_parent: Dict[str, int] = Field(..., description="各父母任务数")
    total_duration: int = Field(..., description="总时长(分钟)")
    average_priority: float = Field(..., description="平均优先级")
