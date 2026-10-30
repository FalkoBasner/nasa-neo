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

All scripts are callable from any directory.

| Script | Purpose |
|---|---|
| `tools/dev/run.sh` | Start the FastAPI server locally on port 8000 with hot-reload |
| `tools/dev/tests.sh [args]` | Run the test suite via pytest (extra args passed through) |
| `tools/dev/docker-build.sh` | Build Docker image tagged `nasa-neo:local` |
| `tools/gh/list-images.sh` | List published container images from ghcr.io with tags and timestamps |
| `tools/k8s/set-nasa-api-key.sh <key>` | Create or update the `nasa-api-key` cluster secret |
| `tools/k8s/release-info.sh` | Show Helm release history (revision, appVersion, status) |
| `tools/k8s/list-secrets.sh` | List all secrets in the nasa namespace |
| `tools/k8s/port-forward.sh [port]` | Port-forward the cluster service to localhost (default: 8008) |
| `tools/k8s/pod-info.sh` | Show pod status (phase, image, restarts, age) |

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

To get the kubeconfig value for the `KUBECONFIG` secret, follow the **Create GitHub Actions service account** step in One-time Cluster Setup below.

### One-time Cluster Setup

Run these once when setting up a new cluster.

**Create namespace:**

```bash
kubectl create namespace nasa
```

**Create NASA API key secret:**

```bash
tools/k8s/set-nasa-api-key.sh <your-nasa-api-key>
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

**Create GitHub Actions service account:**

Create a dedicated Kubernetes identity for CI with the minimum permissions needed to deploy:

```bash
# Service account — the identity CI authenticates as
kubectl create serviceaccount github-actions -n nasa

# RoleBinding — grants built-in 'edit' role: create/update/delete deployments,
# services, etc. within the nasa namespace only (no cluster-wide access)
kubectl create rolebinding github-actions \
  --clusterrole=edit \
  --serviceaccount=nasa:github-actions \
  -n nasa

# Token — JWT valid for 10 years; copy the output into kubeconfig-ci.yaml
kubectl create token github-actions -n nasa --duration=87600h
```

Build a static kubeconfig from the token output and set it as the `KUBECONFIG` GitHub Actions secret:

```bash
gh secret set KUBECONFIG --repo <github-owner>/<repo> < kubeconfig-ci.yaml
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

