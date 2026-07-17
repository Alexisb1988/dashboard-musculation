from datetime import datetime

# Date minimale des séances conservées
MIN_DATE = datetime(2026, 1, 1)

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
