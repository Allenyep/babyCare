from __future__ import annotations

from datetime import datetime, date
from sqlalchemy import String, Integer, Text, ForeignKey, Date, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
import enum


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"


class TimeSlot(str, enum.Enum):
    EARLY = "early"
    MORNING = "morning"
    NOON = "noon"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    baby_id: Mapped[int] = mapped_column(ForeignKey("babies.id", ondelete="CASCADE"), nullable=False, index=True)
    template_id: Mapped[int | None] = mapped_column(ForeignKey("task_templates.id"))
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False, index=True)

    # Basic info
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=5, nullable=False)

    # Time info
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    time_slot: Mapped[TimeSlot] = mapped_column(String(20), nullable=False)
    assigned_to: Mapped[int | None] = mapped_column(ForeignKey("parents.id", ondelete="SET NULL"))

    # Status
    status: Mapped[TaskStatus] = mapped_column(String(20), default=TaskStatus.PENDING, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(default=None)
    completed_by: Mapped[int | None] = mapped_column(ForeignKey("parents.id", ondelete="SET NULL"))
    completion_notes: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relationships
    baby: Mapped["Baby"] = relationship("Baby", back_populates="tasks")
    template: Mapped["TaskTemplate"] = relationship("TaskTemplate")
    schedule: Mapped["Schedule"] = relationship("Schedule", back_populates="tasks")
    assigned_to_detail: Mapped["Parent"] = relationship("Parent", foreign_keys=[Task.assigned_to], back_populates="tasks")
    completion_records: Mapped[list["TaskCompletion"]] = relationship(
        "TaskCompletion", back_populates="task", cascade="all, delete-orphan"
    )
