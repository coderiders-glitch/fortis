from app.models.doctor import Doctor
from app.seed_data import DOCTOR_SEED_DATA


def test_seed_data_has_approved_record_count_and_required_fields():
    assert 15 <= len(DOCTOR_SEED_DATA) <= 20
    required_fields = {"name", "speciality", "details", "symptoms", "experience", "location"}
    assert all(set(record) == required_fields for record in DOCTOR_SEED_DATA)


def test_doctor_model_matches_database_table_and_columns():
    assert Doctor.__tablename__ == "doctor_search_doctors"
    assert set(Doctor.__table__.columns.keys()) == {
        "id",
        "name",
        "speciality",
        "details",
        "symptoms",
        "experience",
        "location",
        "created_at",
    }
    for name in ("name", "speciality", "details", "symptoms", "experience", "location"):
        assert Doctor.__table__.columns[name].nullable is False
