from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, date

from app.db.database import Base


class FatigueRecord(Base):
    """疲劳度记录表"""
    __tablename__ = "fatigue_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey("parents.id"), nullable=False)
    record_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    # 疲劳度评分
    fatigue_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # 影响因素
    task_load: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # 任务负载
    sleep_deficit: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # 睡眠不足
    work_hours: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # 工作时长

    # 统计信息
    total_tasks: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_task_duration: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # 分钟
    actual_sleep: Mapped[float] = mapped_column(Float, nullable=True)  # 实际睡眠时长(小时)
    target_sleep: Mapped[float] = mapped_column(Float, nullable=True)  # 目标睡眠时长(小时)

    # 详细信息
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    # parent = relationship("Parent", back_populates="fatigue_records")


class SleepRecord(Base):
    """睡眠记录表"""
    __tablename__ = "sleep_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey("parents.id"), nullable=False)
    record_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    # 睡眠信息
    sleep_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    sleep_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration_hours: Mapped[float] = mapped_column(Float, nullable=False)

    # 睡眠质量
    quality: Mapped[str] = mapped_column(String(20), nullable=True)  # good/fair/poor
    interruptions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # 夜醒次数

    # 备注
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # 关系
    # parent = relationship("Parent", back_populates="sleep_records")
