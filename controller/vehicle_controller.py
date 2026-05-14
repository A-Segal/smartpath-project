#DTO

from flask import Blueprint, request, jsonify
from repository.VehicleRepository import VehicleRepository
from db_connection import SessionLocal
from dto.vehicleDTO import VehicleDTO

# Blueprint עבור Vehicles
vehicle_bp = Blueprint('vehicle_bp', __name__, url_prefix='/vehicles')

# ===================== יצירת רכב =====================
@vehicle_bp.route('', methods=['POST'])
def add_vehicle():
    db_session = SessionLocal()
    try:
        vehicle_repo = VehicleRepository(db_session)
        data = request.get_json()
        new_vehicle = vehicle_repo.create_vehicle(
            VolunteerID=data['VolunteerID'],
            capacity=data['capacity']
        )

        vehicle_dto = VehicleDTO(
            id=new_vehicle.id,
            VolunteerID=new_vehicle.VolunteerID,
            capacity=new_vehicle.capacity
        )

        return jsonify(vehicle_dto.__dict__), 201
    finally:
        db_session.close()

# ===================== קבלת רכב לפי ID =====================
@vehicle_bp.route('/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    db_session = SessionLocal()
    try:
        vehicle_repo = VehicleRepository(db_session)
        vehicle = vehicle_repo.get_vehicle(vehicle_id)
        if vehicle is None:
            return jsonify({'error': 'Vehicle not found'}), 404

        vehicle_dto = VehicleDTO(
            id=vehicle.id,
            VolunteerID=vehicle.VolunteerID,
            capacity=vehicle.capacity
        )

        return jsonify(vehicle_dto.__dict__)
    finally:
        db_session.close()

# ===================== קבלת כל הרכבים =====================
@vehicle_bp.route('', methods=['GET'])
def get_all_vehicles():
    db_session = SessionLocal()
    try:
        vehicle_repo = VehicleRepository(db_session)
        vehicles = vehicle_repo.get_all_vehicles()

        vehicles_dto = [
            VehicleDTO(
                id=v.id,
                VolunteerID=v.VolunteerID,
                capacity=v.capacity
            ).__dict__ for v in vehicles
        ]

        return jsonify(vehicles_dto)
    finally:
        db_session.close()

# ===================== עדכון רכב =====================
@vehicle_bp.route('/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    db_session = SessionLocal()
    try:
        vehicle_repo = VehicleRepository(db_session)
        data = request.get_json()
        updated_vehicle = vehicle_repo.update_vehicle(
            vehicle_id,
            capacity=data['capacity']
        )

        if updated_vehicle is None:
            return jsonify({'error': 'Vehicle not found'}), 404

        vehicle_dto = VehicleDTO(
            id=updated_vehicle.id,
            VolunteerID=updated_vehicle.VolunteerID,
            capacity=updated_vehicle.capacity
        )

        return jsonify(vehicle_dto.__dict__)
    finally:
        db_session.close()

# ===================== מחיקת רכב =====================
@vehicle_bp.route('/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    db_session = SessionLocal()
    try:
        vehicle_repo = VehicleRepository(db_session)
        success = vehicle_repo.delete_vehicle(vehicle_id)
        if not success:
            return jsonify({'error': 'Vehicle not found'}), 404
        return jsonify({'message': 'Vehicle deleted successfully'})
    finally:
        db_session.close()

# ===================== מחיקת רכבים לפי מתנדב =====================
@vehicle_bp.route('/volunteer/<int:volunteer_id>', methods=['DELETE'])
def delete_vehicles_by_volunteer(volunteer_id):
    db_session = SessionLocal()
    try:
        vehicle_repo = VehicleRepository(db_session)
        vehicle_repo.delete_vehicle_by_volunteer(volunteer_id)
        return jsonify({'message': f'All vehicles for volunteer {volunteer_id} deleted successfully'})
    finally:
        db_session.close()