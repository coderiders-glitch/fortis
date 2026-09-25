from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.doctor import Doctor


def search_doctors(db: Session, keyword: str) -> list[Doctor]:
    pattern = f"%{keyword.strip()}%"
    return (
        db.query(Doctor)
        .filter(
            or_(
                Doctor.name.ilike(pattern),
                Doctor.speciality.ilike(pattern),
                Doctor.details.ilike(pattern),
                Doctor.symptoms.ilike(pattern),
            )
        )
        .order_by(Doctor.id)
        .all()
    )
