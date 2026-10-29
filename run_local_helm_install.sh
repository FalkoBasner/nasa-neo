#!/usr/bin/env bash
set -euo pipefail

./run_local_docker_build.sh

if helm status nasa-neo &>/dev/null; then
  helm upgrade nasa-neo helm/nasa-neo
else
  helm install nasa-neo helm/nasa-neo
fi
