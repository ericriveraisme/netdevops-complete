# Oracle Cloud (OCI) Terraform

OCI infrastructure configuration via Terraform. Secrets and state are excluded from git.

## Files
- `providers.tf`: provider configuration (credentials via variables).
- `versions.tf`: Terraform and provider version constraints.
- `example.tfvars.example`: template for required variables.

## Ignored (by design)
- `.terraform/` cache
- `*.tfstate*` local state

## Next Steps
1. Fill `example.tfvars.example` with your tenancy details (keep as example; do not commit real values).
2. Add backend configuration for remote state.
3. Add core network resources (VCN/VPC, subnets, gateways, security lists/NSGs).
4. Run `terraform init`, then `terraform plan -var-file=example.tfvars.example` to validate.
