#!/usr/bin/env bash
set -euo pipefail

IMAGE="nasa-neo:local"

docker build -t "$IMAGE" .
echo "Built $IMAGE"
