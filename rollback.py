from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()

class RollbackRequest(BaseModel):
    deployment_id: str = Field(..., description="Deployment identifier")
    risk_score: float = Field(..., description="Predicted risk score")
    anomaly_detected: bool = Field(..., description="Whether an anomaly was detected")

class RollbackResponse(BaseModel):
    rollback: bool
    reason: str
    error: Optional[str] = None

@router.post("/decide", response_model=RollbackResponse, summary="Decide whether to trigger a rollback.")
def decide_rollback(req: RollbackRequest) -> RollbackResponse:
    try:
        if req.risk_score > 0.7 or req.anomaly_detected:
            return RollbackResponse(rollback=True, reason="High risk or anomaly detected.")
        return RollbackResponse(rollback=False, reason="Deployment is healthy.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Rollback decision failed: {str(e)}") 