# def solve(
#     groups,
#     start_location,
#     max_capacity,
#     available_time,
#     google_maps_service
# ):
#
#     current_time = 0
#     current_location = start_location
#
#     route = []
#     visited = set()
#     total_meals = 0
#
#     remaining_groups = groups.copy()
#
#     while True:
#
#         best_group = None
#         best_travel_time = None
#
#         for g in remaining_groups:
#
#             if g["center_id"] in visited:
#                 continue
#
#             if g["total_meals"] > max_capacity:
#                 continue
#
#             result = google_maps_service(
#                 current_location["lat"],
#                 current_location["lng"],
#                 g["center_lat"],
#                 g["center_lng"]
#             )
#
#             if isinstance(result, dict):
#                 travel_time = result.get("duration_min", 0)
#             else:
#                 travel_time = result
#
#             service_time = 5
#             new_time = current_time + travel_time + service_time
#
#             if new_time > available_time:
#                 continue
#
#             if best_group is None or travel_time < best_travel_time:
#                 best_group = g
#                 best_travel_time = travel_time
#
#         if not best_group:
#             break
#
#         route.append(best_group["center_id"])
#         visited.add(best_group["center_id"])
#
#         current_time += best_travel_time + 5
#
#         current_location = {
#             "lat": best_group["center_lat"],
#             "lng": best_group["center_lng"]
#         }
#
#         total_meals += best_group["total_meals"]
#         max_capacity -= best_group["total_meals"]
#
#         remaining_groups.remove(best_group)
#
#     return {
#         "route": route,
#         "visited_count": len(route),
#         "total_meals": total_meals,
#         "final_time": current_time,
#         "remaining_capacity": max_capacity
#     }

def solve(
    groups,
    start_location,
    max_capacity,
    available_time,
    google_maps_service
):

    print("=== SOLVE START ===")

    current_time = 0
    current_location = start_location

    route = []
    visited = set()
    total_meals = 0

    remaining_groups = groups.copy()

    print("GROUPS IN SOLVE:", len(groups))

    while True:

        best_group = None
        best_travel_time = None

        for g in remaining_groups:

            print("CHECK GROUP:", g["center_id"])

            if g["center_id"] in visited:
                continue

            # if g["total_meals"] > max_capacity:
            #     continue

            result = google_maps_service(
                current_location["lat"],
                current_location["lng"],
                g["center_lat"],
                g["center_lng"]
            )

            print("MAP RESULT:", result)

            if isinstance(result, dict):
                travel_time = result.get("duration_min", 0)
            else:
                travel_time = result

            if travel_time is None:
                continue

            new_time = current_time + travel_time + 5

            if new_time > available_time:
                continue

            if best_group is None or travel_time < best_travel_time:
                best_group = g
                best_travel_time = travel_time

        if not best_group:
            break

        route.append(best_group["center_id"])
        visited.add(best_group["center_id"])

        current_time += best_travel_time + 5

        current_location = {
            "lat": best_group["center_lat"],
            "lng": best_group["center_lng"]
        }

        total_meals += best_group["total_meals"]
        max_capacity -= best_group["total_meals"]

        remaining_groups.remove(best_group)

    print("=== SOLVE END ===")

    return {
        "route": route,
        "groups_count": len(route),
        "total_meals": total_meals,
        "final_time": current_time,
        "remaining_capacity": max_capacity
    }