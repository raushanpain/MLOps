from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.session import get_db
from ..services.prediction_service import PredictionService
from ..schemas.schemas import PredictionRequest, PredictionResponse

router = APIRouter(
    prefix="/predict",
    tags=["predict"]
)

@router.post("/{model_version_id}", response_model=PredictionResponse)
def predict(model_version_id: int, request: PredictionRequest, db: Session = Depends(get_db)):
    try:
        features = request.features
        prediction = PredictionService.make_prediction(db, model_version_id, features)
        return PredictionResponse(prediction=prediction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
