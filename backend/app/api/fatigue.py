from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.db.database import get_db
from app.services.fatigue_calculator import fatigue_calculator
from app.schemas.fatigue import (
    FatigueRecordCreate,
    FatigueRecordResponse,
    SleepRecordCreate,
    SleepRecordResponse,
    FatigueTrend,
    FatigueAnalysis
)
from app.models.fatigue import FatigueRecord, SleepRecord

router = APIRouter(prefix="/fatigue", tags=["fatigue"])


@router.post("/calculate", response_model=FatigueRecordResponse)
def calculate_fatigue(
    record: FatigueRecordCreate,
    db: Session = Depends(get_db)
):
    """
    计算并保存疲劳度记录

    根据任务负载、睡眠时长、工作时间计算疲劳度评分 (0.0-1.0)
    """
    try:
        fatigue_record = fatigue_calculator.save_fatigue_record(db, record)
        return fatigue_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/record/{parent_id}", response_model=FatigueRecordResponse)
def get_fatigue_record(
    parent_id: int,
    record_date: date = Query(..., description="记录日期"),
    db: Session = Depends(get_db)
):
    """获取指定日期的疲劳度记录"""
    record = db.query(FatigueRecord).filter(
        FatigueRecord.parent_id == parent_id,
        FatigueRecord.record_date == record_date
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Fatigue record not found")

    return record


@router.get("/trend/{parent_id}")
def get_fatigue_trend(
    parent_id: int,
    days: int = Query(7, ge=1, le=30, description="查询天数"),
    db: Session = Depends(get_db)
):
    """
    获取疲劳度趋势

    返回最近N天的疲劳度变化趋势
    """
    try:
        records = fatigue_calculator.get_fatigue_trend(db, parent_id, days)

        if not records:
            return {
                "parent_id": parent_id,
                "days": days,
                "records": [],
                "average": 0,
                "trend": "stable"
            }

        # 计算统计信息
        scores = [r.fatigue_score for r in records]
        average = sum(scores) / len(scores)
        min_score = min(scores)
        max_score = max(scores)

        # 判断趋势
        if len(scores) >= 2:
            recent_avg = sum(scores[-3:]) / min(3, len(scores))
            earlier_avg = sum(scores[:-3]) / max(1, len(scores) - 3) if len(scores) > 3 else recent_avg

            if recent_avg < earlier_avg - 0.1:
                trend = "improving"
            elif recent_avg > earlier_avg + 0.1:
                trend = "worsening"
            else:
                trend = "stable"
        else:
            trend = "stable"

        return {
            "parent_id": parent_id,
            "days": days,
            "records": records,
            "average": round(average, 3),
            "min": round(min_score, 3),
            "max": round(max_score, 3),
            "trend": trend
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analyze/{parent_id}")
def analyze_fatigue(
    parent_id: int,
    record_date: date = Query(..., description="分析日期"),
    db: Session = Depends(get_db)
):
    """
    分析疲劳度

    返回疲劳度的详细分析，包括：
    - 历史平均
    - 百分位
    - 风险等级
    - 改善建议
    """
    try:
        analysis = fatigue_calculator.analyze_fatigue(db, parent_id, record_date)
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compare")
def compare_parents(
    parent_ids: List[int] = Query(..., description="父母ID列表"),
    record_date: date = Query(..., description="对比日期"),
    db: Session = Depends(get_db)
):
    """
    对比父母的疲劳度

    返回双方的疲劳度对比和负载均衡评分
    """
    try:
        comparison = fatigue_calculator.compare_parents_fatigue(db, record_date, parent_ids)
        return comparison
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sleep", response_model=SleepRecordResponse)
def record_sleep(
    record: SleepRecordCreate,
    db: Session = Depends(get_db)
):
    """
    记录睡眠

    保存父母的睡眠记录
    """
    try:
        # 计算睡眠时长
        duration = (record.sleep_end - record.sleep_start).total_seconds() / 3600

        db_record = SleepRecord(
            parent_id=record.parent_id,
            record_date=record.record_date,
            sleep_start=record.sleep_start,
            sleep_end=record.sleep_end,
            duration_hours=duration,
            quality=record.quality,
            interruptions=record.interruptions,
            notes=record.notes
        )

        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        return db_record

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sleep/{parent_id}")
def get_sleep_records(
    parent_id: int,
    start_date: date = Query(None, description="开始日期"),
    end_date: date = Query(None, description="结束日期"),
    db: Session = Depends(get_db)
):
    """
    获取睡眠记录

    返回指定时间范围内的睡眠记录
    """
    try:
        query = db.query(SleepRecord).filter(SleepRecord.parent_id == parent_id)

        if start_date:
            query = query.filter(SleepRecord.record_date >= start_date)
        if end_date:
            query = query.filter(SleepRecord.record_date <= end_date)

        records = query.order_by(SleepRecord.record_date.desc()).all()

        return {
            "parent_id": parent_id,
            "count": len(records),
            "records": records
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics/{parent_id}")
def get_fatigue_statistics(
    parent_id: int,
    days: int = Query(30, ge=1, le=90, description="统计天数"),
    db: Session = Depends(get_db)
):
    """
    获取疲劳度统计

    返回指定时间范围内的疲劳度统计信息
    """
    try:
        from datetime import timedelta

        start_date = date.today() - timedelta(days=days)

        records = db.query(FatigueRecord).filter(
            FatigueRecord.parent_id == parent_id,
            FatigueRecord.record_date >= start_date
        ).all()

        if not records:
            return {
                "parent_id": parent_id,
                "days": days,
                "message": "No records found"
            }

        scores = [r.fatigue_score for r in records]
        task_loads = [r.task_load for r in records]
        sleep_deficits = [r.sleep_deficit for r in records]

        return {
            "parent_id": parent_id,
            "days": days,
            "total_records": len(records),
            "fatigue": {
                "average": round(sum(scores) / len(scores), 3),
                "min": round(min(scores), 3),
                "max": round(max(scores), 3),
                "latest": round(scores[-1], 3) if scores else 0
            },
            "task_load": {
                "average": round(sum(task_loads) / len(task_loads), 3),
                "min": round(min(task_loads), 3),
                "max": round(max(task_loads), 3)
            },
            "sleep_deficit": {
                "average": round(sum(sleep_deficits) / len(sleep_deficits), 3),
                "min": round(min(sleep_deficits), 3),
                "max": round(max(sleep_deficits), 3)
            },
            "high_fatigue_days": sum(1 for s in scores if s >= 0.7),
            "low_fatigue_days": sum(1 for s in scores if s < 0.3)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
