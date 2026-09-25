from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.doctor import Doctor


def search_doctors(db: Session, keyword: str) -> list[Doctor]:
    escaped_keyword = keyword.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    pattern = f"%{escaped_keyword}%"
    return (
        db.query(Doctor)
        .filter(
            or_(
                Doctor.name.ilike(pattern, escape="\\"),
                Doctor.speciality.ilike(pattern, escape="\\"),
                Doctor.details.ilike(pattern, escape="\\"),
                Doctor.symptoms.ilike(pattern, escape="\\"),
            )
        )
        .all()
    )
