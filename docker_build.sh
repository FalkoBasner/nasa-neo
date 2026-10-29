#!/usr/bin/env bash
set -euo pipefail

GIT_SHA=$(git rev-parse --short HEAD)
IMAGE="nasa-neo:${GIT_SHA}"

docker build -t "$IMAGE" .
echo "Built $IMAGE"
