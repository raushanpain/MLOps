from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.session import get_db
from ..services.training_service import TrainingService
from ..schemas.schemas import TrainRequest, TrainingResponse

router = APIRouter(
    prefix="/models",
    tags=["models"]
)

@router.post("/train", response_model=TrainingResponse)
def train_model(request: TrainRequest, db: Session = Depends(get_db)):
    try:
        return TrainingService.train_new_model(db, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
