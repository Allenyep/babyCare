
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class SleepLog(Base):
    """Sleep log for baby and parents"""
    __tablename__ = "sleep_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    baby_id: Mapped[int] = mapped_column(ForeignKey("babies.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("parents.id", ondelete="SET NULL"))

    sleep_type: Mapped[str] = mapped_column(String(10), nullable=False)  # 'nap' or 'night'
    start_time: Mapped[datetime] = mapped_column(nullable=False, index=True)
    end_time: Mapped[Optional[datetime]] = mapped_column(default=None)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)

    notes: Mapped[Optional[str]] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)

    # Relationships
    baby: Mapped["Baby"] = relationship("Baby")
    parent: Mapped["Parent"] = relationship("Parent")
