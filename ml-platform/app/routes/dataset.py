from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ..database.session import get_db
from ..services.dataset_service import DatasetService
from ..schemas.schemas import DatasetResponse

router = APIRouter(
    prefix="/datasets",
    tags=["datasets"]
)

@router.post("/upload", response_model=DatasetResponse)
def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        return DatasetService.upload_dataset(db, file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
