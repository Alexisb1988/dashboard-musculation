"""
Communication avec l'API Hevy.
"""

import os

import requests

BASE_URL = "https://api.hevyapp.com/v1"

API_KEY = os.getenv("HEVY_API_KEY")

HEADERS = {
    "api-key": API_KEY,
    "accept": "application/json"
}


def get_workouts(page=1, page_size=5):
    """
    Télécharge une page de séances depuis Hevy.
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
