from fastapi.routing import APIRoute

from app.main import app


def test_doctor_search_route_is_mounted_at_frontend_api_path() -> None:
    matching_routes = [
        route
        for route in app.routes
        if isinstance(route, APIRoute) and route.path == "/api/doctors/search"
    ]

    assert len(matching_routes) == 1
    assert "GET" in matching_routes[0].methods
