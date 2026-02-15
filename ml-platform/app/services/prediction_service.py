from sqlalchemy.orm import Session
from ..models.models import ModelVersion
import joblib
import pandas as pd
import os

class PredictionService:
    @staticmethod
    def make_prediction(db: Session, model_version_id: int, features: dict):
        # 1. Get Model Version
        version_entry = db.query(ModelVersion).filter(ModelVersion.id == model_version_id).first()
        if not version_entry:
            raise ValueError(f"Model version {model_version_id} not found")

        model_path = version_entry.model_path
        if not os.path.exists(model_path):
             raise FileNotFoundError(f"Model file not found at {model_path}")

        # 2. Load Model
        # In a real app, we would cache this
        model = joblib.load(model_path)

        # 3. Convert features to DataFrame
        # The pipeline expects a DataFrame with specific columns
        df = pd.DataFrame([features])

        # 4. Predict
        try:
            prediction = model.predict(df)
            return prediction.tolist()
        except Exception as e:
            raise ValueError(f"Prediction failed: {str(e)}")
