"""
Dashboard Musculation
Version : 0.2.0

Cette version :
- se connecte à l'API Hevy
- récupère une page de séances
- sauvegarde le JSON dans data/hevy_raw.json

La pagination sera ajoutée à l'étape suivante.
"""

import json
import os
from pathlib import Path

import requests

BASE_URL = "https://api.hevyapp.com/v1"
API_KEY = os.getenv("HEVY_API_KEY")

HEADERS = {
    "api-key": API_KEY,
    "accept": "application/json"
}


def get_workouts(page=1, page_size=5):
    """
    Récupère une page de séances.
    """

    response = requests.get(
        f"{BASE_URL}/workouts",
        headers=HEADERS,
        params={
            "page": page,
            "pageSize": page_size
        }
    )

    response.raise_for_status()

    return response.json()


def save_json(data, filename):
    """
    Sauvegarde un JSON joliment formaté.
    """

    Path("data").mkdir(exist_ok=True)

    with open(f"data/{filename}", "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


def main():

    print("=" * 50)
    print("Dashboard Musculation")
    print("Version 0.2.0")
    print("=" * 50)

    print()

    print("Connexion à Hevy...")

    all_workouts = []

    page = 1

    while True:

    data = get_workouts(page)

    workouts = data.get("workouts", [])

    print(f"OK ({len(workouts)} séances reçues)")

    save_json(data, "hevy_raw.json")

    print()

    print("Sauvegarde effectuée.")

    print()

    print("Dernières séances :")

    for workout in workouts:

        print(
            f"- {workout['title']} | {workout['start_time']}"
        )


if __name__ == "__main__":
    main()
