#!/usr/bin/env bash
set -euo pipefail

docker rmi nasa-neo:local 2>/dev/null || true
./run_docker_build.sh local

docker tag nasa-neo:local localhost:5000/nasa-neo:local
docker push localhost:5000/nasa-neo:local
