# Next Steps and Roadmap

This guide summarizes immediate tasks and the broader roadmap, aligned with the AI onboarding.

## Immediate
- Commit scaffolding for `terraform/`, `k8s/`, and `oracle-cloud/` (done).
- Configure Terraform providers and remote state backend.
- Create `*.tfvars.example` templates; keep real `*.tfvars` local.
- Add initial Kubernetes manifests under `k8s/manifests/`.

## Sprint 0 (from AI Onboarding)
1. Initialize Terraform with providers and remote state.
2. Define base network (VPC/VCN, subnets, gateways, security groups) in OCI.
3. Plan InfluxDB/Grafana deployment via IaC.
4. Establish CI/CD pipeline (linting, tests, plan/apply gates).
5. Document runbooks and onboarding for cloud environment.

## References
- See [docs/AI_ONBOARDING.md](docs/AI_ONBOARDING.md) for context and principles.
