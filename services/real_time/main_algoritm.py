from collections import deque
from services.real_time.route_engine import expand_state


# =========================
# VRP Search Engine
# =========================
def search_best_route(initial_state, groups, google_maps_service):
    """
    Finds optimal route:
    1. Max groups served
    2. Min time (tie breaker)
    """

    queue = deque([initial_state])

    best_state = initial_state

    # חשוב: pruning memory
    visited = {}

    while queue:

        state = queue.popleft()

        key = (
            tuple(state["route"]),
            state["current_meals"]
        )

        # pruning: אם ראינו מצב טוב יותר → דלג
        if key in visited:
            if visited[key] <= state["current_time"]:
                continue

        visited[key] = state["current_time"]

        next_states = expand_state(state, groups, google_maps_service)

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