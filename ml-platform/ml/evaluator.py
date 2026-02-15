from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

def evaluate_model(model, X_test, y_test, problem_type):
    y_pred = model.predict(X_test)
    metrics = {}

    if problem_type == "classification":
        metrics['accuracy'] = accuracy_score(y_test, y_pred)
        # Average='weighted' handles multiclass
        metrics['precision'] = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        metrics['recall'] = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        metrics['f1'] = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    elif problem_type == "regression":
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        metrics['rmse'] = rmse
        metrics['r2'] = r2
    
    return metrics
