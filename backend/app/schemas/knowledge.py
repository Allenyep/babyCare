from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class VaccineSchedule(BaseModel):
    """疫苗计划"""
    id: int
    vaccine_name: str = Field(..., description="疫苗名称")
    age_months: int = Field(..., description="接种月龄")
    description: Optional[str] = Field(None, description="疫苗说明")
    importance: str = Field(..., description="重要性: required/recommended/optional")
    side_effects: Optional[str] = Field(None, description="可能的副作用")
    notes: Optional[str] = Field(None, description="注意事项")


class FoodRecommendation(BaseModel):
    """辅食推荐"""
    id: int
    food_name: str = Field(..., description="食物名称")
    category: str = Field(..., description="食物类别: vegetable/fruit/meat/grain")
    age_months_from: int = Field(..., description="适用月龄起")
    age_months_to: int = Field(..., description="适用月龄止")
    nutrition: str = Field(..., description="营养价值")
    preparation: Optional[str] = Field(None, description="制作方法")
    precautions: Optional[str] = Field(None, description="注意事项")
    allergy_risk: bool = Field(False, description="过敏风险")


class EducationActivity(BaseModel):
    """早教活动"""
    id: int
    activity_name: str = Field(..., description="活动名称")
    category: str = Field(..., description="类别: motor/cognitive/language/social")
    age_months_from: int = Field(..., description="适用月龄起")
    age_months_to: int = Field(..., description="适用月龄止")
    description: str = Field(..., description="活动描述")
    duration_minutes: int = Field(..., description="建议时长(分钟)")
    benefits: str = Field(..., description="发育益处")
    materials: Optional[str] = Field(None, description="所需材料")
    instructions: Optional[str] = Field(None, description="具体步骤")


class DevelopmentMilestone(BaseModel):
    """发育里程碑"""
    id: int
    age_months: int = Field(..., description="月龄")
    category: str = Field(..., description="类别: motor/language/cognitive/social")
    milestone: str = Field(..., description="里程碑描述")
    typical_range: str = Field(..., description="典型出现时间范围")
    concern_signs: Optional[str] = Field(None, description="需要注意的信号")


class KnowledgeBaseResponse(BaseModel):
    """知识库综合响应"""
    baby_age_months: int
    vaccines: List[VaccineSchedule]
    foods: List[FoodRecommendation]
    activities: List[EducationActivity]
    milestones: List[DevelopmentMilestone]


class VaccineListResponse(BaseModel):
    """疫苗列表响应"""
    vaccines: List[VaccineSchedule]
    total: int


class FoodListResponse(BaseModel):
    """辅食列表响应"""
    foods: List[FoodRecommendation]
    total: int


class ActivityListResponse(BaseModel):
    """活动列表响应"""
    activities: List[EducationActivity]
    total: int


class MilestoneListResponse(BaseModel):
    """里程碑列表响应"""
    milestones: List[DevelopmentMilestone]
    total: int


class CustomKnowledge(BaseModel):
    """自定义知识"""
    id: int
    user_id: int
    category: str = Field(..., description="类别")
    title: str = Field(..., description="标题")
    content: str = Field(..., description="内容")
    applicable_age_months: Optional[int] = Field(None, description="适用月龄")
    tags: Optional[List[str]] = Field(None, description="标签")
    created_at: date


class CustomKnowledgeCreate(BaseModel):
    """创建自定义知识"""
    category: str = Field(..., description="类别")
    title: str = Field(..., min_length=1, max_length=200, description="标题")
    content: str = Field(..., min_length=1, description="内容")
    applicable_age_months: Optional[int] = Field(None, ge=0, le=36, description="适用月龄")
    tags: Optional[List[str]] = Field(None, description="标签")
