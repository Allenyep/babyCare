
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class TaskTemplate(Base):
    """Template for generating tasks from knowledge base"""
    __tablename__ = "task_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(20), nullable=False)  # feeding, diaper, education, etc.
    description: Mapped[Optional[str]] = mapped_column(Text)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    # Trigger conditions
    min_age_months: Mapped[Optional[int]] = mapped_column(Integer)
    max_age_months: Mapped[Optional[int]] = mapped_column(Integer)
    frequency: Mapped[str] = mapped_column(String(20), nullable=False)  # daily, weekly, monthly, once

    # Time constraints
    preferred_time_slots: Mapped[Optional[List[str]]] = mapped_column(JSON)  # ["early", "morning", ...]
    required: Mapped[bool] = mapped_column(default=False, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=5, nullable=False)  # 1-10

    # Knowledge base source
    source: Mapped[Optional[str]] = mapped_column(String(50))  # "CDC", "营养学会", "自定义"
    source_url: Mapped[Optional[str]] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
