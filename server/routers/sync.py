from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from .. import models, schemas, database
from .auth import get_current_user, get_db

router = APIRouter()

class AnalyticsSync(BaseModel):
    items: List[schemas.AnalyticsCreate]

@router.post("/sync")
def sync_analytics(sync_data: AnalyticsSync, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Syncs offline analytics data to the server.
    Accepts a list of analytics records.
    """
    for item in sync_data.items:
        # Create new analytics record
        db_analytics = models.Analytics(
            user_id=current_user.id,
            exam_id=item.exam_id,
            chapter_name=item.chapter_name,
            score=item.score,
            time_per_question_avg=item.time_per_question_avg
        )
        db.add(db_analytics)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to sync analytics: {str(e)}")

    return {"message": "Sync successful", "count": len(sync_data.items)}

