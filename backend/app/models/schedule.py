from __future__ import annotations

from datetime import datetime, date
from sqlalchemy import String, Integer, Float, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class TaskCompletion(Base):
    """Record of task completion"""
    __tablename__ = "task_completions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parents.id", ondelete="CASCADE"), nullable=False)

    completed_at: Mapped[datetime] = mapped_column(nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    rating: Mapped[int | None] = mapped_column(Integer)  # Quality rating 1-5

    # Relationships
    task: Mapped["Task"] = relationship("Task", back_populates="completion_records")
    parent: Mapped["Parent"] = relationship("Parent", back_populates="completions")


class Schedule(Base):
    """Daily schedule with tasks and statistics"""
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    baby_id: Mapped[int] = mapped_column(ForeignKey("babies.id", ondelete="CASCADE"), nullable=False, index=True)
    date: Mapped[date] = mapped_column(date, nullable=False, index=True)

    # Statistics
    total_tasks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completed_tasks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completion_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Fatigue and balance scores
    fatigue_scores: Mapped[dict] = mapped_column(JSON, default=dict)  # {parent_id: fatigue_score}
    balance_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Special flags
    is_special_day: Mapped[bool] = mapped_column(default=False, nullable=False)
    special_notes: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relationships
    baby: Mapped["Baby"] = relationship("Baby", back_populates="schedules")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="schedule", cascade="all, delete-orphan")
