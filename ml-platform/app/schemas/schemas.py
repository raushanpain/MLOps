from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import datetime

# Dataset Schemas
class DatasetBase(BaseModel):
    name: str

class DatasetCreate(DatasetBase):
    path: str

class DatasetResponse(DatasetBase):
    id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

# Training Schemas
class TrainRequest(BaseModel):
    dataset_id: int
    target_column: str
    problem_type: str  # "classification" or "regression"

class TrainingResponse(BaseModel):
    model_id: int
    version: int
    metrics: Dict[str, Any]

# Prediction Schemas
class PredictionRequest(BaseModel):
    features: Dict[str, Any]

class PredictionResponse(BaseModel):
    prediction: Any

# Registry Schemas
class ModelVersionResponse(BaseModel):
    id: int
    version: int
    metrics: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True

class ModelResponse(BaseModel):
    id: int
    problem_type: str
    target_column: str
    created_at: datetime
    versions: List[ModelVersionResponse] = []

    class Config:
        orm_mode = True
