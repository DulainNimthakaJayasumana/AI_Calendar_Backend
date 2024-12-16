from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/events", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = models.Event(
        title=event.title,
        description=event.description,
        start_time=event.start_time,
        end_time=event.end_time
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/events", response_model=List[schemas.Event])
def list_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()

@router.get("/events/{event_id}", response_model=schemas.Event)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Not found")
    return event
