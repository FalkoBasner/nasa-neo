#!/usr/bin/env bash
set -euo pipefail
gh api /user/packages/container/nasa-neo/versions \
  --jq '.[] | "\(.metadata.container.tags | join(", "))\t\(.updated_at)"'
