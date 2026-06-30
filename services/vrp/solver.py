from copy import deepcopy
from services.vrp.vrp_state import create_initial_state, is_feasible, get_group_families


MAX_ITERATIONS = 50   # הורדתי כדי שלא יתקע
MAX_BRANCH = 3


def solve(groups, start_location, max_capacity, available_time, google_maps_service):

    print("=== SOLVER START ===")
    print("GROUPS RECEIVED:", len(groups))
    print("START:", start_location)
    print("CAPACITY:", max_capacity)
    print("TIME LIMIT:", available_time)

    state = create_initial_state(
        start_location,
        groups,
        max_capacity,
        available_time
    )

    best_state = deepcopy(state)

    frontier = [state]
    iterations = 0

    while frontier:

        iterations += 1
        print("\n=== ITERATION ===", iterations)

        if iterations > MAX_ITERATIONS:
            print("STOP: MAX ITERATIONS")
            break

        new_frontier = []

        for s in frontier:

            print("\nCURRENT STATE:")
            print("location:", s["current_location"])
            print("time:", s["current_time"])
            print("capacity:", s["capacity_left"])
            print("remaining:", len(s["remaining_groups"]))

            if not s["remaining_groups"]:
                print("NO GROUPS LEFT")
                continue

            candidates = s["remaining_groups"][:MAX_BRANCH]

            for group in candidates:

                print("\nCHECK GROUP:", group["center_id"])
                families = get_group_families(group)
                print("families:", families)

                travel_time = google_maps_service(
                    s["current_location"]["lat"],
                    s["current_location"]["lng"],
                    group["center_lat"],
                    group["center_lng"]
                )

                print("travel_time:", travel_time)

                if travel_time is None:
                    print("SKIP: travel None")
                    continue

                # FEASIBILITY DEBUG
                feasible = is_feasible(s, group, travel_time)
                print("feasible:", feasible)

                if not feasible:
                    continue

                ns = deepcopy(s)

                ns["current_time"] += travel_time + 5
                ns["current_location"] = {
                    "lat": group["center_lat"],
                    "lng": group["center_lng"]
                }

                ns["route"].append(group["center_id"])
                ns["visited_groups"].add(group["center_id"])

                ns["capacity_left"] -= families
                ns["total_deliveries"] += families

                ns["remaining_groups"] = [
                    g for g in s["remaining_groups"]
                    if g["center_id"] != group["center_id"]
                ]

                print(">>> GROUP ADDED")

                new_frontier.append(ns)

                if (
                    ns["total_deliveries"] > best_state["total_deliveries"]
                    or (
                        ns["total_deliveries"] == best_state["total_deliveries"]
                        and ns["current_time"] < best_state["current_time"]
                    )
                ):
                    best_state = deepcopy(ns)
                    print(">>> NEW BEST STATE")

        frontier = new_frontier

        print("NEXT FRONTIER SIZE:", len(frontier))

    print("\n=== SOLVER END ===")
    print("BEST ROUTE:", best_state["route"])
    print("TOTAL:", best_state["total_deliveries"])
    print("TIME:", best_state["current_time"])

    return {
        "route": best_state["route"],
        "total_deliveries": best_state["total_deliveries"],
        "final_time": best_state["current_time"],
        "remaining_capacity": best_state["capacity_left"]
    }