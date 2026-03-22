
from datetime import date, datetime
from typing import Optional
from sqlalchemy import Float, Integer, Date, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class GrowthRecord(Base):
    __tablename__ = "growth_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    baby_id: Mapped[int] = mapped_column(ForeignKey("babies.id", ondelete="CASCADE"), nullable=False, index=True)
    record_date: Mapped[date] = mapped_column(Date, nullable=False)
    weight: Mapped[Optional[float]] = mapped_column(Float)  # kg
    height: Mapped[Optional[float]] = mapped_column(Float)  # cm
    head_circumference: Mapped[Optional[float]] = mapped_column(Float)  # cm
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)

    # Relationship
    baby: Mapped["Baby"] = relationship("Baby", back_populates="growth_records")
