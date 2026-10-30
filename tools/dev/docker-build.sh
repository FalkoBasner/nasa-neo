#!/usr/bin/env bash
# Build the Docker image locally, tagged nasa-neo:local.
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

docker rmi nasa-neo:local 2>/dev/null || true
docker build -t nasa-neo:local "$PROJECT_ROOT"
echo "Built nasa-neo:local"
