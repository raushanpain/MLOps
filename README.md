# ML Platform

A comprehensive machine learning platform built with FastAPI for training, evaluating, and deploying ML models with a REST API interface.

## Features

- **Model Training**: Train machine learning models with custom parameters
- **Dataset Management**: Upload and manage training datasets
- **Model Registry**: Track and manage multiple model versions
- **Predictions**: Make predictions using trained models
- **Database**: PostgreSQL integration for data persistence
- **REST API**: FastAPI-based endpoints for all operations

## Project Structure

```
ml-platform/
├── app/                          # Main FastAPI application
│   ├── main.py                  # FastAPI app initialization
│   ├── database/                # Database configuration
│   │   ├── connection.py        # Database connection setup
│   │   └── session.py           # SQLAlchemy session management
│   ├── models/                  # SQLAlchemy ORM models
│   │   └── models.py            # Database models
│   ├── routes/                  # API endpoints
│   │   ├── dataset.py           # Dataset management endpoints
│   │   ├── prediction.py        # Prediction endpoints
│   │   ├── registry.py          # Model registry endpoints
│   │   └── training.py          # Model training endpoints
│   ├── schemas/                 # Pydantic request/response schemas
│   │   └── schemas.py           # API data schemas
│   └── services/                # Business logic
│       ├── dataset_service.py   # Dataset handling
│       ├── prediction_service.py # Prediction logic
│       └── training_service.py  # Training orchestration
├── ml/                          # Machine learning utilities
│   ├── trainer.py               # Model training logic
│   ├── preprocessing.py         # Data preprocessing
│   └── evaluator.py             # Model evaluation
├── data/                        # Sample datasets
│   ├── train.csv                # Training data
│   └── customers.csv            # Customer data
├── saved_models/                # Trained model storage
├── create_db.py                 # Database initialization script
├── requirements.txt             # Python dependencies
└── verification.py              # Verification utilities
```

## Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the database**:
   ```bash
   python create_db.py
   ```

3. **Verify installation**:
   ```bash
   python verification.py
   ```

## Running the Application

### Start the FastAPI server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Access API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Dataset Management
- `POST /api/datasets/upload` - Upload a new dataset
- `GET /api/datasets` - List all datasets
- `GET /api/datasets/{id}` - Get dataset details

### Training
- `POST /api/training/train` - Start model training
- `GET /api/training/{id}` - Get training status
- `GET /api/training` - List all training jobs

### Model Registry
- `GET /api/registry` - List all models
- `GET /api/registry/{id}` - Get model details
- `POST /api/registry/{id}/promote` - Promote model to production

### Predictions
- `POST /api/predictions/predict` - Make predictions
- `POST /api/predictions/batch` - Batch predictions
- `GET /api/predictions/{id}` - Get prediction history

## Technologies Used

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Machine Learning**: scikit-learn, pandas, numpy
- **Server**: Uvicorn
- **Serialization**: Pickle, JSON

## Dependencies

See [requirements.txt](requirements.txt) for the complete list of dependencies.

Key packages:
- fastapi
- sqlalchemy
- pandas
- scikit-learn
- numpy
- uvicorn

## Configuration

Database connection and other settings can be configured in:
- `app/database/connection.py` - Database connection string
- `app/main.py` - FastAPI configuration

## Development

### Running tests:
```bash
pytest
```

### Code formatting:
```bash
black .
```

### Linting:
```bash
flake8
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Push to the branch
4. Open a pull request

## License

MIT License

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

---

**Repository**: https://github.com/raushanpain/MLOps.git
