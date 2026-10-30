#!/usr/bin/env bash
# Run the pytest test suite. Any extra arguments are passed through to pytest.
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

uv run pytest "$@"