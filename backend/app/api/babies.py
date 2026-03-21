from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.baby import Baby
from app.models.growth_record import GrowthRecord
from app.schemas.baby import BabyCreate, BabyUpdate, BabyResponse, GrowthRecordCreate, GrowthRecordResponse
from app.db.database import get_db

router = APIRouter(prefix="/babies", tags=["babies"])


@router.post("/", response_model=BabyResponse)
def create_baby(baby: BabyCreate, db: Session = Depends(get_db)):
    """Create a new baby profile"""
    db_baby = Baby(**baby.model_dump())
    db.add(db_baby)
    db.commit()
    db.refresh(db_baby)
    return db_baby


@router.get("/", response_model=List[BabyResponse])
def list_babies(db: Session = Depends(get_db)):
    """List all babies"""
    babies = db.query(Baby).all()
    return babies


@router.get("/{baby_id}", response_model=BabyResponse)
def get_baby(baby_id: int, db: Session = Depends(get_db)):
    """Get baby by ID"""
    baby = db.query(Baby).filter(Baby.id == baby_id).first()
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")
    return baby


@router.patch("/{baby_id}", response_model=BabyResponse)
def update_baby(baby_id: int, baby_update: BabyUpdate, db: Session = Depends(get_db)):
    """Update baby profile"""
    baby = db.query(Baby).filter(Baby.id == baby_id).first()
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")

    for field, value in baby_update.model_dump(exclude_unset=True).items():
        setattr(baby, field, value)

    db.commit()
    db.refresh(baby)
    return baby


@router.delete("/{baby_id}")
def delete_baby(baby_id: int, db: Session = Depends(get_db)):
    """Delete baby profile"""
    baby = db.query(Baby).filter(Baby.id == baby_id).first()
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")

    db.delete(baby)
    db.commit()
    return {"deleted": True}


@router.post("/{baby_id}/growth", response_model=GrowthRecordResponse)
def add_growth_record(
    baby_id: int,
    record: GrowthRecordCreate,
    db: Session = Depends(get_db)
):
    """Add growth record for baby"""
    baby = db.query(Baby).filter(Baby.id == baby_id).first()
    if not baby:
        raise HTTPException(status_code=404, detail="Baby not found")

    db_record = GrowthRecord(baby_id=baby_id, **record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


@router.get("/{baby_id}/growth", response_model=List[GrowthRecordResponse])
def list_growth_records(baby_id: int, db: Session = Depends(get_db)):
    """List all growth records for a baby"""
    records = db.query(GrowthRecord).filter(
        GrowthRecord.baby_id == baby_id
    ).order_by(GrowthRecord.record_date.desc()).all()
    return records
