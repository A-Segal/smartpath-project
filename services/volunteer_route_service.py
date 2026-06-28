from services.vrp.solver import solve
from services.utils.googleMaps import (
    geocode_address,
    travel_time_between_points
)


def run_volunteer_route(
    volunteer_id,
    volunteer_repo,
    assignment_repo,
    google_maps_service,
    start_address=None
):
    # # =========================
    # # 1. GET VOLUNTEER
    # # =========================
    # volunteer = volunteer_repo.get_volunteer(volunteer_id)
    #
    # if not volunteer:
    #     return {"error": "volunteer not found"}
    #
    # # =========================
    # # 2. START LOCATION
    # # =========================
    # if start_address:
    #     geo = geocode_address(start_address)
    #     start_location = {
    #         "lat": geo["lat"],
    #         "lng": geo["lng"]
    #     }
    # else:
    #     start_location = {
    #         "lat": float(volunteer.location_lat),
    #         "lng": float(volunteer.location_lng)
    #     }
    #
    # # =========================
    # # 3. GROUPS
    # # =========================
    # groups = assignment_repo.build_groups()
    #
    # # =========================
    # # 4. VEHICLE CAPACITY
    # # =========================
    # vehicle = getattr(volunteer, "vehicle", None)
    # vehicle_capacity = getattr(vehicle, "capacity", 2)
    #
    # # =========================
    # # 5. AVAILABLE TIME
    # # =========================
    # available_time = getattr(volunteer, "available_time", 999999)
    #
    # # =========================
    # # 6. SOLVER (IMPORTANT FIX)
    # # =========================
    # best_state = solve(
    #     groups=groups,
    #     start_location=start_location,
    #     max_capacity=vehicle_capacity,
    #     available_time=available_time,
    #     google_maps_service=travel_time_between_points
    # )
    #
    # route = best_state.get("route", [])
    #
    # # =========================
    # # 7. ASSIGN TO VOLUNTEER
    # # =========================
    # for g in groups:
    #     if g["center_id"] in route:
    #         for assignment_id in g["assignment_ids"]:
    #             assignment = assignment_repo.get_delivery_assignment(assignment_id)
    #
    #             if assignment and assignment.VolunteerID is None:
    #                 assignment_repo.assign_volunteer_to_group(
    #                     assignment_id,
    #                     volunteer_id
    #                 )
    #
    # # =========================
    # # 8. RESULT
    # # =========================
    # return {
    #     "volunteer_id": volunteer.id,
    #     "start_location":start_location,
    # }

    from services.vrp.solver import solve
    from services.utils.googleMaps import (
        geocode_address,
        travel_time_between_points
    )

    def run_volunteer_route(
            volunteer_id,
            volunteer_repo,
            assignment_repo,
            google_maps_service=None,  # לא חובה עכשיו
            start_address=None
    ):

        print("=== START ROUTE DEBUG ===")

        # =========================
        # 1. GET VOLUNTEER
        # =========================
        volunteer = volunteer_repo.get_volunteer(volunteer_id)

        if not volunteer:
            print("VOLUNTEER NOT FOUND")
            return {"error": "volunteer not found"}

        print("VOLUNTEER OK:", volunteer.id)

        # =========================
        # 2. START LOCATION
        # =========================
        if start_address:
            geo = geocode_address(start_address)
            print("GEOCODE RESULT:", geo)

            if "error" in geo:
                return {"error": "geocode failed", "details": geo}

            start_location = {"lat": geo["lat"], "lng": geo["lng"]}
        else:
            start_location = {
                "lat": float(volunteer.location_lat),
                "lng": float(volunteer.location_lng)
            }

        print("START LOCATION:", start_location)

        # =========================
        # 3. GROUPS
        # =========================
        groups = assignment_repo.build_groups()

        print("GROUPS COUNT:", len(groups))

        if len(groups) == 0:
            return {"error": "no groups built - check assignments"}

        # print sample group
        print("SAMPLE GROUP:", groups[0])

        # =========================
        # 4. VEHICLE
        # =========================
        vehicle = getattr(volunteer, "vehicle", None)
        vehicle_capacity = getattr(vehicle, "capacity", 2)

        print("VEHICLE CAPACITY:", vehicle_capacity)

        # =========================
        # 5. SOLVER
        # =========================
        result = solve(
            groups=groups,
            start_location=start_location,
            max_capacity=vehicle_capacity,
            available_time=999999,
            google_maps_service=travel_time_between_points
        )

        print("SOLVER RESULT:", result)

        if not result:
            return {"error": "solver returned None"}

        route = result.get("route", [])

        print("ROUTE:", route)

        # =========================
        # 6. ASSIGNMENTS
        # =========================
        for g in groups:
            if g["center_id"] in route:
                for assignment_id in g["assignment_ids"]:
                    assignment = assignment_repo.get_delivery_assignment(assignment_id)

                    if assignment and assignment.VolunteerID is None:
                        assignment_repo.assign_volunteer_to_group(
                            assignment_id,
                            volunteer_id
                        )

        # =========================
        # 7. RETURN
        # =========================
        response = {
            "volunteer_id": volunteer.id,
            "start_location": start_location,
            "groups_count": len(groups),
            "route": route,
            "total_meals": result.get("total_meals", 0),
            "visited_count": len(route),
            "vehicle_capacity": vehicle_capacity
        }

        print("FINAL RESPONSE:", response)
        print("=== END ROUTE DEBUG ===")

        return response