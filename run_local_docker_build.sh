#!/usr/bin/env bash
set -euo pipefail

docker rmi nasa-neo:local 2>/dev/null || true
./run_docker_build.sh local
