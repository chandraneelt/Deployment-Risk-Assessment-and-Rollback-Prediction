from fastapi import FastAPI, Body
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from change_analyzer import router as change_analyzer_router, analyze_changes
from risk_assessment import router as risk_assessment_router, predict_risk
from monitoring import router as monitoring_router, anomaly_detect
from rollback import router as rollback_router, decide_rollback

app = FastAPI(title="Deployment Risk Assessment and Rollback Prediction")

app.include_router(change_analyzer_router, prefix="/change-analyzer")
app.include_router(risk_assessment_router, prefix="/risk-assessment")
app.include_router(monitoring_router, prefix="/monitoring")
app.include_router(rollback_router, prefix="/rollback")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def root():
    return RedirectResponse(url="/index.html")

@app.post("/pipeline/run")
def run_pipeline(
    repo_path: str = Body(...),
    base_commit: str = Body(...),
    new_commit: str = Body(...),
    metrics: dict = Body(...)
):
    change_result = analyze_changes(repo_path, base_commit, new_commit)
    num_files_changed = len(change_result.get("files_changed", []))
    num_risky_changes = len(change_result.get("risky_changes", []))
    risk_result = predict_risk({
        "num_files_changed": num_files_changed,
        "num_risky_changes": num_risky_changes
    })
    risk_score = risk_result.get("risk_score", 0)
    anomaly_result = anomaly_detect(metrics)
    anomaly_detected = anomaly_result.get("anomaly_detected", False)
    rollback_result = decide_rollback(
        deployment_id=f"{new_commit}",
        risk_score=risk_score,
        anomaly_detected=anomaly_detected
    )
    return {
        "change_analysis": change_result,
        "risk_assessment": risk_result,
        "monitoring": anomaly_result,
        "rollback_decision": rollback_result
    } 