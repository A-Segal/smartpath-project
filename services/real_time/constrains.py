def is_valid_transition(state, transition):
    """
    בודק אם מעבר בין קבוצות מותר לפי אילוצי VRP:
    - זמן
    - קיבולת
    - מניעת כפילות נזקקים
    """

    if transition is None:
        return False

    # זמן
    if state["current_time"] + transition["total_time"] > state["max_time"]:
        return False

    # קיבולת
    if state["current_meals"] + transition["group_meals"] > state["max_meals"]:
        return False

    # מניעת כפילות recipients
    served = state.get("served_recipients", set())

    recipient_id = transition.get("recipient_id")

    if recipient_id is not None and recipient_id in served:
        return False

    return True