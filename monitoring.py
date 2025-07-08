from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional

router = APIRouter()

THRESHOLDS = {
    "error_rate": 0.05,
    "latency": 1000
}

class MonitoringRequest(BaseModel):
    metrics: Dict[str, float] = Field(..., description="Deployment metrics (e.g., error_rate, latency)")

class MonitoringResponse(BaseModel):
    anomaly_detected: bool
    details: str
    anomalies: Dict[str, float]
    error: Optional[str] = None

@router.post("/anomaly-detect", response_model=MonitoringResponse, summary="Detect anomalies in deployment metrics.")
def anomaly_detect(req: MonitoringRequest) -> MonitoringResponse:
    try:
        anomalies = {}
        for key, threshold in THRESHOLDS.items():
            value = req.metrics.get(key)
            if value is not None and value > threshold:
                anomalies[key] = value
        if anomalies:
            return MonitoringResponse(
                anomaly_detected=True,
                details=f"Anomalies detected: {anomalies}",
                anomalies=anomalies
            )
        return MonitoringResponse(
            anomaly_detected=False,
            details="No anomalies detected.",
            anomalies={}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Anomaly detection failed: {str(e)}") 