from app.models import Doctor


def get_all_doctors():
    return Doctor.query.order_by(Doctor.last_name.asc(), Doctor.first_name.asc()).all()
