
from flask import Blueprint, request, jsonify
from repository.delivery_assignmentRepository import DeliveryAssignmentRepository
from db_connection import SessionLocal
from dto.delivery_assignmentDTO import DeliveryAssignmentDTO  # נניח שיש קובץ DTO
from typing import List

# Blueprint עבור DeliveryAssignment
delivery_assignment_bp = Blueprint('delivery_assignment_bp', __name__, url_prefix='/delivery_assignment')

# ==================== יצירת משלוח חדש (POST) ====================
@delivery_assignment_bp.route('', methods=['POST'])
def add_delivery_assignment():
    db_session = SessionLocal()
    try:
        repo = DeliveryAssignmentRepository(db_session)
        data = request.get_json()

        new_assignment = repo.create_delivery_assignment(
            DistributionCenterID=data['DistributionCenterID'],
            RecipientID=data['RecipientID'],
            VolunteerID=data['VolunteerID'],
            amount_of_meals=data['amount_of_meals']
        )

        dto = DeliveryAssignmentDTO(
            id=new_assignment.id,
            DistributionCenterID=new_assignment.DistributionCenterID,
            RecipientID=new_assignment.RecipientID,
            VolunteerID=new_assignment.VolunteerID,
            amount_of_meals=new_assignment.amount_of_meals
        )

        return jsonify(dto.__dict__), 201
    finally:
        db_session.close()

# ==================== קבלת משלוח לפי ID (GET) ====================
@delivery_assignment_bp.route('/<int:assignment_id>', methods=['GET'])
def get_delivery_assignment(assignment_id):
    db_session = SessionLocal()
    try:
        repo = DeliveryAssignmentRepository(db_session)
        assignment = repo.get_delivery_assignment(assignment_id)
        if not assignment:
            return jsonify({'error': 'DeliveryAssignment not found'}), 404

        dto = DeliveryAssignmentDTO(
            id=assignment.id,
            DistributionCenterID=assignment.DistributionCenterID,
            RecipientID=assignment.RecipientID,
            VolunteerID=assignment.VolunteerID,
            amount_of_meals=assignment.amount_of_meals
        )

        return jsonify(dto.__dict__)
    finally:
        db_session.close()

# ==================== קבלת כל המשלוחים (GET all) ====================
@delivery_assignment_bp.route('', methods=['GET'])
def get_all_delivery_assignments():
    db_session = SessionLocal()
    try:
        repo = DeliveryAssignmentRepository(db_session)
        assignments = repo.get_all_delivery_assignments()

        all_dto: List[dict] = [
            DeliveryAssignmentDTO(
                id=a.id,
                DistributionCenterID=a.DistributionCenterID,
                RecipientID=a.RecipientID,
                VolunteerID=a.VolunteerID,
                amount_of_meals=a.amount_of_meals
            ).__dict__ for a in assignments
        ]

        return jsonify(all_dto)
    finally:
        db_session.close()

# ==================== עדכון משלוח (PUT) ====================
@delivery_assignment_bp.route('/<int:assignment_id>', methods=['PUT'])
def update_delivery_assignment(assignment_id):
    db_session = SessionLocal()
    try:
        repo = DeliveryAssignmentRepository(db_session)
        data = request.get_json()

        updated = repo.update_delivery_assignment(
            assignmentID=assignment_id,
            DistributionCenterID=data.get('DistributionCenterID'),
            RecipientID=data.get('RecipientID'),
            VolunteerID=data.get('VolunteerID'),
            amount_of_meals=data.get('amount_of_meals')
        )

        if not updated:
            return jsonify({'error': 'DeliveryAssignment not found'}), 404

        dto = DeliveryAssignmentDTO(
            id=updated.id,
            DistributionCenterID=updated.DistributionCenterID,
            RecipientID=updated.RecipientID,
            VolunteerID=updated.VolunteerID,
            amount_of_meals=updated.amount_of_meals
        )

        return jsonify(dto.__dict__)
    finally:
        db_session.close()

# ==================== מחיקת משלוח (DELETE) ====================
@delivery_assignment_bp.route('/<int:assignment_id>', methods=['DELETE'])
def delete_delivery_assignment(assignment_id):
    db_session = SessionLocal()
    try:
        repo = DeliveryAssignmentRepository(db_session)
        success = repo.delete_delivery_assignment(assignment_id)
        if not success:
            return jsonify({'error': 'DeliveryAssignment not found'}), 404
        return jsonify({'message': 'DeliveryAssignment deleted successfully'})
    finally:
        db_session.close()