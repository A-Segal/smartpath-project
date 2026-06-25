from services.real_time.transition_service import calculate_transition
from services.real_time.constrains import is_valid_transition
from services.real_time.state_engine import create_new_state
from collections import deque

def expand_state(state, groups, travel_service):
    """
    מרחיב מצב לסט מצבים אפשריים,
    תוך סינון מוקדם של אפשרויות לא חוקיות.
    """

    new_states = []

    for group in groups:

        # כבר בוצע במסלול
        if group.id in state["route"]:
            continue

        # חישוב מעבר
        transition = calculate_transition(
            state["current_location"],
            group,
            travel_service
        )

        # סינון מוקדם (חשוב לביצועים)
        if transition is None:
            continue

        # בדיקת אילוצים
        if not is_valid_transition(state, transition):
            continue

        # יצירת מצב חדש
        new_state = create_new_state(state, transition)

        new_states.append(new_state)

    return new_states



def search_best_route(initial_state, groups, travel_service):
    """
    מוצא את המסלול האופטימלי:
    1. מקסימום קבוצות
    2. מינימום זמן
    """

    queue = deque([initial_state])

    best_state = initial_state

    while queue:

        state = queue.popleft()

        next_states = expand_state(state, groups, travel_service)

        for new_state in next_states:

            queue.append(new_state)

            # בדיקת שיפור פתרון
            if (
                len(new_state["route"]) > len(best_state["route"])
                or (
                    len(new_state["route"]) == len(best_state["route"])
                    and new_state["current_time"] < best_state["current_time"]
                )
            ):
                best_state = new_state

    return best_state