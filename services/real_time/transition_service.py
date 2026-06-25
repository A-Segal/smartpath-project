def calculate_transition(current_location, group, travel_service):
    """
    מחשב מעבר בין מיקום נוכחי לקבוצת משלוח.
    """

    travel_result = travel_service(
        current_location.lat,
        current_location.lng,
        group.center.lat,
        group.center.lng
    )

    if not travel_result or "error" in travel_result:
        return None

    travel_time = travel_result["duration_min"]

    service_time = 5  # זמן שירות בסיסי (אפשר לשנות בעתיד)

    return {
        "group_id": group.id,
        "travel_time": travel_time,
        "service_time": service_time,
        "total_time": travel_time + service_time,
        "group_meals": group.amount_of_meals,
        "end_location": group.center,
        "recipient_id": group.RecipientID
    }