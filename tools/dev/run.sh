#!/usr/bin/env bash
# Start the FastAPI dev server on port 8000 with hot-reload.
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

uv run uvicorn nasa_neo.main:app --reload