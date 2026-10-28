# nasa-neo

A small web server wrapping the NASA NeoWs (Near Earth Object Web Service) API, containerized and deployed via Helm to a SAP Gardener Kubernetes cluster.

## API Endpoints

| Endpoint | Behavior |
|---|---|
| `GET /health` | Returns HTTP 200 |
| `GET /neo/week/<N>` | Returns all NEO IDs for calendar week N (e.g. week 4 = 2026-01-19 to 2026-01-25) |
| `GET /neo/week/<N>?filter=hazardous` | Returns only NEO IDs where `is_potentially_hazardous_asteroid == true` |
| `GET /stats` | Returns total number of incoming requests across all endpoints |

Calendar weeks follow ISO 8601 (Monday–Sunday).

## Development Setup

**Install [uv](https://docs.astral.sh/uv/getting-started/installation/)** (Python package manager).

```bash
# Install dependencies
uv sync

# Set your NASA API key
export NASA_API_KEY=your_key_here  # or use DEMO_KEY for lower rate limits

# Run the server
uv run python main.py
```

Get a NASA API key at https://api.nasa.gov/.

## Deployment

- **Registry:** ghcr.io
- **Cluster:** SAP Gardener trial cluster
- **CI/CD:** GitHub Actions → build Docker image → push to ghcr.io → `helm upgrade --install`
- Kubeconfig stored as a GitHub Actions secret
- Gardener kube-apiserver must be publicly reachable (`kubectl cluster-info`)
