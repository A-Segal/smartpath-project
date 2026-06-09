from datetime import date

from db_connection import get_session
from services.batch_algoritm.main_algoritm import run_full_matching
from repository.recipient_request_repository import RecipientRequestRepository
from repository.DS_request_Repository import DSRequestRepository
from repository.distribution_centerRepository import DistributionCenterRepository
from repository.recipientRepository import RecipientRepository
from services.googleMaps import distance_between_points


def test_real_database_matching():
    db = get_session()

    recipient_request_repo = RecipientRequestRepository(db)
    ds_request_repo = DSRequestRepository(db)
    center_repo = DistributionCenterRepository(db)
    recipient_repo = RecipientRepository(db)

    try:
        result = run_full_matching(db)

        print("\n========== MATCHING RESULT ==========\n")

        all_requests = recipient_request_repo.get_all_requests()

        today_requests = [
            request
            for request in all_requests
            if request.request_date.date() == date.today()
        ]

        centers = {
            c.id: c
            for c in center_repo.get_all_distribution_centers()
        }

        recipients = {
            r.id: r
            for r in recipient_repo.get_all_recipients()
        }

        for recipient_id, assignment in sorted(result.items()):

            center_id = assignment["center_id"]
            score = assignment["score"]
            recipient_meals = assignment["recipient_meals"]
            center_meals = assignment["center_meals"]

            recipient_obj = recipients.get(recipient_id)
            center_obj = centers.get(center_id)

            distance = distance_between_points(
                float(center_obj.location_lat),
                float(center_obj.location_lng),
                float(recipient_obj.location_lat),
                float(recipient_obj.location_lng)
            )

            print(
                f"Recipient {recipient_id} "
                f"-> Center {center_id} "
                f"(Score={score:.4f}, Distance={distance:.2f} km) "
                f"| Recipient Meals={recipient_meals} "
                f"| Center Meals={center_meals}"
            )

        print("\n========== STATISTICS ==========\n")

        total_recipients_requested = len(today_requests)
        total_recipients_assigned = len(result)
        total_recipients_not_assigned = (
            total_recipients_requested - total_recipients_assigned
        )

        print(
            f"Recipients requested today: "
            f"{total_recipients_requested}"
        )

        print(
            f"Recipients assigned: "
            f"{total_recipients_assigned}"
        )

        print(
            f"Recipients not assigned: "
            f"{total_recipients_not_assigned}"
        )

        assigned_centers = [
            assignment["center_id"]
            for assignment in result.values()
        ]

        print(
            f"Unique centers used: "
            f"{len(set(assigned_centers))}"
        )

        assert len(result.keys()) == len(set(result.keys()))
        assert len(assigned_centers) == len(set(assigned_centers))

        print("\nNo duplicate recipients: OK")
        print("No duplicate centers: OK")
        print("All validations passed.")

    finally:
        db.close()


if __name__ == "__main__":
    test_real_database_matching()