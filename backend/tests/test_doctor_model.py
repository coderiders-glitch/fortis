from sqlalchemy import DateTime

from app.models.doctor import Doctor


def test_doctor_created_at_maps_to_datetime_column() -> None:
    column = Doctor.__table__.c.created_at

    assert isinstance(column.type, DateTime)
    assert column.nullable is False
    assert column.server_default is not None
