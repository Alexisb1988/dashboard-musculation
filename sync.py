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
# Création du fichier metadata.json
# ==========================================================

def save_metadata(
    downloaded_count,
    kept_count,
    ignored_count,
    workouts
):
    """
    Crée le fichier metadata.json.

    Ce fichier permettra plus tard de savoir :

    - quand la dernière synchronisation a eu lieu
    - combien de séances existent
    - quelle est la première séance
    - quelle est la dernière séance
    """

    if len(workouts) == 0:

        first_workout = None
        last_workout = None

    else:

        dates = sorted([
            workout["start_time"]
            for workout in workouts
        ])

        first_workout = dates[0]
        last_workout = dates[-1]

    metadata = {

        "version": "0.2.3",

        "last_sync": datetime.now().astimezone().isoformat(),

        "downloaded_workouts": downloaded_count,

        "kept_workouts": kept_count,

        "ignored_workouts": ignored_count,

        "first_workout": first_workout,

        "last_workout": last_workout

    }

    save_json(
        metadata,
        "metadata.json"
    )


# ==========================================================
# Téléchargement des séances
# ==========================================================

def download_all_workouts():
    """
    Télécharge toutes les séances disponibles sur Hevy.

    Retour
    ------
    list
        Liste complète des séances.
    """

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

    return all_workouts


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

    all_workouts = download_all_workouts()

# ==========================================================
    # Sauvegarde des données brutes
    # ==========================================================

    raw_data = {
        "workouts": all_workouts,
        "count": len(all_workouts)
    }

    save_json(raw_data, "hevy_raw.json")

    # ==========================================================
    # Création de la base de données filtrée
    # ==========================================================

    filtered_workouts, ignored_count = filter_workouts(all_workouts)

    database = {
        "workouts": filtered_workouts,
        "count": len(filtered_workouts)
    }

    save_json(database, "hevy_database.json")

     # ==========================================================
    # Sauvegarde des métadonnées
    # ==========================================================

    save_metadata(
        downloaded_count=len(all_workouts),
        kept_count=len(filtered_workouts),
        ignored_count=ignored_count,
        workouts=filtered_workouts
    )

    print()
    print("=" * 50)

    log("Import terminé")
    log(f"{len(all_workouts)} séances téléchargées")
    log(f"{len(filtered_workouts)} séances conservées")
    log(f"{ignored_count} séances ignorées")

    print("=" * 50)


if __name__ == "__main__":
    main()
