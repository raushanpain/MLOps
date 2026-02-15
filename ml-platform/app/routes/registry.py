from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database.session import get_db
from ..models.models import Model, ModelVersion
from ..schemas.schemas import ModelResponse, ModelVersionResponse

router = APIRouter(
    prefix="/registry", # Changed from /models to avoid conflict or just grouping
    tags=["registry"]
)

@router.get("/models", response_model=List[ModelResponse])
def list_models(db: Session = Depends(get_db)):
    models = db.query(Model).all()
    return models

@router.get("/models/{model_id}/versions", response_model=List[ModelVersionResponse])
def list_model_versions(model_id: int, db: Session = Depends(get_db)):
    versions = db.query(ModelVersion).filter(ModelVersion.model_id == model_id).all()
    return versions
