# Terraform IaC

This folder contains Terraform source for infrastructure-as-code. State files and local caches are ignored per `.gitignore`.

## Structure
- `modules/`: reusable Terraform modules.

## State Handling
- Local state (`*.tfstate*`) and `.terraform/` are not committed.
- Configure remote state (e.g., object storage) before collaborative work.

## Next Steps
1. Add `providers.tf` and backend config.
2. Create environment-specific `*.tfvars.example` files (real `*.tfvars` excluded).
3. Initialize: `terraform init`.
4. Validate and plan: `terraform fmt && terraform validate && terraform plan`.
5. Integrate CI/CD gates for `fmt`, `validate`, and `plan`.
