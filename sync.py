import os
import requests

API_KEY = os.getenv("HEVY_API_KEY")

headers = {
    "api-key": API_KEY,
    "accept": "application/json"
}

url = "https://api.hevyapp.com/v1/workouts?page=1&pageSize=5"

response = requests.get(url, headers=headers)

print(f"Status : {response.status_code}")

if response.status_code == 200:
    data = response.json()

    workouts = data.get("workouts", [])
    print(f"Nombre de séances reçues : {len(workouts)}")

    for workout in workouts:
        print(f"- {workout.get('title')} ({workout.get('start_time')})")
else:
    print(response.text)
