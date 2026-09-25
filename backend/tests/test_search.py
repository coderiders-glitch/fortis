from app.seed_data import DOCTOR_SEED_DATA
from app.services.search import search_doctors


class FakeQuery:
    def __init__(self, rows):
        self.rows = rows
        self.criteria = []

    def filter(self, criterion):
        self.criteria.append(criterion)
        return self

    def order_by(self, ordering):
        return self

    def all(self):
        return self.rows


class FakeSession:
    def __init__(self, rows):
        self.query_object = FakeQuery(rows)
        self.queried_model = None

    def query(self, model):
        self.queried_model = model
        return self.query_object


def test_search_service_builds_case_insensitive_conditions_for_each_field():
    from app.models.doctor import Doctor

    session = FakeSession([DOCTOR_SEED_DATA[0]])
    results = search_doctors(session, "  CARDIO  ")

    assert session.queried_model is Doctor
    assert len(session.query_object.criteria) == 1
    compiled = str(session.query_object.criteria[0]).upper()
    assert compiled.count(" ILIKE ") == 4
    assert results == [DOCTOR_SEED_DATA[0]]
