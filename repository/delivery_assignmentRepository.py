from sqlalchemy.orm import Session
from models.delivery_assignment import DeliveryAssignment

class DeliveryAssignmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_delivery_assignment(
        self,
        DistributionCenterID: int,
        RecipientID: int,
        VolunteerID: int,
        amount_of_meals: int
    ) -> DeliveryAssignment:
        assignment = DeliveryAssignment(
            DistributionCenterID=DistributionCenterID,
            RecipientID=RecipientID,
            VolunteerID=VolunteerID,
            amount_of_meals=amount_of_meals
        )
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def get_delivery_assignment(self, assignmentID: int) -> DeliveryAssignment | None:
        return self.db.query(DeliveryAssignment).filter(DeliveryAssignment.id == assignmentID).first()

    def get_all_delivery_assignments(self) -> list[DeliveryAssignment]:
        return self.db.query(DeliveryAssignment).all()

    def update_delivery_assignment(
        self,
        assignmentID: int,
        DistributionCenterID: int = None,
        RecipientID: int = None,
        VolunteerID: int = None,
        amount_of_meals: int = None
    ) -> DeliveryAssignment | None:
        assignment = self.get_delivery_assignment(assignmentID)
        if assignment:
            if DistributionCenterID is not None:
                assignment.DistributionCenterID = DistributionCenterID
            if RecipientID is not None:
                assignment.RecipientID = RecipientID
            if VolunteerID is not None:
                assignment.VolunteerID = VolunteerID
            if amount_of_meals is not None:
                assignment.amount_of_meals = amount_of_meals
            self.db.commit()
            self.db.refresh(assignment)
        return assignment

    def delete_delivery_assignment(self, assignmentID: int) -> bool:
        assignment = self.get_delivery_assignment(assignmentID)
        if assignment:
            self.db.delete(assignment)
            self.db.commit()
            return True
        return False