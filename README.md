<<<<<<< HEAD
# Deployment Risk Assessment and Rollback Prediction

## Overview

This project analyzes deployment changes, predicts the likelihood of needing a rollback, and automates rollback triggers using AI/ML and real-time monitoring.

## Modules

- **Change Analyzer:** Parses code/config diffs and summarizes changes.
- **Risk Assessment:** Predicts rollback likelihood using ML. Supports model retraining with real data.
- **Deployment Monitoring:** Detects anomalies in post-deployment metrics.
- **Rollback Decision & Automation:** Triggers rollbacks based on risk and anomalies.

## Tech Stack

- Python (FastAPI)
- scikit-learn, pandas, numpy, gitpython, joblib

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the API server:
   ```bash
   uvicorn main:app --reload
   ```
3. Open the dashboard:
   [http://localhost:8000/](http://localhost:8000/)

## API Endpoints

### Change Analyzer

- `POST /change-analyzer/analyze`
  - **Request:**
    ```json
    { "repo_path": ".", "base_commit": "abc123", "new_commit": "def456" }
    ```
  - **Response:**
    ```json
    { "files_changed": [...], "risky_changes": [...], "summary": "..." }
    ```

### Risk Assessment

- `POST /risk-assessment/predict`
  - **Request:**
    ```json
    { "num_files_changed": 5, "num_risky_changes": 2 }
    ```
  - **Response:**
    ```json
    { "risk_score": 0.65, "rollback_likelihood": 0.65 }
    ```
- `POST /risk-assessment/train`
  - **Upload a CSV** with columns: `num_files_changed`, `num_risky_changes`, `rollback_needed` (0/1)
  - **Response:**
    ```json
    { "message": "Model trained and saved.", "accuracy": 0.92 }
    ```

### Monitoring

- `POST /monitoring/anomaly-detect`
  - **Request:**
    ```json
    { "metrics": { "error_rate": 0.07, "latency": 900 } }
    ```
  - **Response:**
    ```json
    { "anomaly_detected": true, "details": "Anomalies detected: ...", "anomalies": { ... } }
    ```

### Rollback Decision

- `POST /rollback/decide`
  - **Request:**
    ```json
    { "deployment_id": "def456", "risk_score": 0.8, "anomaly_detected": true }
    ```
  - **Response:**
    ```json
    { "rollback": true, "reason": "High risk or anomaly detected." }
    ```

### Full Pipeline

- `POST /pipeline/run`
  - **Request:**
    ```json
    {
      "repo_path": ".",
      "base_commit": "abc123",
      "new_commit": "def456",
      "metrics": { "error_rate": 0.02, "latency": 1100 }
    }
    ```
  - **Response:**
    ```json
    {
      "change_analysis": {...},
      "risk_assessment": {...},
      "monitoring": {...},
      "rollback_decision": {...}
    }
    ```

## Model Training with Real Data

- Prepare a CSV file with columns: `num_files_changed`, `num_risky_changes`, `rollback_needed` (0 or 1)
- Use `/risk-assessment/train` to upload and retrain the model.

## Structure

- `main.py`: FastAPI entry point
- `change_analyzer.py`: Change analysis logic
- `risk_assessment.py`: ML model for risk prediction (with persistence and training)
- `monitoring.py`: Anomaly detection
- `rollback.py`: Rollback automation
- `static/index.html`: Simple dashboard UI

## Example Usage

- Use the dashboard or API endpoints to analyze changes, assess risk, monitor deployments, and trigger rollbacks.
- Retrain the risk model with your own data for improved accuracy.

## License

MIT
=======
# Deployment-Risk-Assessment-and-Rollback-Prediction
>>>>>>> ca2cb23adf2fee2510bf0bf8d4627c53c342f6ec
