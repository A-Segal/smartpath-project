from flask import Blueprint, request, jsonify
from repository.distribution_centerRepository import DistributionCenterRepository
from db_connection import SessionLocal
from dto.distribution_centerDTO import DistributionCenterDTO  # נניח שיש קובץ DTO
from typing import List

# Blueprint עבור DistributionCenter
distribution_center_bp = Blueprint('distribution_center_bp', __name__, url_prefix='/distribution_center')

# ==================== יצירת מרכז חלוקה חדש (POST) ====================
@distribution_center_bp.route('', methods=['POST'])
def add_distribution_center():
    db_session = SessionLocal()
    try:
        repo = DistributionCenterRepository(db_session)
        data = request.get_json()

        new_center = repo.create_distribution_center(
            fname=data['fname'],
            lname=data['lname'],
            username=data['username'],
            password=data['password'],
            mail=data['mail'],
            phone=data['phone'],
            location_lat=data['location_lat'],
            location_lng=data['location_lng'],
            meal_count=data.get('meal_count', 0),
            request=data.get('request')
        )

        dto = DistributionCenterDTO(
            id=new_center.id,
            fname=new_center.fname,
            lname=new_center.lname,
            username=new_center.username,
            mail=new_center.mail,
            phone=new_center.phone,
            location_lat=new_center.location_lat,
            location_lng=new_center.location_lng,
            request=new_center.request
        )

        return jsonify(dto.__dict__), 201
    finally:
        db_session.close()

# ==================== קבלת מרכז לפי ID (GET) ====================
@distribution_center_bp.route('/<int:center_id>', methods=['GET'])
def get_distribution_center(center_id):
    db_session = SessionLocal()
    try:
        repo = DistributionCenterRepository(db_session)
        center = repo.get_distribution_center(center_id)
        if not center:
            return jsonify({'error': 'DistributionCenter not found'}), 404

        dto = DistributionCenterDTO(
            id=center.id,
            fname=center.fname,
            lname=center.lname,
            username=center.username,
            mail=center.mail,
            phone=center.phone,
            location_lat=center.location_lat,
            location_lng=center.location_lng,
            request=center.request
        )

        return jsonify(dto.__dict__)
    finally:
        db_session.close()

# ==================== קבלת כל מרכזי החלוקה (GET all) ====================
@distribution_center_bp.route('', methods=['GET'])
def get_all_distribution_centers():
    db_session = SessionLocal()
    try:
        repo = DistributionCenterRepository(db_session)
        centers = repo.get_all_distribution_centers()

        all_dto: List[dict] = [
            DistributionCenterDTO(
                id=c.id,
                fname=c.fname,
                lname=c.lname,
                username=c.username,
                mail=c.mail,
                phone=c.phone,
                location_lat=c.location_lat,
                location_lng=c.location_lng,
                request=c.request
            ).__dict__ for c in centers
        ]

        return jsonify(all_dto)
    finally:
        db_session.close()

# ==================== עדכון מרכז חלוקה (PUT) ====================
@distribution_center_bp.route('/<int:center_id>', methods=['PUT'])
def update_distribution_center(center_id):
    db_session = SessionLocal()
    try:
        repo = DistributionCenterRepository(db_session)
        data = request.get_json()

        updated = repo.update_distribution_center(
            centerID=center_id,
            fname=data.get('fname'),
            lname=data.get('lname'),
            username=data.get('username'),
            password=data.get('password'),
            mail=data.get('mail'),
            phone=data.get('phone'),
            location_lat=data.get('location_lat'),
            location_lng=data.get('location_lng'),
            request=data.get('request')
        )

        if not updated:
            return jsonify({'error': 'DistributionCenter not found'}), 404

        dto = DistributionCenterDTO(
            id=updated.id,
            fname=updated.fname,
            lname=updated.lname,
            username=updated.username,
            mail=updated.mail,
            phone=updated.phone,
            location_lat=updated.location_lat,
            location_lng=updated.location_lng,
            request=updated.request
        )

        return jsonify(dto.__dict__)
    finally:
        db_session.close()

# ==================== מחיקת מרכז חלוקה (DELETE) ====================
@distribution_center_bp.route('/<int:center_id>', methods=['DELETE'])
def delete_distribution_center(center_id):
    db_session = SessionLocal()
    try:
        repo = DistributionCenterRepository(db_session)
        success = repo.delete_distribution_center(center_id)
        if not success:
            return jsonify({'error': 'DistributionCenter not found'}), 404
        return jsonify({'message': 'DistributionCenter deleted successfully'})
    finally:
        db_session.close()