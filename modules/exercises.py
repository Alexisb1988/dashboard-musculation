"""
Gestion des exercices.
"""

from modules.database import save_json


# ==========================================================
# Construction de l'index des exercices
# ==========================================================

def build_exercise_index(workouts):
    """
    Construit un index des exercices présents dans les séances.
    """

    exercise_index = {}

    for workout in workouts:

        workout_id = workout.get("id")
        workout_date = workout.get("start_time")

        for exercise in workout.get("exercises", []):

            template_id = exercise.get("exercise_template_id")

            if template_id is None:
                continue

            if template_id not in exercise_index:

                exercise_index[template_id] = {
                    "template_id": template_id,
                    "name": exercise.get("title"),
                    "workout_count": 0,
                    "set_count": 0,
                    "first_seen": workout_date,
                    "last_seen": workout_date,
                    "workout_ids": []
                }

            current = exercise_index[template_id]

            current["workout_count"] += 1
            current["set_count"] += len(exercise.get("sets", []))

            if workout_date < current["first_seen"]:
                current["first_seen"] = workout_date

            if workout_date > current["last_seen"]:
                current["last_seen"] = workout_date

            current["workout_ids"].append(workout_id)

    return exercise_index


# ==========================================================
# Historique
# ==========================================================

def get_exercise_history(workouts, template_id):

    history = []

    for workout in workouts:

        workout_date = workout.get("start_time")

        for exercise in workout.get("exercises", []):

            if exercise.get("exercise_template_id") != template_id:
                continue

            history.append(
                {
                    "date": workout_date,
                    "workout_id": workout.get("id"),
                    "workout_title": workout.get("title"),
                    "exercise_name": exercise.get("title"),
                    "sets": exercise.get("sets", [])
                }
            )

    history.sort(key=lambda x: x["date"])

    return history


# ==========================================================
# Sauvegarde
# ==========================================================

def save_exercise_database(exercise_index):

    save_json(
        exercise_index,
        "exercise_database.json"
    )
