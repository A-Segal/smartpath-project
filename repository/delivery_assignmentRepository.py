from sqlalchemy.orm import Session
from models.delivery_assignment import DeliveryAssignment


class DeliveryAssignmentRepository:
    def __init__(self, db: Session):
        self.db = db

    # =========================
    # CREATE
    # =========================
    def create_delivery_assignment(
        self,
        DistributionCenterID: int,
        RecipientID: int,
        VolunteerID: int,
        amount_of_meals: int,
        type: int,
    ) -> DeliveryAssignment:

        assignment = DeliveryAssignment(
            DistributionCenterID=DistributionCenterID,
            RecipientID=RecipientID,
            VolunteerID=VolunteerID,
            amount_of_meals=amount_of_meals,
            type=type
        )

        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    # =========================
    # READ
    # =========================
    def get_delivery_assignment(self, assignmentID: int):
        return self.db.query(DeliveryAssignment)\
            .filter(DeliveryAssignment.id == assignmentID)\
            .first()

    def get_all_delivery_assignments(self):
        return self.db.query(DeliveryAssignment).all()

    # =========================
    # UPDATE (IMPORTANT FOR ALGO 2)
    # =========================
    def assign_volunteer_to_group(self, assignment_id: int, volunteer_id: int):
        """
        שלב אלגוריתם 2:
        מחבר מתנדב לקבוצה קיימת
        """
        assignment = self.get_delivery_assignment(assignment_id)

        if not assignment:
            return None

        assignment.VolunteerID = volunteer_id
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    # =========================
    # DELETE
    # =========================
    def delete_delivery_assignment(self, assignmentID: int) -> bool:
        assignment = self.get_delivery_assignment(assignmentID)

        if not assignment:
            return False

        self.db.delete(assignment)
        self.db.commit()
        return True



    # =========================
    # VRP INPUT (IMPORTANT FIX)
    # =========================
    def get_unassigned_groups(self):
        """
        קבוצות שעדיין לא קיבלו מתנדב
        (זה ה־INPUT של האלגוריתם)
        """

        return self.db.query(DeliveryAssignment)\
            .filter(DeliveryAssignment.VolunteerID.is_(None))\
            .all()