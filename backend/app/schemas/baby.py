from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional, List
from enum import Enum


class GenderEnum(str, Enum):
    male = "male"
    female = "female"


class RelationshipEnum(str, Enum):
    mother = "mother"
    father = "father"
    grandparent = "grandparent"
    nanny = "nanny"


# Baby Schemas
class BabyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    nickname: Optional[str] = Field(None, max_length=50)
    birthday: date
    gender: GenderEnum
    avatar: Optional[str] = None


class BabyCreate(BabyBase):
    pass


class BabyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    nickname: Optional[str] = Field(None, max_length=50)
    avatar: Optional[str] = None


class BabyResponse(BabyBase):
    id: int
    age_months: int
    created_at: datetime

    class Config:
        from_attributes = True


class GrowthRecordCreate(BaseModel):
    record_date: date
    weight: Optional[float] = Field(None, gt=0)
    height: Optional[float] = Field(None, gt=0)
    head_circumference: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = None


class GrowthRecordResponse(BaseModel):
    id: int
    baby_id: int
    record_date: date
    weight: Optional[float]
    height: Optional[float]
    head_circumference: Optional[float]
    notes: Optional[str]

    class Config:
        from_attributes = True
