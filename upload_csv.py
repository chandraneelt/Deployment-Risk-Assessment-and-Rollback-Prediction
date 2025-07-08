import requests

with open("deployments.csv", "rb") as f:
    response = requests.post(
        "http://localhost:8000/risk-assessment/train",
        files={"file": f}
    )
print(response.json())