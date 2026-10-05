import subprocess
import sys
from pathlib import Path

import pytest

SCOPE_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_feature_scope.py"


@pytest.mark.parametrize(
    ("changed_path", "expected_exit"),
    [("app/features/auth/api.py", 0), ("app/features/catalog/api.py", 1), ("README.md", 1)],
)
def test_feature_scope_check_on_real_git_diff(
    tmp_path: Path, changed_path: str, expected_exit: int
) -> None:
    def git(*args):
        return subprocess.run(
            ["git", *args], cwd=tmp_path, check=True, capture_output=True, text=True
        ).stdout.strip()

    git("init", "-b", "main")
    git("config", "user.name", "Scope Test")
    git("config", "user.email", "scope-test@example.com")
    (tmp_path / "README.md").write_text("baseline\n")
    git("add", ".")
    git("commit", "-m", "baseline")
    base_sha = git("rev-parse", "HEAD")
    changed_file = tmp_path / changed_path
    changed_file.parent.mkdir(parents=True, exist_ok=True)
    changed_file.write_text("feature change\n")
    git("add", ".")
    git("commit", "-m", "feature")
    result = subprocess.run(
        [sys.executable, str(SCOPE_SCRIPT), "--branch", "feature/auth", "--base-ref", base_sha],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == expected_exit, result.stdout + result.stderr
