from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app


class FakeQuery:
    def __init__(self, results):
        self.results = results

    def filter(self, *criteria):
        return self

    def all(self):
        return self.results


class FakeSession:
    def __init__(self, results):
        self.results = results

    def query(self, model):
        return FakeQuery(self.results)

    def close(self):
        pass


def doctor_record():
    return type(
        "DoctorRecord",
        (),
        {
            "id": 1,
            "name": "Dr. Sarah Johnson",
            "speciality": "Cardiologist",
            "details": "Heart disease prevention specialist.",
            "symptoms": "chest pain, shortness of breath",
            "experience": 15,
            "location": "123 Heart Center",
        },
    )()


def test_search_returns_contract_response():
    app.dependency_overrides[get_db] = lambda: FakeSession([doctor_record()])
    try:
        response = TestClient(app).get("/api/doctors/search", params={"q": "CARDIO"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 1
    assert payload["message"] == "Found 1 matching doctor"
    assert payload["results"][0]["name"] == "Dr. Sarah Johnson"
    assert payload["results"][0]["experience"] == 15


def test_search_returns_clear_no_results_response():
    app.dependency_overrides[get_db] = lambda: FakeSession([])
    try:
        response = TestClient(app).get("/api/doctors/search", params={"q": "unknown"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "results": [],
        "count": 0,
        "message": "No results found. Try a different search term.",
    }


def test_empty_search_query_returns_contract_error():
    response = TestClient(app).get("/api/doctors/search", params={"q": "   "})

    assert response.status_code == 400
    assert response.json() == {
        "error": "invalid_request",
        "message": "Search query cannot be empty",
    }


def test_health_endpoint():
    response = TestClient(app).get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
