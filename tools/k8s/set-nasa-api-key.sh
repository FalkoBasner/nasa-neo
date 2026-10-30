#!/usr/bin/env bash
# Create or update the nasa-api-key Kubernetes secret with the NASA API key.
set -euo pipefail

# shellcheck source=config.sh
source "$(dirname "${BASH_SOURCE[0]}")/config.sh"

if [[ -z "${1:-}" ]]; then
  echo "Usage: $(basename "$0") <nasa-api-key>"
  exit 1
fi

kubectl create secret generic nasa-api-key \
  --namespace "$NAMESPACE" \
  --from-literal=NASA_API_KEY="$1" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "Secret nasa-api-key upserted in namespace $NAMESPACE"
