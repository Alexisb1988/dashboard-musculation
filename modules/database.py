"""
Gestion des fichiers générés.
"""

from datetime import datetime
import json


# ==========================================================
# Sauvegarde JSON
# ==========================================================

import os


def save_json(data, filename):

    filepath = os.path.join("data", filename)

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

# ==========================================================
# Métadonnées
# ==========================================================

def save_metadata(
    downloaded_count,
    kept_count,
    ignored_count,
    workouts
):
    """
    Génère metadata.json.
    """

    if len(workouts) == 0:

        first_workout = None
        last_workout = None

    else:

        dates = sorted(
            workout["start_time"]
            for workout in workouts
        )

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
