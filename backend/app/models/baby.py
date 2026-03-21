from __future__ import annotations

from datetime import date, datetime
from sqlalchemy import String, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class Baby(Base):
    __tablename__ = "babies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    nickname: Mapped[str | None] = mapped_column(String(50))
    birthday: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)  # 'male' or 'female'
    avatar: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now, nullable=False
    )

    # Relationships
    parents: Mapped[list["Parent"]] = relationship(
        "Parent", back_populates="baby", cascade="all, delete-orphan"
    )
    growth_records: Mapped[list["GrowthRecord"]] = relationship(
        "GrowthRecord", back_populates="baby", cascade="all, delete-orphan"
    )
    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="baby", cascade="all, delete-orphan"
    )
    schedules: Mapped[list["Schedule"]] = relationship(
        "Schedule", back_populates="baby", cascade="all, delete-orphan"
    )

    @property
    def age_months(self) -> int:
        """Calculate baby's age in months"""
        today = date.today()
        years = today.year - self.birthday.year
        months = today.month - self.birthday.month
        return years * 12 + months
