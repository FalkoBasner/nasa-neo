#!/usr/bin/env bash
# List Kubernetes secrets in the nasa namespace.
set -euo pipefail

# shellcheck source=config.sh
source "$(dirname "${BASH_SOURCE[0]}")/config.sh"

kubectl get secrets -n "$NAMESPACE"
