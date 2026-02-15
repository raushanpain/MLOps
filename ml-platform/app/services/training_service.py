from sqlalchemy.orm import Session
from ..models.models import Model, ModelVersion, Dataset
from ..schemas.schemas import TrainRequest
from ml.trainer import train_model

class TrainingService:
    @staticmethod
    def train_new_model(db: Session, request: TrainRequest):
        # 1. Fetch Dataset
        dataset = db.query(Dataset).filter(Dataset.id == request.dataset_id).first()
        if not dataset:
            raise ValueError(f"Dataset with id {request.dataset_id} not found")

        # 2. Create Model Record
        model = Model(
            dataset_id=dataset.id,
            problem_type=request.problem_type,
            target_column=request.target_column
        )
        db.add(model)
        db.commit()
        db.refresh(model)

        # 3. Train Model
        # Version is 1 for new model
        current_version = 1 
        
        try:
            results = train_model(
                dataset_path=dataset.path,
                target_column=request.target_column,
                problem_type=request.problem_type,
                model_id=model.id,
                version=current_version
            )
        except Exception as e:
            # If training fails, maybe delete the model record or log it?
            # For now, we'll raise it.
            raise e

        # 4. Save Version
        model_version = ModelVersion(
            model_id=model.id,
            version=current_version,
            metrics=results['metrics'],
            model_path=results['model_path']
        )
        db.add(model_version)
        db.commit()
        db.refresh(model_version)

        return {
            "model_id": model.id,
            "version": current_version,
            "metrics": results['metrics']
        }
