def create_new_state(state, transition):
    """
    יוצר מצב חדש אחרי מעבר לקבוצת משלוח.
    """

    new_route = state["route"] + [transition["group_id"]]

    new_served = state["served_recipients"].copy()
    new_served.add(transition["recipient_id"])

    return {
        "current_location": transition["end_location"],

        "current_time": state["current_time"] + transition["total_time"],

        "current_meals": state["current_meals"] + transition["group_meals"],

        "max_time": state["max_time"],

        "max_meals": state["max_meals"],

        "route": new_route,

        "visited_groups": state["visited_groups"].union({transition["group_id"]}),

        "served_recipients": new_served
    }