# nasa-neo — AI Instructions

## NASA API

- **Feed endpoint:** `GET https://api.nasa.gov/neo/rest/v1/feed?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&api_key=KEY`
- Max 7-day range per request — maps to one calendar week
- Key response fields: `id`, `neo_reference_id`, `is_potentially_hazardous_asteroid`
- Response grouped by date under `near_earth_objects`

## Required Endpoints

| Endpoint | Behavior |
|---|---|
| `GET /health` | Returns HTTP 200 |
| `GET /neo/week/<N>` | Returns all NEO IDs for calendar week N (e.g. week 4 = 2026-01-19 to 2026-01-25) |
| `GET /neo/week/<N>?filter=hazardous` | Returns only NEO IDs where `is_potentially_hazardous_asteroid == true` |
| `GET /stats` | Returns total number of incoming requests across all endpoints |

## Implementation Notes

- Calendar week uses ISO 8601: Monday–Sunday
- Week-to-date conversion must handle year boundaries
- `/stats` counter is in-memory (resets on pod restart) — acceptable for this task

## Tech Stack

- **Language:** Python 3.12 — current stable LTS, broad library support, 3.13 still has rough edges
- **Framework:** FastAPI — minimal boilerplate, async, auto OpenAPI docs at `/docs`
- **Package manager:** uv

## Project Structure

```
nasa-neo/
├── main.go (or main.py)
├── Dockerfile
├── helm/
│   └── nasa-neo/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           └── ingress.yaml
└── .github/
    └── workflows/
        └── deploy.yml
```

## Constraints

- Not expected to be production-ready