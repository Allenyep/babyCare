from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.services.knowledge_base import knowledge_base_service
from app.schemas.knowledge import (
    VaccineListResponse,
    FoodListResponse,
    ActivityListResponse,
    MilestoneListResponse,
    KnowledgeBaseResponse
)

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.get("/vaccines", response_model=VaccineListResponse)
def get_vaccines(
    age_months: int = Query(..., ge=0, le=36, description="宝宝月龄"),
    upcoming: bool = Query(False, description="是否获取即将接种的疫苗"),
    db: Session = Depends(get_db)
):
    """
    获取疫苗推荐

    - **age_months**: 宝宝月龄(0-36个月)
    - **upcoming**: true返回未来3个月需要接种的疫苗，false返回当前月龄的疫苗
    """
    try:
        if upcoming:
            vaccines = knowledge_base_service.get_upcoming_vaccines(age_months)
        else:
            vaccines = knowledge_base_service.get_vaccines_by_age(age_months)

        return VaccineListResponse(
            vaccines=vaccines,
            total=len(vaccines)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/foods", response_model=FoodListResponse)
def get_foods(
    age_months: int = Query(..., ge=0, le=36, description="宝宝月龄"),
    db: Session = Depends(get_db)
):
    """
    获取辅食推荐

    - **age_months**: 宝宝月龄(0-36个月)
    - 返回该月龄适合的辅食列表，包括制作方法和注意事项
    """
    try:
        foods = knowledge_base_service.get_foods_by_age(age_months)

        return FoodListResponse(
            foods=foods,
            total=len(foods)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/activities", response_model=ActivityListResponse)
def get_activities(
    age_months: int = Query(..., ge=0, le=36, description="宝宝月龄"),
    category: Optional[str] = Query(None, description="活动类别: motor/cognitive/language/social"),
    db: Session = Depends(get_db)
):
    """
    获取早教活动推荐

    - **age_months**: 宝宝月龄(0-36个月)
    - **category**: 可选，筛选特定类别的活动
    - 返回适合该月龄的早教活动，包括活动说明、所需材料等
    """
    try:
        activities = knowledge_base_service.get_activities_by_age(age_months)

        # 按类别筛选
        if category:
            activities = [a for a in activities if a.category == category]

        return ActivityListResponse(
            activities=activities,
            total=len(activities)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/milestones", response_model=MilestoneListResponse)
def get_milestones(
    age_months: int = Query(..., ge=0, le=36, description="宝宝月龄"),
    category: Optional[str] = Query(None, description="里程碑类别: motor/language/cognitive/social"),
    db: Session = Depends(get_db)
):
    """
    获取发育里程碑

    - **age_months**: 宝宝月龄(0-36个月)
    - **category**: 可选，筛选特定类别的里程碑
    - 返回该月龄相关的发育里程碑和需要注意的信号
    """
    try:
        milestones = knowledge_base_service.get_milestones_by_age(age_months)

        # 按类别筛选
        if category:
            milestones = [m for m in milestones if m.category == category]

        return MilestoneListResponse(
            milestones=milestones,
            total=len(milestones)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/comprehensive", response_model=KnowledgeBaseResponse)
def get_comprehensive_knowledge(
    age_months: int = Query(..., ge=0, le=36, description="宝宝月龄"),
    db: Session = Depends(get_db)
):
    """
    获取综合知识

    - **age_months**: 宝宝月龄(0-36个月)
    - 返回该月龄的完整知识，包括：
        - 即将需要接种的疫苗
        - 适合的辅食推荐
        - 推荐的早教活动
        - 相关的发育里程碑
    """
    try:
        knowledge = knowledge_base_service.get_comprehensive_knowledge(age_months)
        return knowledge
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories")
def get_categories():
    """
    获取知识库分类信息

    返回各类别代码和对应的中文名称
    """
    return {
        "vaccine_importance": {
            "required": "必须接种",
            "recommended": "推荐接种",
            "optional": "可选接种"
        },
        "food_category": {
            "vegetable": "蔬菜",
            "fruit": "水果",
            "meat": "肉蛋奶",
            "grain": "谷物"
        },
        "activity_category": {
            "motor": "大运动/精细动作",
            "cognitive": "认知能力",
            "language": "语言发展",
            "social": "社交情感"
        },
        "milestone_category": {
            "motor": "运动发育",
            "language": "语言发育",
            "cognitive": "认知发育",
            "social": "社交发育"
        }
    }
