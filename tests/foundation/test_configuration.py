import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("exported_value", [None, "13"])
def test_dotenv_loads_without_overriding_exported_environment(
    tmp_path: Path, exported_value: str | None
) -> None:
    (tmp_path / ".env").write_text("ACCESS_TOKEN_EXPIRE_MINUTES=17\n", encoding="utf-8")
    environment = dict(os.environ, PYTHONPATH=str(PROJECT_ROOT))
    environment.pop("ACCESS_TOKEN_EXPIRE_MINUTES", None)
    if exported_value is not None:
        environment["ACCESS_TOKEN_EXPIRE_MINUTES"] = exported_value
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from app.core.config import get_settings; "
            "print(get_settings().access_token_expire_minutes)",
        ],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == (exported_value or "17")


def test_api_test_client_does_not_initialize_demo_database(
    client, monkeypatch: pytest.MonkeyPatch
) -> None:
    from app import main

    def forbidden_init():
        pytest.fail("Test lifespan must not initialize the demo database")

    monkeypatch.setattr(main, "init_db", forbidden_init)
    # Re-enter this client's lifespan to prove the test app has no database initializer.
    with client:
        assert client.get("/health").status_code == 200
