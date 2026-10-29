#!/usr/bin/env bash
set -euo pipefail

GIT_SHA=$(git rev-parse --short HEAD)
IMAGE="nasa-neo:${1:-$GIT_SHA}"

docker build -t "$IMAGE" .
echo "Built $IMAGE"
