"""Reject feature PRs that also change shared files or another feature."""

import argparse
import subprocess
import sys

ALLOWED_DIRECTORIES = {
    "feature/auth": ("app/features/auth/", "tests/auth/"),
    "feature/catalog": ("app/features/catalog/", "tests/catalog/"),
    "feature/booking": ("app/features/booking/", "tests/booking/"),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", required=True)
    parser.add_argument("--base-ref", required=True)
    args = parser.parse_args()
    allowed = ALLOWED_DIRECTORIES.get(args.branch)
    if allowed is None:
        print("Shared/integration PR: scope check does not apply")
        return 0
    result = subprocess.run(
        ["git", "diff", "--name-only", "-z", f"{args.base_ref}...HEAD"],
        check=True,
        capture_output=True,
    )
    changed_paths = result.stdout.decode().split("\0")
    blocked = [path for path in changed_paths if path and not path.startswith(allowed)]
    if blocked:
        print("Feature PR changes files outside its ownership:")
        print("\n".join(blocked))
        print("Move shared changes into a chore/foundation PR and merge it first.")
        return 1
    print("Feature scope passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
