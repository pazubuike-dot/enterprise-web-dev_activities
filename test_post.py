import requests

url = "http://localhost:8000/api/save_analysis"
headers = {"Authorization": "Bearer test-token"}
payload = {
    "algorithm": "linear_search",
    "n_max": 100,
    "step": 10
}

response = requests.post(url, json=payload, headers=headers)
print("Status Code:", response.status_code)
print("Response JSON:", response.json())