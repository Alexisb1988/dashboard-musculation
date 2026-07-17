"""
Gestion des séances Hevy.
"""

from modules.api import get_workouts
from modules.utils import log


def download_all_workouts():
    """
    Télécharge toutes les séances disponibles
    depuis l'API Hevy.
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
