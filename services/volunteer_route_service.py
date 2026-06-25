from services.volunteer_route_service import (
    build_initial_state,
    assign_route_to_volunteer
)
from services.real_time.route_engine import search_best_route

def run_volunteer_route(
    volunteer_id,
    volunteer_repo,
    group_repo,
    google_maps_service
):
    """
    מריץ את אלגוריתם VRP ומחזיר מסלול סופי.
    """

    volunteer = volunteer_repo.get_by_id(volunteer_id)

    groups = group_repo.get_unassigned_groups()

    initial_state = build_initial_state(
        volunteer,
        volunteer.start_location
    )

    best_state = search_best_route(
        initial_state,
        groups,
        google_maps_service
    )

    assign_route_to_volunteer(
        best_state,
        volunteer_id,
        group_repo
    )

    return best_state