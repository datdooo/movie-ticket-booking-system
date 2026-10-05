#!/usr/bin/env bash
set -euo pipefail

mkdir -p artifacts
python -m scripts.seed

report_prefix="${LOAD_REPORT_PREFIX:-artifacts/locust-${LOAD_USERS:-50}u}"
mkdir -p "$(dirname "$report_prefix")"
export LOAD_PROFILE="${LOAD_PROFILE:-full}"
case "$LOAD_PROFILE" in
  full|catalog) ;;
  *) echo "LOAD_PROFILE must be full or catalog" >&2; exit 1 ;;
esac
python - "$report_prefix" <<'PY'
import json
import os
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
metadata = {
    "commit_sha": commit.stdout.strip() if commit.returncode == 0 else "unavailable",
    "started_at": datetime.now(UTC).isoformat(),
    "users": os.getenv("LOAD_USERS", "50"),
    "spawn_rate": os.getenv("LOAD_SPAWN_RATE", "5"),
    "run_time": os.getenv("LOAD_RUN_TIME", "60s"),
    "profile": os.environ["LOAD_PROFILE"],
    "cpu_count": os.cpu_count(),
    "platform": platform.platform(),
}
Path(sys.argv[1] + '-metadata.json').write_text(json.dumps(metadata, indent=2))
PY

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 >artifacts/server.log 2>&1 &
server_pid=$!
trap 'kill "$server_pid" 2>/dev/null || true' EXIT

ready=false
for _ in $(seq 1 30); do
  if ! kill -0 "$server_pid" 2>/dev/null; then
    cat artifacts/server.log
    echo "API process exited before the load test" >&2
    exit 1
  fi
  if python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" 2>/dev/null; then
    ready=true
    break
  fi
  sleep 1
done

if [ "$ready" != true ]; then
  echo "API did not become healthy; load test aborted" >&2
  exit 1
fi

python -m locust \
  -f tests/load/locustfile.py \
  --host http://127.0.0.1:8000 \
  --headless \
  --users "${LOAD_USERS:-50}" \
  --spawn-rate "${LOAD_SPAWN_RATE:-5}" \
  --run-time "${LOAD_RUN_TIME:-60s}" \
  --exit-code-on-error 1 \
  --html "$report_prefix-report.html" \
  --csv "$report_prefix"

python - "$report_prefix" <<'PY'
import csv
import sys
from pathlib import Path

with Path(sys.argv[1] + '_stats.csv').open() as stream:
    totals = next(row for row in csv.DictReader(stream) if row['Name'] == 'Aggregated')
if int(totals['Request Count']) == 0:
    raise SystemExit('No requests were measured; this is not a valid load result')
if int(totals['Failure Count']) != 0:
    raise SystemExit('Load test contains failed requests')
PY
