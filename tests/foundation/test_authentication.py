from datetime import UTC, datetime, timedelta

import jwt
import pytest
from fastapi.testclient import TestClient

from app.api.middleware import authentication
from app.core.config import get_settings
from app.core.security import create_access_token

PROTECTED_ROUTES = [
    ("GET", "/bookings/me"),
    ("GET", "/bookings/1"),
    ("POST", "/bookings"),
    ("DELETE", "/bookings/1"),
]


@pytest.mark.parametrize(("method", "path"), PROTECTED_ROUTES)
@pytest.mark.parametrize("case", ["missing", "malformed", "expired", "no_exp", "bad_signature"])
def test_protected_routes_reject_invalid_credentials(
    client: TestClient, method: str, path: str, case: str
) -> None:
    settings = get_settings()
    now = datetime.now(UTC)
    payload = {"sub": "1", "iat": now, "exp": now + timedelta(minutes=5)}
    headers = {}
    if case == "malformed":
        headers = {"Authorization": "Bearer invalid"}
    elif case != "missing":
        if case == "expired":
            payload["exp"] = now - timedelta(seconds=1)
        if case == "no_exp":
            payload.pop("exp")
        secret = (
            "wrong-signing-secret-for-test-only"
            if case == "bad_signature"
            else settings.jwt_secret_key
        )
        headers = {"Authorization": f"Bearer {jwt.encode(payload, secret, algorithm='HS256')}"}
    kwargs = {"json": {"showtime_id": 1, "seat_id": 1}} if method == "POST" else {}
    response = client.request(method, path, headers=headers, **kwargs)
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_jwt_is_decoded_once_in_middleware(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = authentication.decode_access_token
    decoded = []

    def counted_decode(token, settings):
        user_id = original(token, settings)
        decoded.append(user_id)
        return user_id

    monkeypatch.setattr(authentication, "decode_access_token", counted_decode)
    token = create_access_token(1, get_settings())
    response = client.get("/bookings/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 501
    assert decoded == [1]
