from flask import Blueprint, request, jsonify
from repository.DC_request_Repository import DCRequestRepository
from db_connection import SessionLocal
from dto.DC_requestDTO import DCRequestDTO
from datetime import datetime

# Blueprint עבור DS Requests
dc_request_bp = Blueprint('dc_request_bp', __name__, url_prefix='/dc_requests')


# ===================== יצירת בקשה =====================
@dc_request_bp.route('', methods=['POST'])
def add_request():
    db_session = SessionLocal()
    try:
        repo = DCRequestRepository(db_session)
        data = request.get_json()

        request_date = data.get('request_date')
        if request_date:
            request_date = datetime.fromisoformat(request_date)

        type = data.get('type', 0)  # ערך ברירת מחדל 0

        new_request = repo.create_request(
            distribution_center_id=data['DistributionCenterID'],
            amount_of_meals=data['amount_of_meals'],
            request_date=request_date,
            type=type
        )

        dto = DCRequestDTO(
            id=new_request.id,
            DistributionCenterID=new_request.DistributionCenterID,
            amount_of_meals=new_request.amount_of_meals,
            request_date=new_request.request_date.isoformat(),
            type=new_request.type
        )
        return jsonify(dto.__dict__), 201
    finally:
        db_session.close()


# ===================== קבלת בקשה לפי ID =====================
@dc_request_bp.route('/<int:request_id>', methods=['GET'])
def get_request(request_id):
    db_session = SessionLocal()
    try:
        repo = DCRequestRepository(db_session)
        req = repo.get_request(request_id)
        if req is None:
            return jsonify({'error': 'Request not found'}), 404

        dto = DCRequestDTO(
            id=req.id,
            DistributionCenterID=req.DistributionCenterID,
            amount_of_meals=req.amount_of_meals,
            request_date=req.request_date.isoformat(),
            type=req.type
        )
        return jsonify(dto.__dict__)
    finally:
        db_session.close()


# ===================== קבלת כל הבקשות =====================
@dc_request_bp.route('', methods=['GET'])
def get_all_requests():
    db_session = SessionLocal()
    try:
        repo = DCRequestRepository(db_session)
        all_requests = repo.get_all_requests()

        dto_list = [
            DCRequestDTO(
                id=r.id,
                DistributionCenterID=r.DistributionCenterID,
                amount_of_meals=r.amount_of_meals,
                request_date=r.request_date.isoformat(),
                type=r.type
            ).__dict__ for r in all_requests
        ]
        return jsonify(dto_list)
    finally:
        db_session.close()


# ===================== עדכון בקשה =====================
@dc_request_bp.route('/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    db_session = SessionLocal()
    try:
        repo = DCRequestRepository(db_session)
        data = request.get_json()

        request_date = data.get('request_date')
        if request_date:
            request_date = datetime.fromisoformat(request_date)

        type = data.get('type', None)

        updated_request = repo.update_request(
            request_id,
            amount_of_meals=data.get('amount_of_meals'),
            request_date=request_date,
            type=type
        )

        if updated_request is None:
            return jsonify({'error': 'Request not found'}), 404

        dto = DCRequestDTO(
            id=updated_request.id,
            DistributionCenterID=updated_request.DistributionCenterID,
            amount_of_meals=updated_request.amount_of_meals,
            request_date=updated_request.request_date.isoformat(),
            type=updated_request.type
        )
        return jsonify(dto.__dict__)
    finally:
        db_session.close()


# ===================== מחיקת בקשה =====================
@dc_request_bp.route('/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    db_session = SessionLocal()
    try:
        repo = DCRequestRepository(db_session)
        success = repo.delete_request(request_id)
        if not success:
            return jsonify({'error': 'Request not found'}), 404
        return jsonify({'message': 'Request deleted successfully'})
    finally:
        db_session.close()