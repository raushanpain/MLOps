from fastapi import FastAPI
from .database.connection import engine, Base
from .routes import dataset, training, prediction, registry

app = FastAPI(title="Mini ML Platform")

@app.on_event("startup")
def on_startup():
    # Create tables
    Base.metadata.create_all(bind=engine)

app.include_router(dataset.router)
app.include_router(training.router)
app.include_router(prediction.router)
app.include_router(registry.router)

@app.get("/")
def read_root():
    return {"message": "Mini ML Platform is running"}
