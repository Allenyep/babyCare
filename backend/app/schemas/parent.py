from pydantic import BaseModel, Field, validator
from typing import Optional, List
from app.schemas.baby import RelationshipEnum


class ParentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    relationship: RelationshipEnum
    phone: Optional[str] = Field(None, pattern=r"^\d{11}$")
    avatar: Optional[str] = None
    work_start_time: Optional[str] = Field(None, pattern=r"^([0-1]\d|2[0-3]):([0-5]\d)$")
    work_end_time: Optional[str] = Field(None, pattern=r"^([0-1]\d|2[0-3]):([0-5]\d)$")
    sleep_start_time: Optional[str] = Field(None, pattern=r"^([0-1]\d|2[0-3]):([0-5]\d)$")
    sleep_end_time: Optional[str] = Field(None, pattern=r"^([0-1]\d|2[0-3]):([0-5]\d)$")
    target_sleep_hours: float = Field(default=7.0, gt=0, le=12)
    capabilities: Optional[List[str]] = None
    unavailable_slots: Optional[List[dict]] = None


class ParentCreate(ParentBase):
    pass


class ParentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    avatar: Optional[str] = None
    work_start_time: Optional[str] = None
    work_end_time: Optional[str] = None
    target_sleep_hours: Optional[float] = Field(None, gt=0, le=12)


class ParentResponse(ParentBase):
    id: int
    baby_id: int
    fatigue_score: float = 0.0
    today_completed: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
