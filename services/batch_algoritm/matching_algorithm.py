from repository.distribution_centerRepository import DistributionCenterRepository
from repository.recipientRepository import RecipientRepository
from repository.DS_request_Repository import DSRequestRepository
from repository.recipient_request_repository import RecipientRequestRepository
from services.googleMaps import distance_between_points




#the func get the params and return the score
def calculate_match_score(
    center_meals: int,
    recipient_meals: int,
    distance: float
) -> float:
    """
    Calculate match score.

    Lower score = better match.
    """

    distance_ratio = distance / 100

    remaining_meals_ratio = (
        center_meals - recipient_meals
    ) / center_meals

    score = (
        distance_ratio * 0.8
        +
        remaining_meals_ratio * 0.2
    )

    return score


#the func create Dictionary of the filter meals and max dist that the key:CenterID and the value is: not sort list of object :(RecipientID, Score)
def build_candidates_for_centers(db):
    """
    Dictionary<
        CenterID,
        List<
            (
                RecipientID,
                Score,
                RecipientMeals,
                CenterMeals
            )
        >
    >
    """

    center_repo = DistributionCenterRepository(db)
    recipient_repo = RecipientRepository(db)
    ds_request_repo = DSRequestRepository(db)
    recipient_request_repo = RecipientRequestRepository(db)

    centers = center_repo.get_all_distribution_centers()
    recipients = recipient_repo.get_all_recipients()

    center_requests = ds_request_repo.get_all_requests()
    recipient_requests = recipient_request_repo.get_all_requests()

    center_requests_dict = {
        request.DistributionCenterID: request
        for request in center_requests
    }

    recipient_requests_dict = {
        request.RecipientID: request
        for request in recipient_requests
    }

    candidates_by_center = {}

    for center in centers:

        candidates_by_center[center.id] = []

        center_request = center_requests_dict.get(center.id)

        if center_request is None:
            continue

        center_meals = center_request.amount_of_meals

        for recipient in recipients:

            recipient_request = recipient_requests_dict.get(
                recipient.id
            )

            if recipient_request is None:
                continue

            recipient_meals = (
                recipient_request.amount_of_meals
            )

            if recipient_meals > center_meals:
                continue

            distance = distance_between_points(
                float(center.location_lat),
                float(center.location_lng),
                float(recipient.location_lat),
                float(recipient.location_lng)
            )

            if distance > 100:
                continue

            score = calculate_match_score(
                center_meals=center_meals,
                recipient_meals=recipient_meals,
                distance=distance
            )

            candidates_by_center[center.id].append(
                (
                    recipient.id,
                    score,
                    recipient_meals,
                    center_meals
                )
            )

    return candidates_by_center

#the func get the all candidates_by_center and sort to every center their list.
def sort_center_candidates(candidates_by_center):
    """
    Sort each center's candidates list by score (ascending).
    Lower score = better match.
    """

    for center_id, candidates in candidates_by_center.items():

        # sort only this center's list
        candidates.sort(key=lambda x: x[1])

    return candidates_by_center