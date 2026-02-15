from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.connection import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    path = Column(String(500))
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    models = relationship("Model", back_populates="dataset")


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    problem_type = Column(String(50))  # classification / regression
    target_column = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    dataset = relationship("Dataset", back_populates="models")
    versions = relationship("ModelVersion", back_populates="model")


class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("models.id"))
    version = Column(Integer)
    metrics = Column(JSON)
    model_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    model = relationship("Model", back_populates="versions")
