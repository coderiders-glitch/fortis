import pytest
from fastapi.testclient import TestClient

import app.main as main_module
from app.api import doctors as doctors_module
from app.database import get_db


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(main_module, "initialize_database", lambda: None)
    main_module.app.dependency_overrides[get_db] = lambda: object()
    with TestClient(main_module.app) as test_client:
        yield test_client
    main_module.app.dependency_overrides.clear()


def test_search_returns_matching_doctor_and_contract_fields(client, monkeypatch):
    doctor = {
        "id": 1,
        "name": "Dr. Sarah Johnson",
        "speciality": "Cardiologist",
        "details": "Heart disease prevention specialist.",
        "symptoms": "chest pain, palpitations",
        "experience": 15,
        "location": "123 Heart Center",
    }
    monkeypatch.setattr(doctors_module, "search_doctors", lambda db, keyword: [doctor])

    response = client.get("/api/doctors/search", params={"q": "CARDIO"})

    assert response.status_code == 200
    assert response.json() == {
        "results": [doctor],
        "count": 1,
        "message": "Found 1 matching doctor",
    }


def test_search_returns_clear_no_results_message(client, monkeypatch):
    monkeypatch.setattr(doctors_module, "search_doctors", lambda db, keyword: [])

    response = client.get("/api/doctors/search", params={"q": "not-a-doctor"})

    assert response.status_code == 200
    assert response.json() == {
        "results": [],
        "count": 0,
        "message": "No results found. Try a different search term.",
    }


def test_blank_search_is_a_contract_error(client, monkeypatch):
    def unexpected_search(db, keyword):
        pytest.fail("Search service must not run for blank input")

    monkeypatch.setattr(doctors_module, "search_doctors", unexpected_search)
    response = client.get("/api/doctors/search", params={"q": "   "})

    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "error": "invalid_request",
            "message": "Search query cannot be empty",
        }
    }


def test_search_rejects_keyword_longer_than_contract_limit(client, monkeypatch):
    response = client.get("/api/doctors/search", params={"q": "x" * 201})

    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "invalid_request"


def test_health_endpoint(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
