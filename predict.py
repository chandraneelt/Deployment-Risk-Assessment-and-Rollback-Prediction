import requests
data = {
"num_files_changed": 10,
"num_risky_changes": 2
}
response = requests.post(
"http://localhost:8000/risk-assessment/predict",json=data)
print(response.json())