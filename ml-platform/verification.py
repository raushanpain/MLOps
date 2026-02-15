import os
import shutil
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.session import get_db
from app.database.connection import Base
import pandas as pd
import io

# Setup Test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_end_to_end():
    # 0. Cleanup
    if os.path.exists("data"):
        shutil.rmtree("data")
    if os.path.exists("saved_models"):
        shutil.rmtree("saved_models")
    os.makedirs("data", exist_ok=True)
    os.makedirs("saved_models", exist_ok=True)

    # 1. Create Dummy CSV
    csv_content = """feature1,feature2,target
1.0,2.0,0
1.5,1.8,0
5.0,8.0,1
5.5,8.2,1
"""
    files = {'file': ('train.csv', csv_content, 'text/csv')}

    # 2. Upload Dataset
    print("Uploading dataset...")
    response = client.post("/datasets/upload", files=files)
    assert response.status_code == 200
    dataset_id = response.json()['id']
    print(f"Dataset uploaded. ID: {dataset_id}")

    # 3. Train Model
    print("Training model...")
    response = client.post("/models/train", json={
        "dataset_id": dataset_id,
        "target_column": "target",
        "problem_type": "classification"
    })
    assert response.status_code == 200
    data = response.json()
    model_id = data['model_id']
    version = data['version']
    metrics = data['metrics']
    print(f"Model trained. ID: {model_id}, Version: {version}")
    print(f"Metrics: {metrics}")

    # 4. Predict
    print("Making prediction...")
    
    # Get model version id via registry to be sure (since train returns metrics but not full object usually, 
    # though we could return it. Here we use the registry to verify it works too).
    response = client.get(f"/registry/models/{model_id}/versions")
    assert response.status_code == 200
    versions = response.json()
    # Find the version we just trained
    target_version = next(v for v in versions if v['version'] == version)
    model_version_id = target_version['id']
    print(f"Target Model Version ID: {model_version_id}")

    prediction_response = client.post(f"/predict/{model_version_id}", json={
        "features": {
            "feature1": 1.2,
            "feature2": 1.9
        }
    })
    
    if prediction_response.status_code != 200:
        print(f"Prediction failed: {prediction_response.text}")
        return False
        
    print(f"Prediction: {prediction_response.json()}")
    return True

if __name__ == "__main__":
    try:
        if test_end_to_end() is False:
            exit(1)
        print("Verification Successful!")
    except Exception as e:
        print(f"Verification Failed: {e}")
        exit(1)
