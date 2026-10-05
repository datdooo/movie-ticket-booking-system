from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.features.catalog.dependencies import get_catalog_service


def test_unknown_path_uses_json_error_envelope(client: TestClient) -> None:
    response = client.get("/unknown-path")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


def test_unexpected_error_uses_json_without_exposing_exception(client: TestClient) -> None:
    def explode():
        raise RuntimeError("internal database details must not be returned")

    client.app.dependency_overrides[get_catalog_service] = lambda: SimpleNamespace(
        list_movies=explode
    )
    with TestClient(client.app, raise_server_exceptions=False) as test_client:
        response = test_client.get("/movies")
    assert response.status_code == 500
    assert response.json() == {"error": {"code": "INTERNAL_ERROR", "message": "Lỗi hệ thống"}}
