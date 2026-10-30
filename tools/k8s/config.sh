# Shared configuration for dev scripts.
# Source this file — do not execute it directly.

NAMESPACE="nasa"
APP_LABEL="app=nasa-neo"
KUBE_CONTEXT="garden-nasa--r3qxqvepx6-external"

if [[ $(kubectl config current-context) != "$KUBE_CONTEXT" ]]; then
  kubectl config use-context "$KUBE_CONTEXT"
fi
