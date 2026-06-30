def create_initial_state(start_location, groups, max_capacity, available_time):
    return {
        "current_location": start_location,
        "current_time": 0.0,

        "remaining_groups": groups,
        "visited_groups": set(),

        "capacity_left": max_capacity,

        "total_deliveries": 0,

        "route": [],

        "available_time": available_time
    }


def get_group_families(group):
    if "group_families" in group:
        return group["group_families"]

    if "recipients_locations" in group:
        return len(group["recipients_locations"])

    return group.get("total_meals", 0)


def is_feasible(state, group, travel_time, service_time=5):

    new_time = state["current_time"] + travel_time + service_time

    if new_time > state["available_time"]:
        return False

    families = get_group_families(group)

    if families > state["capacity_left"]:
        return False

    if group["center_id"] in state["visited_groups"]:
        return False

    return True