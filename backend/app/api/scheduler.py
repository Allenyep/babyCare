from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.db.database import get_db
from app.services.scheduler import scheduler_service
from app.schemas.scheduler import (
    DailySchedule,
    SchedulePreview,
    GenerateScheduleRequest,
    ScheduleAdjustment,
    ScheduleStatistics,
    RecurringTaskConfig
)

router = APIRouter(prefix="/scheduler", tags=["scheduler"])


@router.post("/generate", response_model=DailySchedule)
def generate_schedule(
    request: GenerateScheduleRequest,
    db: Session = Depends(get_db)
):
    """
    生成每日日程

    根据宝宝月龄自动生成包含以下内容的日程：
    - 重复任务（喂奶、换尿布、睡眠等）
    - 知识库任务（早教活动）
    - 自定义任务

    任务分配考虑因素：
    - 父母工作时间
    - 负载均衡
    - 时间段合理性
    """
    try:
        # TODO: 从数据库获取宝宝信息
        baby_name = "宝宝"  # 临时硬编码
        baby_age_months = 6  # 临时硬编码

        # TODO: 从数据库获取父母信息
        parent_availability = {
            1: {"name": "妈妈", "work_hours": "09:00-18:00"},
            2: {"name": "爸爸", "work_hours": "10:00-19:00"}
        }

        schedule = scheduler_service.generate_daily_schedule(
            baby_id=request.baby_id,
            baby_name=baby_name,
            baby_age_months=baby_age_months,
            target_date=request.date,
            preferences=request.preferences,
            include_knowledge_tasks=request.include_knowledge_tasks,
            include_recurring_tasks=request.include_recurring_tasks,
            custom_tasks=request.custom_tasks,
            parent_availability=parent_availability
        )

        return schedule

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/preview", response_model=SchedulePreview)
def preview_schedule(
    request: GenerateScheduleRequest,
    db: Session = Depends(get_db)
):
    """
    预览日程（不保存）

    生成日程预览并提供优化建议和警告
    """
    try:
        # 先生成日程
        schedule_result = generate_schedule(request, db)

        # 预览
        preview = scheduler_service.preview_schedule(
            schedule_result,
            request.preferences
        )

        return preview

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/adjust", response_model=DailySchedule)
def adjust_schedule(
    baby_id: int = Query(..., description="宝宝ID"),
    target_date: date = Query(..., description="目标日期"),
    adjustments: List[ScheduleAdjustment] = [],
    db: Session = Depends(get_db)
):
    """
    调整日程

    允许修改任务的：
    - 时间段
    - 分配对象
    - 删除任务

    注意：这是简化版本，实际应从数据库加载现有日程
    """
    try:
        # TODO: 从数据库加载现有日程
        # 这里临时生成一个新日程作为示例
        baby_name = "宝宝"
        baby_age_months = 6

        schedule = scheduler_service.generate_daily_schedule(
            baby_id=baby_id,
            baby_name=baby_name,
            baby_age_months=baby_age_months,
            target_date=target_date
        )

        # 应用调整
        adjusted_schedule = scheduler_service.adjust_schedule(schedule, adjustments)

        return adjusted_schedule

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics", response_model=ScheduleStatistics)
def get_schedule_statistics(
    baby_id: int = Query(..., description="宝宝ID"),
    target_date: date = Query(..., description="目标日期"),
    db: Session = Depends(get_db)
):
    """
    获取日程统计信息

    返回日程的详细统计：
    - 各时间段任务分布
    - 各类别任务数量
    - 父母任务分配
    - 总时长和平均优先级
    """
    try:
        # TODO: 从数据库加载日程
        # 这里临时生成一个新日程作为示例
        baby_name = "宝宝"
        baby_age_months = 6

        schedule = scheduler_service.generate_daily_schedule(
            baby_id=baby_id,
            baby_name=baby_name,
            baby_age_months=baby_age_months,
            target_date=target_date
        )

        stats = scheduler_service.get_schedule_statistics(schedule)
        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recurring-tasks")
def get_recurring_tasks():
    """
    获取当前重复任务配置

    返回所有已配置的重复任务
    """
    return {
        "recurring_tasks": scheduler_service.recurring_tasks
    }


@router.put("/recurring-tasks")
def update_recurring_tasks(
    tasks: List[RecurringTaskConfig]
):
    """
    更新重复任务配置

    允许自定义重复任务的设置
    """
    try:
        scheduler_service.set_recurring_tasks(tasks)
        return {
            "message": "重复任务配置已更新",
            "count": len(tasks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/time-slots")
def get_time_slots():
    """
    获取时间段定义

    返回所有可用的时间段及其说明
    """
    from app.services.scheduler import TimeSlot

    return {
        "time_slots": [
            {
                "code": slot.value,
                "name": data["name"],
                "hours": data["hours"],
                "order": data["order"]
            }
            for slot, data in scheduler_service.TIME_SLOTS.items()
        ]
    }


@router.post("/optimize")
def optimize_schedule(
    baby_id: int = Query(..., description="宝宝ID"),
    target_date: date = Query(..., description="目标日期"),
    optimize_for: str = Query("balance", description="优化目标: balance/sleep"),
    db: Session = Depends(get_db)
):
    """
    优化日程

    根据指定目标优化任务分配：
    - balance: 负载均衡（最小化父母负担差异）
    - sleep: 睡眠优先（保证双方睡眠时间）

    TODO: 实现优化算法（当前返回建议）
    """
    try:
        # TODO: 实现真正的优化算法
        # 当前返回简单的建议

        suggestions = []

        if optimize_for == "balance":
            suggestions = [
                "调整3个任务从妈妈到爸爸以平衡负担",
                "考虑将上午的部分任务移到下午"
            ]
        elif optimize_for == "sleep":
            suggestions = [
                "将夜间任务全部分配给一方，另一方保证睡眠",
                "减少晚间任务数量，提前到下午完成"
            ]
        else:
            suggestions = ["未知的优化目标"]

        return {
            "optimize_for": optimize_for,
            "suggestions": suggestions,
            "message": "优化功能开发中，当前仅返回建议"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
