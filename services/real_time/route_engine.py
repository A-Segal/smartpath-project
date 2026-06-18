# =========================
# חישוב מעבר לקבוצה
# =========================
def calculate_transition(current_location, group, google_maps_service):
    """
    מחשב עלות מעבר:
    - זמן נסיעה
    - זמן שירות
    - מספר מנות
    """

    center = group.center

    travel_result = google_maps_service.travel_time_between_points(
        current_location.lat,
        current_location.lng,
        center.lat,
        center.lng
    )

    if "error" in travel_result:
        return None

    travel_time = travel_result["duration_min"]
    distance = travel_result["distance_km"]

    service_time = group.service_time
    meals = group.total_meals

    return {
        "travel_time": travel_time,
        "service_time": service_time,
        "total_time": travel_time + service_time,
        "distance": distance,
        "meals": meals,
        "center_id": center.id
    }


# =========================
# בדיקת חוקיות מעבר
# =========================
def is_valid_transition(state, transition, group):
    """
    בדיקת אילוצים:
    - זמן
    - קיבולת
    - לא נבחר כבר במסלול
    """

    if transition is None:
        return False

    if state["current_time"] + transition["total_time"] > state["max_time"]:
        return False

    if state["current_meals"] + transition["meals"] > state["max_meals"]:
        return False

    if group.id in state["assigned_groups"]:
        return False

    return True


# =========================
# יצירת State חדש
# =========================
def create_new_state(state, group, transition):
    """
    יוצר מצב חדש אחרי הוספת קבוצה למסלול
    """

    return {
        "current_location": group.end_location,
        "current_time": state["current_time"] + transition["total_time"],
        "current_meals": state["current_meals"] + transition["meals"],
        "max_time": state["max_time"],
        "max_meals": state["max_meals"],

        # מסלול קבוצות
        "route": state["route"] + [group.id],

        # מניעת חזרות בתוך אותו מסלול
        "assigned_groups": state["assigned_groups"].copy() | {group.id}
    }


# =========================
# הרחבת מצבים (Core Engine)
# =========================
def expand_state(state, groups, google_maps_service):
    """
    מייצר את כל המצבים האפשריים מהמצב הנוכחי
    """

    new_states = []

    for group in groups:

        if group.id in state["assigned_groups"]:
            continue

        transition = calculate_transition(
            state["current_location"],
            group,
            google_maps_service
        )

        if not is_valid_transition(state, transition, group):
            continue

        new_states.append(
            create_new_state(state, group, transition)
        )

    return new_states


# =========================
# אלגוריתם חיפוש (VRP Solver)
# =========================
def search_best_route(initial_state, groups, google_maps_service):
    """
    מוצא מסלול אופטימלי:
    1. מקסימום קבוצות
    2. זמן מינימלי
    """

    from collections import deque

    queue = deque([initial_state])

    best_state = initial_state

    while queue:

        state = queue.popleft()

        next_states = expand_state(state, groups, google_maps_service)

        for new_state in next_states:

            queue.append(new_state)

            if (
                len(new_state["route"]) > len(best_state["route"])
                or (
                    len(new_state["route"]) == len(best_state["route"])
                    and new_state["current_time"] < best_state["current_time"]
                )
            ):
                best_state = new_state

    return best_state