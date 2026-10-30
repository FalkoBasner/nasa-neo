#!/usr/bin/env bash
# Show status of nasa-neo pods in the cluster (phase, image, restarts, age).
set -euo pipefail

# shellcheck source=config.sh
source "$(dirname "$0")/config.sh"

kubectl get pods -n "$NAMESPACE" -l "$APP_LABEL" \
  -o custom-columns='POD:.metadata.name,STATUS:.status.phase,IMAGE:.spec.containers[0].image,RESTARTS:.status.containerStatuses[0].restartCount,AGE:.metadata.creationTimestamp'
