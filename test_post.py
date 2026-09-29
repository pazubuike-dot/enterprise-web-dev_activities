import requests

base_url = "http://localhost:8000"
payload = {
    "algorithm": "linear_search",
    "n_max": 100,
    "step": 10
}

print("=== RUNNING AUTOMATED API SECURITY TESTS ===\n")

# 1. Test Unauthorized Request (Expect 401)
print("Testing Test 1: Request WITHOUT token (Expected: 401)...")
response_unauth = requests.post(f"{base_url}/api/save_analysis", json=payload)
print("Status Code:", response_unauth.status_code)
print("Response JSON:", response_unauth.json())
print("-" * 50)

# 2. Test Authorized Request (Expect 201)
print("Testing Test 2: Request WITH valid JWT token (Expected: 201)...")
# Automatically fetch a fresh token
token_res = requests.get(f"{base_url}/api/token")
access_token = token_res.json()["access_token"]

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

response_auth = requests.post(f"{base_url}/api/save_analysis", json=payload, headers=headers)
print("Status Code:", response_auth.status_code)
print("Response JSON:", response_auth.json())
print("-" * 50)

print("=== ALL TESTS COMPLETED ===")