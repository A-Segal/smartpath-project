from db_connection import get_session
from repository.delivery_assignmentRepository import DeliveryAssignmentRepository
from services.batch_algoritm.execute_full_matching import execute_full_matching


def create_assignments_from_matching():

    assignments = execute_full_matching()

    db = get_session()

    try:

        repo = DeliveryAssignmentRepository(db)

        created_count = 0

        for recipient_id, assignment in assignments.items():

            repo.create_delivery_assignment(
                DistributionCenterID=assignment["center_id"],
                RecipientID=recipient_id,
                VolunteerID=None,
                amount_of_meals=assignment["recipient_meals"],
                freshness_priority=assignment.get("freshness_priority", 0)

            )

            created_count += 1

        return created_count

    finally:
        db.close()