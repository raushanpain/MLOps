import shutil
import os
from fastapi import UploadFile
from sqlalchemy.orm import Session
from ..models.models import Dataset

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

class DatasetService:
    @staticmethod
    def upload_dataset(db: Session, file: UploadFile):
        file_location = os.path.join(DATA_DIR, file.filename)
        
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        dataset = Dataset(name=file.filename, path=file_location)
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        return dataset

    @staticmethod
    def get_dataset(db: Session, dataset_id: int):
        return db.query(Dataset).filter(Dataset.id == dataset_id).first()
