#!/usr/bin/env bash
# End-to-end smoke test of the built container image (not the dev bind-mount
# setup in docker-compose.yml): build, start, wait for Streamlit's health
# endpoint, import every runtime dependency inside the container, and fetch the
# app shell. Removes the container on exit. No credentials needed.
set -euo pipefail

cd "$(dirname "$0")/.."
image="azure-rbac-insight:e2e"
name="rbac-e2e-$$"
port="${E2E_PORT:-18501}"

cleanup() {
  status=$?
  if [ "$status" -ne 0 ]; then
    echo "==> FAILED (exit $status); container logs:"
    docker logs --tail 60 "$name" 2>&1 || true
  fi
  docker rm -f "$name" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "==> build image"
docker build -t "$image" .

echo "==> start container"
docker run -d --name "$name" -p "127.0.0.1:$port:8501" "$image" >/dev/null

echo "==> wait for health endpoint"
ok=0
for _ in $(seq 1 40); do
  if [ "$(curl -s --max-time 3 "http://127.0.0.1:$port/_stcore/health" || true)" = "ok" ]; then ok=1; break; fi
  [ "$(docker inspect -f '{{.State.Running}}' "$name")" = "true" ] || { echo "FAIL: container exited"; exit 1; }
  sleep 2
done
[ "$ok" -eq 1 ] || { echo "FAIL: health endpoint never returned ok"; exit 1; }

echo "==> runtime imports inside the container"
docker exec "$name" python -c "
import streamlit, pandas, plotly, matplotlib, numpy, azure.identity
import azure.mgmt.subscription, azure.mgmt.authorization, azure.mgmt.resource
print('imports ok, streamlit', streamlit.__version__)"

echo "==> app shell is served"
curl -fsS --max-time 10 "http://127.0.0.1:$port/" | grep -qi "<title>" \
  || { echo "FAIL: main page did not return an HTML shell"; exit 1; }

echo "==> app script runs headless (sample CSV through the real image)"
docker exec "$name" python -c "
from streamlit.testing.v1 import AppTest
at = AppTest.from_file('/app/app.py', default_timeout=60).run()
assert not at.exception, at.exception
print('app.py rendered without exceptions')"

echo "OK: end-to-end checks passed"
