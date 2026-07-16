import os
import requests

API_KEY = os.getenv("HEVY_API_KEY")

headers = {
    "api-key": API_KEY,
    "accept": "application/json"
}

url = "https://api.hevyapp.com/v1/workouts?page=1&pageSize=5"

response = requests.get(url, headers=headers)

print("Status :", response.status_code)
print(response.text)
