# Next Steps and Roadmap

This guide summarizes immediate tasks and the broader roadmap, aligned with the AI onboarding.

## Immediate
- Commit scaffolding for `terraform/`, `k8s/`, and `oracle-cloud/` (done).
- Configure Terraform providers and remote state backend.
- Create `*.tfvars.example` templates; keep real `*.tfvars` local.
- Add initial Kubernetes manifests under `k8s/manifests/`.

## Process Overview
- Terraform (OCI): Define providers in [oracle-cloud/providers.tf](oracle-cloud/providers.tf) and versions in [oracle-cloud/versions.tf](oracle-cloud/versions.tf). Configure remote state using [oracle-cloud/backend.tf.example](oracle-cloud/backend.tf.example) (rename to `backend.tf` locally). Keep secrets in `example.tfvars.example` templates; do not commit real values.
- Modules: Add reusable code in [terraform/modules](terraform/modules). Reference modules from environment-specific stacks in [oracle-cloud](oracle-cloud).
- Kubernetes: Manage declarative manifests under [k8s/manifests](k8s/manifests). Start with [namespace-netdevops.yaml](k8s/manifests/namespace-netdevops.yaml) and [deployment-placeholder.yaml](k8s/manifests/deployment-placeholder.yaml). Tie service endpoints to resources provisioned by Terraform.
- CI/CD: Add gates for `terraform fmt`, `validate`, and `plan`; add `kubectl diff` or GitOps validations. Use environment overlays and never commit secrets.

## How This Builds on Current Work
- Monitoring pipeline is verified locally; IaC will codify the same stack for reproducible environments.
- Terraform will provision network and platform resources; Kubernetes will host workloads (e.g., Grafana/Influx or app services) using outputs from Terraform.
- `.gitignore` patterns already prevent committing state/secrets, aligning with secure operational practices outlined in [docs/AI_ONBOARDING.md](docs/AI_ONBOARDING.md).


## Sprint 0 (from AI Onboarding)
1. Initialize Terraform with providers and remote state.
2. Define base network (VPC/VCN, subnets, gateways, security groups) in OCI.
3. Plan InfluxDB/Grafana deployment via IaC.
4. Establish CI/CD pipeline (linting, tests, plan/apply gates).
5. Document runbooks and onboarding for cloud environment.

## References
- See [docs/AI_ONBOARDING.md](docs/AI_ONBOARDING.md) for context and principles.
