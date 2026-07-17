"""
Dashboard Musculation
Version : 0.2.1

Cette version :
- récupère toutes les pages Hevy
- fusionne toutes les séances
- sauvegarde un JSON unique

La prochaine étape filtrera les séances avant le 01/01/2026.
"""


import math
from datetime import datetime

from modules.api import get_workouts
from modules.utils import log
from modules.workouts import download_all_workouts
from modules.database import save_json
from modules.filter import filter_workouts

from modules.exercises import (
    build_exercise_index,
    get_exercise_history,
    save_exercise_database
)

# ==========================================================
# Configuration
# ==========================================================

# Date minimale des séances conservées
MIN_DATE = datetime(2026, 1, 1)

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
# Programme principal
# ==========================================================
    
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

    # ==========================================================
    # Construction de l'index des exercices
    # ==========================================================

    exercise_index = build_exercise_index(
        filtered_workouts
    )

    save_exercise_database(
        exercise_index
    )

    log(f"{len(exercise_index)} exercices uniques détectés")
    log("exercise_database.json généré")

    print()
    print("===== Liste des exercices =====")

    for exercise in sorted(
        exercise_index.values(),
        key=lambda x: x["name"]
    ):
        print(
            f'{exercise["name"]:<45} {exercise["workout_count"]:>3} séances'
        )

    print("===============================")

    print()
    print("=" * 50)

    log("Import terminé")
    log(f"{len(all_workouts)} séances téléchargées")
    log(f"{len(filtered_workouts)} séances conservées")
    log(f"{ignored_count} séances ignorées")

    print("=" * 50)



if __name__ == "__main__":
    main()
