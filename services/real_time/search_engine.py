from collections import deque
from services.real_time.route_engine import expand_state

def search_best_route(initial_state, groups, travel_service):
    """
    אלגוריתם חיפוש ראשי עם:
    - בדיקות חוקיות בסיסיות
    - pruning ראשוני
    """

    queue = deque([initial_state])
    best_state = initial_state

    # מניעת חזרות בסיסית
    visited = {}

    while queue:

        state = queue.popleft()

        key = (
            tuple(state["route"]),
            state["current_meals"]
        )

        # אם כבר ראינו מצב טוב יותר → דילוג
        if key in visited:
            if visited[key] <= state["current_time"]:
                continue

        visited[key] = state["current_time"]

        next_states = expand_state(state, groups, travel_service)

        for new_state in next_states:

            queue.append(new_state)

            # עדכון פתרון מיטבי
            if (
                len(new_state["route"]) > len(best_state["route"])
                or (
                    len(new_state["route"]) == len(best_state["route"])
                    and new_state["current_time"] < best_state["current_time"]
                )
            ):
                best_state = new_state

    return best_state