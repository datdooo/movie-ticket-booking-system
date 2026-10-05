from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_openapi_contains_all_required_business_endpoints(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()
    paths = schema["paths"]
    operations = {
        (method.upper(), path)
        for path, methods in paths.items()
        for method in methods
        if method in {"get", "post", "delete", "put", "patch"}
    }
    assert operations == {
        ("POST", "/auth/register"),
        ("POST", "/auth/login"),
        ("GET", "/movies"),
        ("GET", "/showtimes"),
        ("GET", "/showtimes/{showtime_id}/seats"),
        ("POST", "/bookings"),
        ("GET", "/bookings/me"),
        ("GET", "/bookings/{booking_id}"),
        ("DELETE", "/bookings/{booking_id}"),
        ("GET", "/health"),
    }
    assert paths["/bookings"]["post"]["security"]
    assert paths["/bookings/me"]["get"]["security"]
    assert paths["/bookings/{booking_id}"]["get"]["security"]
    assert paths["/bookings/{booking_id}"]["delete"]["security"]


def test_protected_get_and_post_reject_missing_token(client: TestClient) -> None:
    assert client.get("/bookings/me").status_code == 401
    assert client.get("/bookings/1").status_code == 401
    assert client.post("/bookings", json={"showtime_id": 1, "seat_id": 1}).status_code == 401
