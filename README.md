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

**Install [asdf](https://asdf-vm.com/guide/getting-started.html)** for tool version management, then:

```bash
asdf plugin add uv https://github.com/asdf-community/asdf-uv.git
asdf plugin add helm https://github.com/Antiarchitect/asdf-helm.git
asdf install
```

This installs all tools pinned in `.tool-versions` (`uv`, `helm`).

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

### One-time Repository Setup

**Add GitHub Actions secrets** under Settings → Secrets and variables → Actions:

| Secret | Value |
|---|---|
| `KUBECONFIG` | Shoot cluster kubeconfig (see below) |
| `NASA_API_KEY` | Your NASA API key from https://api.nasa.gov/ |

To get the kubeconfig value for the `KUBECONFIG` secret:

```bash
kubectl config view --raw --minify --context=<your-shoot-context>
```

Paste the full output as the secret value.

### One-time Cluster Setup

Run these once when setting up a new cluster.

**Create namespace:**

```bash
kubectl create namespace nasa
```

**Create ghcr.io pull secret:**

Create a GitHub PAT with `read:packages` scope, then:

```bash
kubectl create secret docker-registry ghcr-pull-secret \
  --docker-server=ghcr.io \
  --docker-username=<github-username> \
  --docker-password=<github-pat> \
  --namespace nasa
```

**Rotate pull secret:**

```bash
kubectl create secret docker-registry ghcr-pull-secret \
  --docker-server=ghcr.io \
  --docker-username=<github-username> \
  --docker-password=<new-github-pat> \
  --namespace nasa \
  --dry-run=client -o yaml | kubectl apply -f -
```

