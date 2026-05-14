#DTO
from flask import Blueprint, request, jsonify
from repository.staff_memberRepository import StaffMemberRepository
from db_connection import SessionLocal
from dto.staff_memberDTO import StaffMemberDTO

staff_bp = Blueprint('staff_bp', __name__, url_prefix='/staff')

# ===================== יצירת עובד =====================
@staff_bp.route('', methods=['POST'])
def add_staff_member():
    db_session = SessionLocal()
    try:
        staff_repo = StaffMemberRepository(db_session)
        data = request.get_json()
        new_staff = staff_repo.create_staff_member(
            fname=data['fname'],
            lname=data['lname'],
            username=data['username'],
            password=data['password'],
            PermissionID=data['PermissionID'],
            mail=data.get('mail'),
            phone=data.get('phone')
        )
        staff_dto = StaffMemberDTO(
            id=new_staff.id,
            fname=new_staff.fname,
            lname=new_staff.lname,
            username=new_staff.username,
            mail=new_staff.mail,
            phone=new_staff.phone,
            PermissionID=new_staff.PermissionID
        )
        return jsonify(staff_dto.__dict__), 201
    finally:
        db_session.close()


# ===================== קבלת עובד לפי ID =====================
@staff_bp.route('/<int:staff_id>', methods=['GET'])
def get_staff_member(staff_id):
    db_session = SessionLocal()
    try:
        staff_repo = StaffMemberRepository(db_session)
        staff = staff_repo.get_staff_member(staff_id)
        if staff is None:
            return jsonify({'error': 'Staff member not found'}), 404

        staff_dto = StaffMemberDTO(
            id=staff.id,
            fname=staff.fname,
            lname=staff.lname,
            username=staff.username,
            mail=staff.mail,
            phone=staff.phone,
            PermissionID=staff.PermissionID
        )
        return jsonify(staff_dto.__dict__)
    finally:
        db_session.close()


# ===================== קבלת כל העובדים =====================
@staff_bp.route('', methods=['GET'])
def get_all_staff_members():
    db_session = SessionLocal()
    try:
        staff_repo = StaffMemberRepository(db_session)
        staff_members = staff_repo.get_all_staff_members()
        staff_dtos = [
            StaffMemberDTO(
                id=s.id,
                fname=s.fname,
                lname=s.lname,
                username=s.username,
                mail=s.mail,
                phone=s.phone,
                PermissionID=s.PermissionID
            ).__dict__ for s in staff_members
        ]
        return jsonify(staff_dtos)
    finally:
        db_session.close()


# ===================== עדכון עובד =====================
@staff_bp.route('/<int:staff_id>', methods=['PUT'])
def update_staff_member(staff_id):
    db_session = SessionLocal()
    try:
        staff_repo = StaffMemberRepository(db_session)
        data = request.get_json()
        updated_staff = staff_repo.update_staff_member(
            staff_id,
            fname=data.get('fname'),
            lname=data.get('lname'),
            username=data.get('username'),
            password=data.get('password'),
            PermissionID=data.get('PermissionID'),
            mail=data.get('mail'),
            phone=data.get('phone')
        )
        if updated_staff is None:
            return jsonify({'error': 'Staff member not found'}), 404

        staff_dto = StaffMemberDTO(
            id=updated_staff.id,
            fname=updated_staff.fname,
            lname=updated_staff.lname,
            username=updated_staff.username,
            mail=updated_staff.mail,
            phone=updated_staff.phone,
            PermissionID=updated_staff.PermissionID
        )
        return jsonify(staff_dto.__dict__)
    finally:
        db_session.close()


# ===================== מחיקת עובד =====================
@staff_bp.route('/<int:staff_id>', methods=['DELETE'])
def delete_staff_member(staff_id):
    db_session = SessionLocal()
    try:
        staff_repo = StaffMemberRepository(db_session)
        success = staff_repo.delete_staff_member(staff_id)
        if not success:
            return jsonify({'error': 'Staff member not found'}), 404
        return jsonify({'message': 'Staff member deleted successfully'})
    finally:
        db_session.close()