from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd
import numpy as np

def get_preprocessor(X: pd.DataFrame):
    """
    Auto-detects numerical and categorical columns and returns a ColumnTransformer.
    """
    # Identify numerical and categorical columns
    search_numeric_features = X.select_dtypes(include=[np.number]).columns
    search_categorical_features = X.select_dtypes(include=['object', 'category']).columns

    # Remove target column if present (though X should be features only usually)
    # Ideally X passed here is already separated from y.
    
    numeric_features = list(search_numeric_features)
    categorical_features = list(search_categorical_features)

    # Define transformers
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Bundle preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    return preprocessor

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning if needed before split. 
    For now, we rely on the pipeline to handle missing values.
    """
    return df
