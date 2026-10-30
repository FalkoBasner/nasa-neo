#!/usr/bin/env bash
# List published nasa-neo container images from ghcr.io with tags and timestamps.
set -euo pipefail
gh api /user/packages/container/nasa-neo/versions \
  --jq '.[] | "\(.metadata.container.tags | join(", "))\t\(.updated_at)"'