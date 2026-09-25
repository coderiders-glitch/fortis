from app.models.doctor import Doctor
from app.seed_data import SEED_DOCTORS


def test_doctor_model_matches_required_database_fields():
    columns = Doctor.__table__.columns

    assert Doctor.__tablename__ == "doctor_search_doctors"
    assert {"id", "name", "speciality", "details", "symptoms", "experience", "location", "created_at"}.issubset(columns.keys())
    for field in ("name", "speciality", "details", "symptoms", "experience", "location"):
        assert columns[field].nullable is False


def test_seed_data_has_between_fifteen_and_twenty_complete_records():
    assert 15 <= len(SEED_DOCTORS) <= 20
    required_fields = {"name", "speciality", "details", "symptoms", "experience", "location"}
    assert all(set(record) == required_fields for record in SEED_DOCTORS)
