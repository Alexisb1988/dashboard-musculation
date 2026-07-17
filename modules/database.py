"""
Gestion des fichiers JSON du projet.
"""

import json
from pathlib import Path


def save_json(data, filename):
    """
    Sauvegarde un objet Python au format JSON.
    """

    Path("data").mkdir(exist_ok=True)

    with open(
        f"data/{filename}",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )
