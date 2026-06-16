

# the func Builds the initial state for the VRP algorithm
def build_initial_state(volunteer, start_location):
    """
    Converts volunteer + DB data into algorithm state.

    Includes:
    - location
    - time limit
    - capacity (vehicle type)
    - empty route
    - empty assigned set
    """

    vehicle_capacity_map = {
        "small": 1,
        "medium": 2,
        "large": 3
    }

    max_meals = vehicle_capacity_map.get(volunteer.vehicle_type, 1)

    return {
        "current_location": start_location,
        "current_time": 0,
        "current_meals": 0,
        "max_time": volunteer.available_time,
        "max_meals": max_meals,
        "route": [],
        "assigned_groups": set()
    }




# the func Orchestrates full VRP flow for a volunteer (DB → algorithm → result)
def run_volunteer_route(volunteer_id, volunteer_repo, group_repo, google_maps_service, search_best_route, build_initial_state):
    """
    Main service entry point that connects DB and VRP engine.
    """

    # 1. load volunteer
    volunteer = volunteer_repo.get_by_id(volunteer_id)

    # 2. load available groups
    groups = group_repo.get_unassigned_groups()

    # 3. start location
    start_location = volunteer.start_location

    # 4. build initial state
    initial_state = build_initial_state(volunteer, start_location)

    # 5. run algorithm
    best_state = search_best_route(
        initial_state,
        groups,
        google_maps_service
    )

    return best_state