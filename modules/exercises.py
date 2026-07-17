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

    Les exercices officiels sont indexés grâce à leur
    exercise_template_id.

    Les exercices personnalisés sont également conservés et
    indexés grâce à leur nom.
    """

    exercise_index = {}

    for workout in workouts:

        workout_id = workout.get("id")
        workout_date = workout.get("start_time")

        for exercise in workout.get("exercises", []):

            template_id = exercise.get("exercise_template_id")
            title = exercise.get("title")

            # Clé interne unique
            if template_id is not None:
                exercise_key = f"template_{template_id}"
                is_custom = False
            else:
                exercise_key = f"custom_{title}"
                is_custom = True

            if exercise_key not in exercise_index:

                exercise_index[exercise_key] = {
                    "id": exercise_key,
                    "template_id": template_id,
                    "name": title,

                    "is_custom": is_custom,

                    "workout_count": 0,
                    "set_count": 0,

                    "first_seen": workout_date,
                    "last_seen": workout_date,

                    "workout_ids": []
                }

            current = exercise_index[exercise_key]

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

def get_exercise_history(workouts, exercise_id):
    """
    Retourne toutes les occurrences d'un exercice,
    classées par date.
    """

    history = []

    for workout in workouts:

        workout_date = workout.get("start_time")

        for exercise in workout.get("exercises", []):

            template_id = exercise.get("exercise_template_id")
            title = exercise.get("title")

            if template_id is not None:
                current_id = f"template_{template_id}"
            else:
                current_id = f"custom_{title}"

            if current_id != exercise_id:
                continue

            history.append(
                {
                    "date": workout_date,
                    "workout_id": workout.get("id"),
                    "workout_title": workout.get("title"),
                    "exercise_name": title,
                    "sets": exercise.get("sets", [])
                }
            )

    history.sort(key=lambda x: x["date"])

    return history
# ==========================================================
# Statistiques
# ==========================================================

def calculate_exercise_statistics(exercise_index):
    """
    Calcule les statistiques globales de chaque exercice.
    """

    for exercise in exercise_index.values():

        exercise["history_count"] = len(exercise["workout_ids"])

# ==========================================================
# Sauvegarde
# ==========================================================

def save_exercise_database(exercise_index):
    """
    Sauvegarde la base des exercices.
    """

    save_json(
        exercise_index,
        "exercise_database.json"
    )
