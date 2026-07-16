"""
Dashboard Musculation
Version : 0.2.1

Cette version :
- récupère toutes les pages Hevy
- fusionne toutes les séances
- sauvegarde un JSON unique

La prochaine étape filtrera les séances avant le 01/01/2026.
"""

import json
import math
import os
from pathlib import Path
from datetime import datetime

import requests

BASE_URL = "https://api.hevyapp.com/v1"
API_KEY = os.getenv("HEVY_API_KEY")

HEADERS = {
    "api-key": API_KEY,
    "accept": "application/json"
}
# ==========================================================
# Configuration
# ==========================================================

# Date minimale des séances conservées
MIN_DATE = datetime(2026, 1, 1)

def log(message):
    print(f"[INFO] {message}")


def get_workouts(page=1, page_size=5):

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

    Path("data").mkdir(exist_ok=True)

    with open(f"data/{filename}", "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )

# ==========================================================
# Filtrage des séances
# ==========================================================

def filter_workouts(workouts):
    """
    Conserve uniquement les séances dont la date est
    supérieure ou égale au 01/01/2026.

    Paramètres
    ----------
    workouts : list
        Liste complète des séances téléchargées.

    Retour
    ------
    tuple
        (
            liste des séances conservées,
            nombre de séances ignorées
        )
    """

    kept_workouts = []
    ignored_count = 0

    for workout in workouts:

        workout_date = datetime.fromisoformat(
            workout["start_time"].replace("Z", "+00:00")
        )

        workout_date = workout_date.replace(tzinfo=None)

        if workout_date >= MIN_DATE:
            kept_workouts.append(workout)
        else:
            ignored_count += 1

    return kept_workouts, ignored_count
    
def main():

    print("=" * 50)
    print("Dashboard Musculation")
    print("Version 0.2.1")
    print("=" * 50)
    print()

    all_workouts = []

    page = 1
    total_pages = None

    while True:

        log(f"Lecture page {page}")

        data = get_workouts(page)

        workouts = data.get("workouts", [])

        if total_pages is None:
            total_pages = data.get("page_count", 1)
            log(f"{total_pages} pages détectées")

        log(f"{len(workouts)} séances")

        all_workouts.extend(workouts)

        if page >= total_pages:
            break

        page += 1

    result = {
        "workouts": all_workouts,
        "count": len(all_workouts)
    }

    save_json(result, "hevy_raw.json")

    print()
    print("=" * 50)
    log("Import terminé")
    log(f"{len(all_workouts)} séances récupérées")
    print("=" * 50)


if __name__ == "__main__":
    main()
