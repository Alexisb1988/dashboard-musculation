"""
Calcul des statistiques globales.
"""


def calculate_global_statistics(workouts):
    """
    Calcule les statistiques globales des séances.
    """

    statistics = {
        "workout_count": 0,
        "exercise_count": 0,
        "set_count": 0,
        "rep_count": 0,
        "total_volume": 0,

        "first_workout": None,
        "last_workout": None,
    }

    for workout in workouts:

        statistics["workout_count"] += 1

        workout_date = workout.get("start_time")

        if (
            statistics["first_workout"] is None
            or workout_date < statistics["first_workout"]
        ):
            statistics["first_workout"] = workout_date

        if (
            statistics["last_workout"] is None
            or workout_date > statistics["last_workout"]
        ):
            statistics["last_workout"] = workout_date

        for exercise in workout.get("exercises", []):

            statistics["exercise_count"] += 1

            for current_set in exercise.get("sets", []):

                statistics["set_count"] += 1

                reps = current_set.get("reps") or 0
                weight = current_set.get("weight_kg") or 0

                statistics["rep_count"] += reps
                statistics["total_volume"] += reps * weight

    return statistics
