from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


class FatigueRecordCreate(BaseModel):
    """创建疲劳度记录"""
    parent_id: int = Field(..., description="父母ID")
    record_date: date = Field(..., description="记录日期")
    total_tasks: int = Field(0, description="总任务数")
    total_task_duration: int = Field(0, description="总任务时长(分钟)")
    actual_sleep: Optional[float] = Field(None, description="实际睡眠时长(小时)")
    target_sleep: Optional[float] = Field(None, description="目标睡眠时长(小时)")
    work_hours: Optional[float] = Field(0, description="工作时长(小时)")
    notes: Optional[str] = Field(None, description="备注")


class FatigueRecordResponse(BaseModel):
    """疲劳度记录响应"""
    id: int
    parent_id: int
    record_date: date
    fatigue_score: float
    task_load: float
    sleep_deficit: float
    work_hours: float
    total_tasks: int
    total_task_duration: int
    actual_sleep: Optional[float]
    target_sleep: Optional[float]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SleepRecordCreate(BaseModel):
    """创建睡眠记录"""
    parent_id: int = Field(..., description="父母ID")
    record_date: date = Field(..., description="记录日期")
    sleep_start: datetime = Field(..., description="入睡时间")
    sleep_end: datetime = Field(..., description="醒来时间")
    quality: Optional[str] = Field(None, description="睡眠质量: good/fair/poor")
    interruptions: int = Field(0, ge=0, description="夜醒次数")
    notes: Optional[str] = Field(None, description="备注")


class SleepRecordResponse(BaseModel):
    """睡眠记录响应"""
    id: int
    parent_id: int
    record_date: date
    sleep_start: datetime
    sleep_end: datetime
    duration_hours: float
    quality: Optional[str]
    interruptions: int
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class FatigueTrend(BaseModel):
    """疲劳度趋势"""
    parent_id: int
    parent_name: str
    trend: List[FatigueRecordResponse]
    average_fatigue: float
    min_fatigue: float
    max_fatigue: float
    trend_direction: str  # improving/stable/worsening


class FatigueComparison(BaseModel):
    """疲劳度对比"""
    date: date
    parents: List[dict]
    balance_score: float
    gap: float


class FatigueAnalysis(BaseModel):
    """疲劳度分析"""
    current_fatigue: FatigueRecordResponse
    historical_average: float
    percentile: float  # 在历史记录中的百分位
    risk_level: str  # low/medium/high
    recommendations: List[str]
