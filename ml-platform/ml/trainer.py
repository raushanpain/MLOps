import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import joblib
import os
from .preprocessing import get_preprocessor
from .evaluator import evaluate_model

MODEL_DIR = "saved_models"
os.makedirs(MODEL_DIR, exist_ok=True)

def get_model(problem_type: str):
    if problem_type == "classification":
        # Default to Random Forest for robustness
        return RandomForestClassifier(n_estimators=100)
    elif problem_type == "regression":
        return RandomForestRegressor(n_estimators=100)
    else:
        raise ValueError(f"Unknown problem type: {problem_type}")

def train_model(dataset_path: str, target_column: str, problem_type: str, model_id: int, version: int):
    # 1. Load Data
    df = pd.read_csv(dataset_path)
    
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset.")
    
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # 2. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Preprocessing
    # We pass X to get_preprocessor to auto-detect columns
    preprocessor = get_preprocessor(X)

    # 4. Model Selection
    clf = get_model(problem_type)

    # 5. Create Pipeline
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', clf)
    ])

    # 6. Train
    model_pipeline.fit(X_train, y_train)

    # 7. Evaluate
    metrics = evaluate_model(model_pipeline, X_test, y_test, problem_type)

    # 8. Save Model
    save_filename = f"model_{model_id}_v{version}.pkl"
    save_path = os.path.join(MODEL_DIR, save_filename)
    joblib.dump(model_pipeline, save_path)

    return {
        "metrics": metrics,
        "model_path": save_path
    }
