from fastapi import APIRouter, Body, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import Dict, Optional
import numpy as np
from sklearn.linear_model import LogisticRegression
import pandas as pd
import joblib
import os

router = APIRouter()

MODEL_PATH = "risk_model.joblib"

class RiskAssessmentRequest(BaseModel):
    num_files_changed: int = Field(..., description="Number of files changed")
    num_risky_changes: int = Field(..., description="Number of risky changes")

class RiskAssessmentResponse(BaseModel):
    risk_score: float
    rollback_likelihood: float
    error: Optional[str] = None

class TrainResponse(BaseModel):
    message: str
    accuracy: Optional[float] = None
    error: Optional[str] = None

def load_model() -> LogisticRegression:
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    X_train = np.array([
        [1, 0], [2, 0], [5, 1], [10, 2], [20, 5], [3, 1], [7, 2], [15, 4]
    ])
    y_train = np.array([0, 0, 0, 1, 1, 0, 1, 1])
    model = LogisticRegression()
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)
    return model

@router.post("/predict", response_model=RiskAssessmentResponse, summary="Predict rollback risk from change features.")
def predict_risk(req: RiskAssessmentRequest) -> RiskAssessmentResponse:
    try:
        model = load_model()
        X = np.array([[req.num_files_changed, req.num_risky_changes]])
        prob = model.predict_proba(X)[0][1]
        return RiskAssessmentResponse(risk_score=float(prob), rollback_likelihood=float(prob))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Risk assessment failed: {str(e)}")

@router.post("/train", response_model=TrainResponse, summary="Train the risk model with uploaded CSV data.")
def train_model(file: UploadFile = File(...)) -> TrainResponse:
    try:
        df = pd.read_csv(file.file)
        X = df[["num_files_changed", "num_risky_changes"]].values
        y = df["rollback_needed"].values
        model = LogisticRegression()
        model.fit(X, y)
        joblib.dump(model, MODEL_PATH)
        accuracy = model.score(X, y)
        return TrainResponse(message="Model trained and saved.", accuracy=accuracy)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Model training failed: {str(e)}") 