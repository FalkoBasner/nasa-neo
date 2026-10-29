# nasa-neo

A small web server wrapping the NASA NeoWs (Near Earth Object Web Service) API, containerized and deployed via Helm to a SAP Gardener Kubernetes cluster.

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Returns HTTP 200 |
| `GET` | `/docs` | Swagger UI (OpenAPI) |


## Development Setup

**Install [uv](https://docs.astral.sh/uv/getting-started/installation/)** (Python package manager).

```bash
# Install dependencies
uv sync

# Set your NASA API key
export NASA_API_KEY=your_key_here  # or use DEMO_KEY for lower rate limits
```

```bash
# Run the server
./run_local_dev.sh
```

| Script | Purpose |
|---|---|
| `run_local_dev.sh` | Start the FastAPI server locally on port 8080 with hot-reload |
| `run_tests.sh` | Run the test suite via pytest |

Get a NASA API key at https://api.nasa.gov/.

## Deployment

- **Registry:** ghcr.io
- **Cluster:** SAP Gardener trial cluster
- **CI/CD:** GitHub Actions → build Docker image → push to ghcr.io → `helm upgrade --install`
- Kubeconfig stored as a GitHub Actions secret
- Gardener kube-apiserver must be publicly reachable (`kubectl cluster-info`)
