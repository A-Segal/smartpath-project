from sqlalchemy.orm import Session
from models.delivery_assignment import DeliveryAssignment
from models.distribution_center import DistributionCenter
from models.distribution_center import DistributionCenter
from models.recipient import Recipient


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

    def get_unassigned_groups_view(self):
        """
        הופך DeliveryAssignment ל-GROUP לוגי לפי DistributionCenterID
        """

        rows = self.db.query(DeliveryAssignment) \
            .filter(DeliveryAssignment.VolunteerID.is_(None)) \
            .all()

        groups = {}

        for r in rows:
            center_id = r.DistributionCenterID

            if center_id not in groups:
                groups[center_id] = {
                    "center_id": center_id,
                    "assignment_ids": [],
                    "total_meals": 0,
                    "recipient_count": 0
                }

            groups[center_id]["assignment_ids"].append(r.id)
            groups[center_id]["total_meals"] += r.amount_of_meals
            groups[center_id]["recipient_count"] += 1

        return list(groups.values())


    def build_groups(self):
        rows = self.db.query(DeliveryAssignment)\
            .filter(DeliveryAssignment.VolunteerID.is_(None))\
            .all()

        groups = {}

        for r in rows:

            center = self.db.query(DistributionCenter)\
                .filter(DistributionCenter.id == r.DistributionCenterID)\
                .first()

            recipient = self.db.query(Recipient)\
                .filter(Recipient.id == r.RecipientID)\
                .first()

            if not center or not recipient:
                continue

            key = r.DistributionCenterID

            if key not in groups:
                groups[key] = {
                    "center_id": key,
                    "center_lat": float(center.location_lat),
                    "center_lng": float(center.location_lng),
                    "recipients_locations": [],
                    "assignment_ids": [],
                    "total_meals": 0
                }

            groups[key]["recipients_locations"].append({
                "lat": float(recipient.location_lat),
                "lng": float(recipient.location_lng)
            })

            groups[key]["assignment_ids"].append(r.id)
            groups[key]["total_meals"] += r.amount_of_meals

        return list(groups.values())