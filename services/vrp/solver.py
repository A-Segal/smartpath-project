"""
VRP Solver — Grouped Delivery with Time Constraints

אלגוריתם State Space Search:
- חיפוש מלא על כל סדרי הקבוצות האפשריים
- Pruning: דילוג על מצבים שכבר ראינו בזמן טוב יותר
- מטרה: מקסום מספר deliveries, בתיקו — מינימום זמן
"""

from copy import deepcopy
from services.vrp.vrp_state import (
    create_initial_state,
    is_feasible,
    get_group_families,
    apply_move,
    state_key,
)


def solve(
    groups: list,
    start_location: dict,
    max_capacity: int,
    available_time: float,
    google_maps_service,
) -> dict:
    """
    State Space Search — מוצא את המסלול האופטימלי למתנדב.

    Parameters
    ----------
    groups : list[dict]
        רשימת קבוצות (מבנה מ-build_groups).
    start_location : dict
        מיקום התחלתי {"lat": ..., "lng": ...}.
    max_capacity : int
        קיבולת הרכב (מקס משפחות לקבוצה).
    available_time : float
        זמן פנוי של המתנדב (בדקות).
    google_maps_service : callable
        פונקציית Google Distance Matrix (מקבלת lat1,lng1,lat2,lng2, מחזירה דקות).

    Returns
    -------
    dict : {
        "route": list[center_id],
        "total_deliveries": int,
        "final_time": float,
        "remaining_capacity": int
    }
    """
    if not groups:
        return {
            "route": [],
            "total_deliveries": 0,
            "final_time": 0.0,
            "remaining_capacity": max_capacity,
        }

    state = create_initial_state(start_location, groups, max_capacity, available_time)

    # best_seen[state_key] = best_time — pruning
    best_seen: dict[str, float] = {}

    # overall best
    best_state = deepcopy(state)

    # frontier — רשימת מצבים להרחבה
    frontier = [state]

    while frontier:
        new_frontier = []

        for s in frontier:
            if not s["remaining_groups"]:
                continue

            # בדיקת כל הקבוצות הנותרות
            for group in s["remaining_groups"]:
                # זמן נסיעה
                travel_time = google_maps_service(
                    s["current_location"]["lat"],
                    s["current_location"]["lng"],
                    group["center_lat"],
                    group["center_lng"],
                )

                if travel_time is None or travel_time >= 999:
                    continue

                # בדיקת feasibility
                if not is_feasible(s, group, travel_time):
                    continue

                # יצירת מצב חדש
                ns = apply_move(s, group, travel_time)

                # Pruning — דילוג על מצב שכבר ראינו בזמן טוב יותר
                key = state_key(ns)
                if key in best_seen and best_seen[key] <= ns["current_time"]:
                    continue
                best_seen[key] = ns["current_time"]

                new_frontier.append(ns)

                # בדיקה אם זה המצב הכי טוב
                if ns["total_deliveries"] > best_state["total_deliveries"] or (
                    ns["total_deliveries"] == best_state["total_deliveries"]
                    and ns["current_time"] < best_state["current_time"]
                ):
                    best_state = deepcopy(ns)

        frontier = new_frontier

    return {
        "route": best_state["route"],
        "total_deliveries": best_state["total_deliveries"],
        "final_time": best_state["current_time"],
        "remaining_capacity": max_capacity,
    }
