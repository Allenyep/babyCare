from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from enum import Enum


class TimeSlotEnum(str, Enum):
    early = "early"
    morning = "morning"
    noon = "noon"
    afternoon = "afternoon"
    evening = "evening"
    night = "night"


class TaskCategoryEnum(str, Enum):
    feeding = "feeding"
    diaper = "diaper"
    education = "education"
    food = "food"
    outdoor = "outdoor"
    hygiene = "hygiene"
    medical = "medical"


class TaskStatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    skipped = "skipped"
    cancelled = "cancelled"


class TaskBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: TaskCategoryEnum
    description: Optional[str] = None
    duration_minutes: int = Field(..., gt=0, le=480)
    priority: int = Field(default=5, ge=1, le=10)
    date: date
    time_slot: TimeSlotEnum
    assigned_to: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    assigned_to: Optional[int] = None
    status: Optional[TaskStatusEnum] = None


class TaskCompletion(BaseModel):
    completed_by: int
    notes: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)


class TaskResponse(TaskBase):
    id: int
    baby_id: int
    template_id: Optional[int]
    schedule_id: int
    status: TaskStatusEnum
    completed_at: Optional[datetime]
    completed_by: Optional[int]
    completion_notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
