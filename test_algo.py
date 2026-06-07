# from db_connection import get_session
# from services.batch_algoritm.main_algoritm import run_full_matching
#
#
# def test_real_database_matching():
#     db = get_session()
#
#     try:
#         result = run_full_matching(db)
#
#         print("\n========== MATCHING RESULT ==========\n")
#
#         for recipient_id, (center_id, score) in sorted(result.items()):
#             print(
#                 f"Recipient {recipient_id} "
#                 f"-> Center {center_id} "
#                 f"(Score={score:.4f})"
#             )
#
#         print("\n========== STATISTICS ==========\n")
#
#         print(f"Total assignments: {len(result)}")
#
#         assigned_centers = [
#             center_id
#             for center_id, score in result.values()
#         ]
#
#         print(
#             f"Unique centers used: "
#             f"{len(set(assigned_centers))}"
#         )
#
#         print(
#             f"Unique recipients assigned: "
#             f"{len(result)}"
#         )
#
#         # Validation 1
#         assert len(result.keys()) == len(set(result.keys()))
#
#         # Validation 2
#         assert len(assigned_centers) == len(set(assigned_centers))
#
#         print("\nAll validations passed.")
#
#     finally:
#         db.close()
#
#
# if __name__ == "__main__":
#     test_real_database_matching()


from db_connection import get_session

from services.batch_algoritm.main_algoritm import run_full_matching
from services.googleMaps import distance_between_points

from repository.recipientRepository import RecipientRepository
from repository.distribution_centerRepository import DistributionCenterRepository
from repository.DS_request_Repository import DSRequestRepository
from repository.recipient_request_repository import RecipientRequestRepository


def test_real_database_matching():
    db = get_session()

    try:
        result = run_full_matching(db)

        recipient_repo = RecipientRepository(db)
        center_repo = DistributionCenterRepository(db)
        recipient_request_repo = RecipientRequestRepository(db)
        center_request_repo = DSRequestRepository(db)

        recipients = {
            r.id: r
            for r in recipient_repo.get_all_recipients()
        }

        centers = {
            c.id: c
            for c in center_repo.get_all_distribution_centers()
        }

        recipient_requests = {
            r.RecipientID: r
            for r in recipient_request_repo.get_all_requests()
        }

        center_requests = {
            r.DistributionCenterID: r
            for r in center_request_repo.get_all_requests()
        }

        print("\n========== RAW RESULT ==========")
        print(result)

        print("\n========== ASSIGNMENTS ==========\n")

        for recipient_id, (center_id, score) in sorted(result.items()):

            recipient = recipients.get(recipient_id)
            center = centers.get(center_id)

            if recipient is None:
                print(f"Recipient {recipient_id} not found")
                continue

            if center is None:
                print(f"Center {center_id} not found")
                continue

            distance = distance_between_points(
                float(center.location_lat),
                float(center.location_lng),
                float(recipient.location_lat),
                float(recipient.location_lng)
            )

            recipient_request = recipient_requests.get(
                recipient_id
            )

            center_request = center_requests.get(
                center_id
            )

            recipient_meals = (
                recipient_request.amount_of_meals
                if recipient_request
                else "UNKNOWN"
            )

            center_meals = (
                center_request.amount_of_meals
                if center_request
                else "UNKNOWN"
            )

            print(
                f"Recipient {recipient_id}"
                f" -> Center {center_id}"
            )

            print(
                f"Score: {score:.4f}"
            )

            print(
                f"Distance: {distance:.2f} km"
            )

            print(
                f"Recipient meals: {recipient_meals}"
            )

            print(
                f"Center meals: {center_meals}"
            )

            if (
                isinstance(recipient_meals, int)
                and isinstance(center_meals, int)
            ):
                print(
                    f"Remaining meals: "
                    f"{center_meals - recipient_meals}"
                )

            print("-" * 50)

        print("\n========== STATISTICS ==========\n")

        print(
            f"Total assignments: {len(result)}"
        )

        assigned_centers = [
            center_id
            for center_id, score
            in result.values()
        ]

        print(
            f"Unique centers used: "
            f"{len(set(assigned_centers))}"
        )

        print(
            f"Unique recipients assigned: "
            f"{len(result)}"
        )

        assert len(result) == len(
            set(result.keys())
        )

        assert len(assigned_centers) == len(
            set(assigned_centers)
        )

        print("\nAll validations passed.")

    finally:
        db.close()


if __name__ == "__main__":
    test_real_database_matching()