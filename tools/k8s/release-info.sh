#!/usr/bin/env bash
# Show the current Helm release info for nasa-neo (revision, chart, appVersion, status).
set -euo pipefail

# shellcheck source=config.sh
source "$(dirname "${BASH_SOURCE[0]}")/config.sh"

helm history nasa-neo --namespace "$NAMESPACE"
