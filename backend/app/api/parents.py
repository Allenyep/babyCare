from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.parent import Parent
from app.schemas.parent import ParentCreate, ParentUpdate, ParentResponse
from app.db.database import get_db

router = APIRouter(prefix="/parents", tags=["parents"])


@router.post("/", response_model=ParentResponse)
def create_parent(parent: ParentCreate, db: Session = Depends(get_db)):
    """Create a new parent/caregiver"""
    db_parent = Parent(**parent.model_dump())
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return db_parent


@router.get("/", response_model=List[ParentResponse])
def list_parents(db: Session = Depends(get_db)):
    """List all parents"""
    parents = db.query(Parent).all()
    return parents


@router.get("/{parent_id}", response_model=ParentResponse)
def get_parent(parent_id: int, db: Session = Depends(get_db)):
    """Get parent by ID"""
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent


@router.patch("/{parent_id}", response_model=ParentResponse)
def update_parent(
    parent_id: int,
    parent_update: ParentUpdate,
    db: Session = Depends(get_db)
):
    """Update parent information"""
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")

    for field, value in parent_update.model_dump(exclude_unset=True).items():
        setattr(parent, field, value)

    db.commit()
    db.refresh(parent)
    return parent


@router.delete("/{parent_id}")
def delete_parent(parent_id: int, db: Session = Depends(get_db)):
    """Delete parent"""
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")

    db.delete(parent)
    db.commit()
    return {"deleted": True}
