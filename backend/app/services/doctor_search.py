from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.doctor import Doctor


_SEARCHABLE_FIELDS = (Doctor.name, Doctor.speciality, Doctor.details, Doctor.symptoms)


def build_search_conditions(query: str):
    pattern = f"%{query}%"
    return tuple(field.ilike(pattern) for field in _SEARCHABLE_FIELDS)


def search_doctors(db: Session, query: str) -> list[Doctor]:
    return (
        db.query(Doctor)
        .filter(or_(*build_search_conditions(query)))
        .order_by(Doctor.name)
        .all()
    )
