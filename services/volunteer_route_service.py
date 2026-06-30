from services.vrp.solver import solve
from services.utils.googleMaps import (
    geocode_address,
    travel_time_between_points
)


def get_capacity(vehicle_type):
    return {
        1: 1,
        2: 3,
        3: 6,
        4: 10,
        5: 20
    }.get(vehicle_type, 3)


# =========================
# FLATTEN ROUTE FOR REACT
# =========================
def build_detailed_route(route, groups, start_location):
    group_map = {g["center_id"]: g for g in groups}

    full_route = []

    # START POINT
    full_route.append({
        "step": 0,
        "type": "start",
        "center_id": None,
        "assignment_id": None,
        "lat": start_location["lat"],
        "lng": start_location["lng"]
    })

    step = 1

    for center_id in route:
        group = group_map.get(center_id)
        if not group:
            continue

        # CENTER
        full_route.append({
            "step": step,
            "type": "center",
            "center_id": center_id,
            "assignment_id": None,
            "lat": group["center_lat"],
            "lng": group["center_lng"]
        })
        step += 1

        # RECIPIENTS (ordered inside group)
        for aid, loc in zip(
            group.get("assignment_ids", []),
            group.get("recipients_locations", [])
        ):
            full_route.append({
                "step": step,
                "type": "recipient",
                "center_id": center_id,
                "assignment_id": aid,
                "lat": loc["lat"],
                "lng": loc["lng"]
            })
            step += 1

    return full_route


# =========================
# MAIN SERVICE
# =========================
def run_volunteer_route(
    volunteer_id,
    volunteer_repo,
    assignment_repo,
    google_maps_service=None,
    start_address=None
):

    print("=== START ROUTE DEBUG ===")

    # 1. VOLUNTEER
    volunteer = volunteer_repo.get_volunteer(volunteer_id)
    if not volunteer:
        return {"error": "volunteer not found"}

    # 2. START LOCATION
    if start_address:
        geo = geocode_address(start_address)
        if not geo or "error" in geo:
            return {"error": "geocode failed", "details": geo}

        start_location = {"lat": geo["lat"], "lng": geo["lng"]}
    else:
        start_location = {
            "lat": float(volunteer.location_lat),
            "lng": float(volunteer.location_lng)
        }

    # 3. GROUPS
    groups = assignment_repo.build_groups()

    groups = [
        g for g in groups
        if isinstance(g, dict)
        and g.get("center_id")
        and g.get("center_lat")
        and g.get("center_lng")
    ]

    if not groups:
        return {
            "volunteer_id": volunteer.id,
            "start_location": start_location,
            "route": [],
            "detailed_route": [],
            "message": "no groups available"
        }

    # 4. VEHICLE CAPACITY
    vehicle = getattr(volunteer, "vehicle", None)
    vehicle_type = getattr(vehicle, "type", 3)
    vehicle_capacity = get_capacity(vehicle_type)

    # 5. SOLVER
    result = solve(
        groups=groups,
        start_location=start_location,
        max_capacity=vehicle_capacity,
        available_time=999999,
        google_maps_service=travel_time_between_points
    )

    if not result:
        return {"error": "solver failed"}

    route = result.get("route", [])

    if not route:
        return {
            "volunteer_id": volunteer.id,
            "start_location": start_location,
            "route": [],
            "detailed_route": [],
            "message": "no feasible route found"
        }

    # 6. BUILD UI ROUTE
    detailed_route = build_detailed_route(route, groups, start_location)

    # 7. ASSIGNMENTS
    for g in groups:
        if g["center_id"] in route:
            for assignment_id in g.get("assignment_ids", []):
                assignment = assignment_repo.get_delivery_assignment(assignment_id)
                if assignment and assignment.VolunteerID is None:
                    assignment_repo.assign_volunteer_to_group(
                        assignment_id,
                        volunteer_id
                    )

    # 8. RESPONSE
    return {
        "volunteer_id": volunteer.id,
        "start_location": start_location,
        "route": route,
        "detailed_route": detailed_route,
        "groups_count": len(groups),
        "vehicle_capacity": vehicle_capacity,
        "total_meals": result.get("total_meals", 0),
        "visited_count": len(route)
    }



# from services.vrp.solver import solve
# from services.utils.googleMaps import (
#     geocode_address,
#     travel_time_between_points
# )
#
#
# # =========================
# # VEHICLE CAPACITY MAP
# # =========================
# def get_capacity(vehicle_type):
#     return {
#         1: 1,
#         2: 3,
#         3: 6,
#         4: 10,
#         5: 20
#     }.get(vehicle_type, 3)
#
#
# # =========================
# # NORMALIZE GROUPS
# # =========================
# def normalize_groups(groups):
#     clean = []
#
#     for g in groups:
#         if not isinstance(g, dict):
#             continue
#         if not g.get("center_id"):
#             continue
#
#         recipients = g.get("recipients_locations", [])
#
#         g["group_families"] = len(recipients)
#
#         if "total_meals" not in g or g["total_meals"] == 0:
#             g["total_meals"] = g["group_families"]
#
#         clean.append(g)
#
#     return clean
#
#
# # =========================
# # BUILD DETAILED ROUTE
# # =========================
# def build_detailed_route(route, groups, start_location):
#     group_map = {g["center_id"]: g for g in groups}
#
#     detailed = []
#
#     # start node
#     detailed.append({
#         "step": 0,
#         "type": "start",
#         "center_id": None,
#         "assignment_id": None,
#         "lat": start_location["lat"],
#         "lng": start_location["lng"]
#     })
#
#     step = 1
#
#     for center_id in route:
#         g = group_map.get(center_id)
#         if not g:
#             continue
#
#         # center step
#         detailed.append({
#             "step": step,
#             "type": "center",
#             "center_id": center_id,
#             "assignment_id": None,
#             "lat": g["center_lat"],
#             "lng": g["center_lng"]
#         })
#         step += 1
#
#         # recipients steps
#         for aid, loc in zip(
#             g.get("assignment_ids", []),
#             g.get("recipients_locations", [])
#         ):
#             detailed.append({
#                 "step": step,
#                 "type": "recipient",
#                 "center_id": center_id,
#                 "assignment_id": aid,
#                 "lat": loc["lat"],
#                 "lng": loc["lng"]
#             })
#             step += 1
#
#     return detailed
#
#
# # =========================
# # MAIN SERVICE
# # =========================
# def run_volunteer_route(
#     volunteer_id,
#     volunteer_repo,
#     assignment_repo,
#     google_maps_service=None,
#     start_address=None
# ):
#
#     print("=== ROUTE SERVICE START ===")
#
#     # 1. volunteer
#     volunteer = volunteer_repo.get_volunteer(volunteer_id)
#     if not volunteer:
#         return {"error": "volunteer not found"}
#
#     # 2. start location
#     if start_address:
#         geo = geocode_address(start_address)
#         if not geo or "error" in geo:
#             return {"error": "geocode failed"}
#         start_location = {"lat": geo["lat"], "lng": geo["lng"]}
#     else:
#         start_location = {
#             "lat": float(volunteer.location_lat),
#             "lng": float(volunteer.location_lng)
#         }
#
#     # 3. groups
#     groups = assignment_repo.build_groups()
#     groups = normalize_groups(groups)
#
#     if not groups:
#         return {"error": "no groups"}
#
#     print("GROUPS:", len(groups))
#
#     # 4. capacity
#     vehicle = getattr(volunteer, "vehicle", None)
#     vehicle_type = getattr(vehicle, "type", 3)
#     capacity = get_capacity(vehicle_type)
#
#     print("CAPACITY:", capacity)
#
#     # 5. solve
#     result = solve(
#         groups=groups,
#         start_location=start_location,
#         max_capacity=capacity,
#         available_time=999999,
#         google_maps_service=travel_time_between_points
#     )
#
#     route = result.get("route", [])
#
#     # fallback
#     if not route:
#         return {
#             "volunteer_id": volunteer.id,
#             "start_location": start_location,
#             "route": [],
#             "detailed_route": [],
#             "message": "no feasible route found"
#         }
#
#     # 6. detailed route (FOR REACT / GOOGLE MAPS)
#     detailed_route = build_detailed_route(route, groups, start_location)
#
#     # 7. assign to DB
#     for g in groups:
#         if g["center_id"] in route:
#             for aid in g.get("assignment_ids", []):
#                 assignment = assignment_repo.get_delivery_assignment(aid)
#                 if assignment and assignment.VolunteerID is None:
#                     assignment_repo.assign_volunteer_to_group(aid, volunteer_id)
#
#     # 8. response
#     return {
#         "volunteer_id": volunteer.id,
#         "start_location": start_location,
#         "groups_count": len(groups),
#         "route": route,
#         "detailed_route": detailed_route,
#         "total_meals": result.get("total_deliveries", 0),
#         "visited_count": len(route),
#         "vehicle_capacity": capacity,
#         "final_time": result.get("final_time", 0)
#     }