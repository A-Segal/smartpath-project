# # ------------------------------------------------------------
# # Batch Allocation Engine (Optimized Version)
# # תפקיד:
# # - חישוב Score חכם לפי מרחק + התאמת ביקוש/קיבולת
# # - מניעת התאמות לא יעילות
# # - שיבוץ Greedy לפי Score יורד
# #
# # שיפור מרכזי:
# # מרחק לא נחסם אלא נכנס כפקטור ירידה (Decay Function)
# # כדי לאפשר פתרון אופטימלי גלובלי
# # ------------------------------------------------------------
#
# import math
# from collections import defaultdict
#
#
# def calculate_score(distance_km: float, capacity: int, demand: int):
#
#     # ירידת איכות לפי מרחק (Exponential Decay)
#     distance_score = math.exp(-distance_km / 20)
#
#     # התאמת ביקוש לקיבולת
#     match_score = min(capacity, demand) / max(capacity, demand)
#
#     # שילוב משוקלל
#     return (0.75 * distance_score) + (0.25 * match_score)
#
#
# def build_batch_allocation(filtered_options: list):
#
#     center_capacity = defaultdict(int)
#     recipient_demand = defaultdict(int)
#
#     # ----------------------------
#     # אתחול מצב מערכת
#     # ----------------------------
#     for opt in filtered_options:
#         center_capacity[opt["center_id"]] = opt["capacity"]
#         recipient_demand[opt["recipient_id"]] = opt["demand"]
#
#     scored_options = []
#
#     # ----------------------------
#     # חישוב ציונים
#     # ----------------------------
#     for opt in filtered_options:
#
#         score = calculate_score(
#             opt["distance_km"],
#             opt["capacity"],
#             opt["demand"]
#         )
#
#         scored_options.append({
#             "center_id": opt["center_id"],
#             "recipient_id": opt["recipient_id"],
#             "distance_km": opt["distance_km"],
#             "capacity": opt["capacity"],
#             "demand": opt["demand"],
#             "score": score
#         })
#
#     scored_options.sort(key=lambda x: x["score"], reverse=True)
#
#     allocations = []
#
#     # ----------------------------
#     # שיבוץ חמדני (Greedy)
#     # ----------------------------
#     for opt in scored_options:
#
#         c = opt["center_id"]
#         r = opt["recipient_id"]
#
#         if center_capacity[c] <= 0 or recipient_demand[r] <= 0:
#             continue
#
#         allocated = min(center_capacity[c], recipient_demand[r])
#
#         if allocated <= 0:
#             continue
#
#         allocations.append({
#             "DistributionCenterID": c,
#             "RecipientID": r,
#             "amount_of_meals": allocated,
#             "distance_km": opt["distance_km"],
#
#             # נתוני מקור (לניתוח CSV)
#             "center_requested_meals": opt["capacity"],
#             "recipient_requested_meals": opt["demand"]
#         })
#
#         center_capacity[c] -= allocated
#         recipient_demand[r] -= allocated
#
#     return {
#         "allocations": allocations,
#         "center_capacity_status": dict(center_capacity),
#         "recipient_demand_status": dict(recipient_demand)
#     }









# ------------------------------------------------------------
# Batch Allocation Engine (GEOGRAPHIC CLUSTER OPTIMIZED)
# ------------------------------------------------------------
# תפקיד:
# מנוע שיבוץ Batch מתקדם עם אופטימיזציה גיאוגרפית אמיתית
#
# מטרות:
# ✅ מקסימום נזקקים שמקבלים מענה
# ✅ ללא כפילות recipients
# ✅ ללא חריגה מקיבולת centers
# ✅ ללא partial allocation
# ✅ צמצום מרחקים
# ✅ clustering אמיתי בין recipients
# ✅ Dynamic Greedy Recalculation
#
# שיפור מרכזי:
# Center יכול לשרת כמה recipients
# רק אם recipients קרובים אחד לשני
#
# חוק:
# Recipient נוסף חייב להיות עד 3KM
# מכל recipient שכבר שובץ לאותו center
#
# דרישות:
# filter_all_divides_by_mealAccount
# חייב להחזיר:
#
# recipient_lat
# recipient_lng
#
# ------------------------------------------------------------

import math
from collections import defaultdict

from services.googleMaps import distance_between_points


# ------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------

MAX_CENTER_DISTANCE_KM = 30

MAX_RECIPIENT_CLUSTER_DISTANCE_KM = 3


# ------------------------------------------------------------
# DISTANCE SCORE
# ------------------------------------------------------------

def calculate_distance_score(distance_km):

    if distance_km > MAX_CENTER_DISTANCE_KM:
        return 0

    return 1 / (
        1 + (distance_km ** 1.7)
    )


# ------------------------------------------------------------
# SCORE FUNCTION
# ------------------------------------------------------------

def calculate_score(
    distance_km,
    capacity,
    demand,
    recipient_served_before
):

    if distance_km > MAX_CENTER_DISTANCE_KM:
        return -1

    # -----------------------------
    # DISTANCE
    # -----------------------------
    distance_score = calculate_distance_score(
        distance_km
    )

    # -----------------------------
    # CAPACITY MATCH
    # -----------------------------
    capacity_score = (
        demand / capacity
    )

    # -----------------------------
    # FULL COVER
    # -----------------------------
    full_cover_bonus = 1

    # -----------------------------
    # FIRST RECIPIENT BONUS
    # -----------------------------
    first_bonus = (
        0 if recipient_served_before else 1
    )

    # -----------------------------
    # FINAL SCORE
    # -----------------------------
    score = (
        (0.50 * distance_score) +
        (0.25 * capacity_score) +
        (0.15 * full_cover_bonus) +
        (0.10 * first_bonus)
    )

    return score


# ------------------------------------------------------------
# CHECK RECIPIENT CLUSTER
# ------------------------------------------------------------

def recipient_fits_cluster(
    existing_recipients,
    new_recipient
):

    # center עדיין ריק
    if not existing_recipients:
        return True

    new_lat = new_recipient["recipient_lat"]
    new_lng = new_recipient["recipient_lng"]

    for r in existing_recipients:

        dist = distance_between_points(
            r["recipient_lat"],
            r["recipient_lng"],
            new_lat,
            new_lng
        )

        if dist > MAX_RECIPIENT_CLUSTER_DISTANCE_KM:
            return False

    return True


# ------------------------------------------------------------
# MAIN ENGINE
# ------------------------------------------------------------

def build_batch_allocation(filtered_options):

    # --------------------------------------------------------
    # STATE
    # --------------------------------------------------------

    center_capacity = {}

    recipient_demand = {}

    assigned_recipients = set()

    center_recipients = defaultdict(list)

    allocations = []

    # --------------------------------------------------------
    # INIT STATE
    # --------------------------------------------------------

    for opt in filtered_options:

        center_capacity[
            opt["center_id"]
        ] = opt["capacity"]

        recipient_demand[
            opt["recipient_id"]
        ] = opt["demand"]

    # --------------------------------------------------------
    # DYNAMIC GREEDY LOOP
    # --------------------------------------------------------

    while True:

        best_option = None

        best_score = -1

        # ----------------------------------------------------
        # RECALCULATE EVERYTHING
        # ----------------------------------------------------

        for opt in filtered_options:

            c = opt["center_id"]

            r = opt["recipient_id"]

            distance = opt["distance_km"]

            demand = opt["demand"]

            capacity = center_capacity[c]

            # --------------------------------------------
            # recipient already assigned
            # --------------------------------------------
            if r in assigned_recipients:
                continue

            # --------------------------------------------
            # invalid states
            # --------------------------------------------
            if capacity <= 0:
                continue

            if demand <= 0:
                continue

            # --------------------------------------------
            # no partial allocation
            # --------------------------------------------
            if capacity < demand:
                continue

            # --------------------------------------------
            # distance hard limit
            # --------------------------------------------
            if distance > MAX_CENTER_DISTANCE_KM:
                continue

            # --------------------------------------------
            # geographic cluster validation
            # --------------------------------------------
            fits_cluster = recipient_fits_cluster(
                center_recipients[c],
                opt
            )

            if not fits_cluster:
                continue

            # --------------------------------------------
            # calculate score
            # --------------------------------------------
            score = calculate_score(
                distance,
                capacity,
                demand,
                r in assigned_recipients
            )

            if score > best_score:

                best_score = score

                best_option = opt

        # ----------------------------------------------------
        # NO MORE VALID OPTIONS
        # ----------------------------------------------------

        if best_option is None:
            break

        # ----------------------------------------------------
        # EXECUTE ALLOCATION
        # ----------------------------------------------------

        c = best_option["center_id"]

        r = best_option["recipient_id"]

        meals = best_option["demand"]

        allocations.append({

            "DistributionCenterID": c,

            "RecipientID": r,

            "amount_of_meals": meals,

            "distance_km": round(
                best_option["distance_km"],
                2
            ),

            "score": round(
                best_score,
                4
            ),

            "center_requested_meals":
                best_option["capacity"],

            "recipient_requested_meals":
                meals
        })

        # ----------------------------------------------------
        # UPDATE STATE
        # ----------------------------------------------------

        center_capacity[c] -= meals

        recipient_demand[r] = 0

        assigned_recipients.add(r)

        center_recipients[c].append({

            "recipient_id": r,

            "recipient_lat":
                best_option["recipient_lat"],

            "recipient_lng":
                best_option["recipient_lng"]
        })

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    return {

        "allocations": allocations,

        "center_capacity_status":
            dict(center_capacity),

        "recipient_demand_status":
            dict(recipient_demand),

        "total_recipients_served":
            len(assigned_recipients),

        "total_allocations":
            len(allocations)
    }

