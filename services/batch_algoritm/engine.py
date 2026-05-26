# ------------------------------------------------------------
# Batch Allocation Engine (Optimized Version)
# תפקיד:
# - חישוב Score חכם לפי מרחק + התאמת ביקוש/קיבולת
# - מניעת התאמות לא יעילות
# - שיבוץ Greedy לפי Score יורד
#
# שיפור מרכזי:
# מרחק לא נחסם אלא נכנס כפקטור ירידה (Decay Function)
# כדי לאפשר פתרון אופטימלי גלובלי
# ------------------------------------------------------------

import math
from collections import defaultdict


def calculate_score(distance_km: float, capacity: int, demand: int):

    # ירידת איכות לפי מרחק (Exponential Decay)
    distance_score = math.exp(-distance_km / 20)

    # התאמת ביקוש לקיבולת
    match_score = min(capacity, demand) / max(capacity, demand)

    # שילוב משוקלל
    return (0.75 * distance_score) + (0.25 * match_score)


def build_batch_allocation(filtered_options: list):

    center_capacity = defaultdict(int)
    recipient_demand = defaultdict(int)

    # ----------------------------
    # אתחול מצב מערכת
    # ----------------------------
    for opt in filtered_options:
        center_capacity[opt["center_id"]] = opt["capacity"]
        recipient_demand[opt["recipient_id"]] = opt["demand"]

    scored_options = []

    # ----------------------------
    # חישוב ציונים
    # ----------------------------
    for opt in filtered_options:

        score = calculate_score(
            opt["distance_km"],
            opt["capacity"],
            opt["demand"]
        )

        scored_options.append({
            "center_id": opt["center_id"],
            "recipient_id": opt["recipient_id"],
            "distance_km": opt["distance_km"],
            "capacity": opt["capacity"],
            "demand": opt["demand"],
            "score": score
        })

    scored_options.sort(key=lambda x: x["score"], reverse=True)

    allocations = []

    # ----------------------------
    # שיבוץ חמדני (Greedy)
    # ----------------------------
    for opt in scored_options:

        c = opt["center_id"]
        r = opt["recipient_id"]

        if center_capacity[c] <= 0 or recipient_demand[r] <= 0:
            continue

        allocated = min(center_capacity[c], recipient_demand[r])

        if allocated <= 0:
            continue

        allocations.append({
            "DistributionCenterID": c,
            "RecipientID": r,
            "amount_of_meals": allocated,
            "distance_km": opt["distance_km"],

            # נתוני מקור (לניתוח CSV)
            "center_requested_meals": opt["capacity"],
            "recipient_requested_meals": opt["demand"]
        })

        center_capacity[c] -= allocated
        recipient_demand[r] -= allocated

    return {
        "allocations": allocations,
        "center_capacity_status": dict(center_capacity),
        "recipient_demand_status": dict(recipient_demand)
    }