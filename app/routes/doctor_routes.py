from flask import Blueprint, jsonify
from app.services import list_doctors
from app.schema import DoctorRead

doctor_bp = Blueprint("doctor", __name__)


@doctor_bp.route("/", methods=["GET"])
def get_doctors():
    doctors = list_doctors()
    return jsonify([DoctorRead.from_orm(doc).dict() for doc in doctors])
