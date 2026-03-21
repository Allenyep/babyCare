from __future__ import annotations

from datetime import datetime
from sqlalchemy import String, Integer, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class Parent(Base):
    __tablename__ = "parents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    baby_id: Mapped[int] = mapped_column(ForeignKey("babies.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    relationship: Mapped[str] = mapped_column(String(20), nullable=False)  # 'mother', 'father', etc.
    avatar: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(20))

    # Time constraints
    work_start_time: Mapped[str | None] = mapped_column(String(5))  # HH:MM
    work_end_time: Mapped[str | None] = mapped_column(String(5))
    sleep_start_time: Mapped[str | None] = mapped_column(String(5))
    sleep_end_time: Mapped[str | None] = mapped_column(String(5))
    unavailable_slots: Mapped[dict | None] = mapped_column(JSON)  # [{"day": 1, "start": "09:00", "end": "12:00"}]

    # Capabilities and preferences
    capabilities: Mapped[list[str] | None] = mapped_column(JSON)  # ["diaper", "feeding", "cooking"]
    target_sleep_hours: Mapped[float] = mapped_column(Float, default=7.0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relationships
    baby: Mapped["Baby"] = relationship("Parent", back_populates="parents")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="assigned_to_detail")
    completions: Mapped[list["TaskCompletion"]] = relationship("TaskCompletion", back_populates="parent")
