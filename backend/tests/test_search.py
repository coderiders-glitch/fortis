from sqlalchemy.dialects import postgresql

from app.models.doctor import Doctor
from app.services.search import search_doctors


class CapturingQuery:
    def __init__(self, result):
        self.result = result
        self.criteria = []

    def filter(self, *criteria):
        self.criteria.extend(criteria)
        return self

    def all(self):
        return self.result


class CapturingSession:
    def __init__(self, result):
        self.query_instance = CapturingQuery(result)
        self.model = None

    def query(self, model):
        self.model = model
        return self.query_instance


def test_search_builds_case_insensitive_parameterized_filter_for_all_fields():
    session = CapturingSession([])

    results = search_doctors(session, "heart")

    assert results == []
    assert session.model is Doctor
    assert len(session.query_instance.criteria) == 1
    compiled = session.query_instance.criteria[0].compile(dialect=postgresql.dialect())
    sql = str(compiled).lower()
    assert sql.count("ilike") == 4
    assert len(compiled.params) == 4
    assert set(compiled.params.values()) == {"%heart%"}


def test_search_escapes_wildcards_in_keyword():
    session = CapturingSession([])

    search_doctors(session, "100%_match")

    compiled = session.query_instance.criteria[0].compile(dialect=postgresql.dialect())
    assert set(compiled.params.values()) == {r"%100\%\_match%"}
