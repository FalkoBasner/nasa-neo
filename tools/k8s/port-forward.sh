#!/usr/bin/env bash
# Port-forwards the nasa-neo service to localhost.
#
# Usage: ./port-forward.sh [local-port]
#   local-port  Local port to bind (default: 8008)
set -euo pipefail

# shellcheck source=config.sh
source "$(dirname "$0")/config.sh"
LOCAL_PORT="${1:-8008}"
REMOTE_PORT="80"

"$(dirname "$0")/pod-info.sh"

SERVICE=$(kubectl get deployments -n "$NAMESPACE" \
  -l "$APP_LABEL" \
  --sort-by=.metadata.creationTimestamp \
  -o jsonpath='{.items[-1].metadata.name}')

echo ""
echo "Port-forwarding service/$SERVICE  $LOCAL_PORT -> $REMOTE_PORT"
echo "Press Ctrl+C to stop."
echo ""
kubectl port-forward -n "$NAMESPACE" "service/$SERVICE" "${LOCAL_PORT}:${REMOTE_PORT}"
