# nasa-neo

A small web server wrapping the NASA NeoWs (Near Earth Object Web Service) API, containerized and deployed via Helm to a SAP Gardener Kubernetes cluster.

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Returns HTTP 200 |
| `GET` | `/neo/week/<N>` | All NEO IDs for calendar week N |
| `GET` | `/neo/week/<N>?filter=hazardous` | Only potentially hazardous NEO IDs |
| `GET` | `/stats` | Total request count (resets on restart) |
| `GET` | `/docs` | Swagger UI (OpenAPI) |


## Development Setup

**Install [uv](https://docs.astral.sh/uv/getting-started/installation/)** (Python package manager).

```bash
uv sync
export NASA_API_KEY=your_key_here  # omit to use DEMO_KEY (rate limited)
```

| Script | Purpose |
|---|---|
| `run_local_dev.sh` | Start the FastAPI server locally on port 8000 with hot-reload |
| `run_tests.sh` | Run the test suite via pytest |
| `run_local_docker_build.sh` | Build Docker image tagged `nasa-neo:local` |
| `run_docker_build.sh` | Build Docker image tagged `nasa-neo:<git-sha>` (used in CI) |

Get a NASA API key at https://api.nasa.gov/.

## Deployment

- **Registry:** ghcr.io
- **Cluster:** SAP Gardener trial cluster
- **CI/CD:** GitHub Actions → build Docker image → push to ghcr.io → `helm upgrade --install`
- Kubeconfig stored as a GitHub Actions secret
- Gardener kube-apiserver must be publicly reachable (`kubectl cluster-info`)
