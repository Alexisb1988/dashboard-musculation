import json
import os
from pathlib import Path

import requests

API_KEY = os.getenv("HEVY_API_KEY")

headers = {
    "api-key": API_KEY,
    "accept": "application/json"
}

url = "https://api.hevyapp.com/v1/workouts?page=1&pageSize=5"

response = requests.get(url, headers=headers)

if response.status_code != 200:
    raise Exception(f"Erreur API Hevy : {response.status_code}\n{response.text}")

data = response.json()

# Création du dossier data si besoin
Path("data").mkdir(exist_ok=True)

# Sauvegarde du JSON complet
with open("data/hevy_raw.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ {len(data.get('workouts', []))} séances sauvegardées.")
