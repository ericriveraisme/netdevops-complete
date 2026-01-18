# Kubernetes Manifests

This folder holds Kubernetes YAML manifests for deployments, services, and config.

## Structure
- `manifests/`: app and infra manifests (namespaced by environment).

## Next Steps
1. Define cluster contexts and namespaces.
2. Add deployments/services/configmaps/secrets (use external secret managers; do not commit secrets).
3. Choose deployment method: `kubectl apply` or GitOps (e.g., Argo CD).
4. Add health checks and observability annotations.
