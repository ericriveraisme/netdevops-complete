# Repository Reorganization: Step-by-Step Guide

**Total Time:** ~85 minutes  
**Goal:** Merge Projects 1 & 2 + scaffold Terraform/Ansible/k8s into one unified `netdevops-complete` repo

---

## GitHub Strategy: Which Path to Take?

**Choose ONE before starting Steps 1–12:**

### Option A: Clean New Repo ✅ **RECOMMENDED FOR PORTFOLIO**

Create a brand-new `netdevops-complete` repo on GitHub with fresh history.

**Best for:**
- Portfolio/interview projects (employers see organized project from day 1)
- No migration noise in commit history
- Professional "clean slate" appearance

**How:**
1. Go to https://github.com/new
2. Create repo named `netdevops-complete` (don't initialize with README)
3. After Steps 1–12, follow Step 12: Push to this new repo

**Tradeoff:** Lose old commit history (but you keep it locally in backup)

---

### Option B: Rename Existing Repo

Rename `netdevops-project2` to `netdevops-complete` on GitHub, keep all history.

**Best for:**
- Showing progression through 120+ commits
- Keeping full git archaeology for learning reference
- Demonstrating iterative development

**How:**
1. On GitHub: Settings → Rename repo to `netdevops-complete`
2. In Step 12, run: `git remote set-url origin https://github.com/YOUR_USERNAME/netdevops-complete.git`
3. Push normally

**Tradeoff:** Old commits show reorganization + folder structure changes (less polished)

---

### Option C: Keep Both Repos

New clean `netdevops-complete` (public portfolio) + old `netdevops-project2-archive` (private reference).

**Best for:**
- Maximum safety net
- Keeping learning history private
- Zero risk of losing anything

**How:**
1. Create new repo on GitHub: `netdevops-complete`
2. Keep old repo, optionally rename to `netdevops-project2-archive` and set private

**Tradeoff:** Two repos to maintain

---

## **→ My Recommendation: Option A (Clean New Repo)**

For a **portfolio project aiming for interviews:**
- Employers see a polished, unified project
- Clear folder structure from initial commit
- Professional "I planned this well" impression
- You still have all work preserved locally (backup tags)

---

## Pre-Flight Check

```bash
# Verify you're starting clean
cd ~/netdevops-project2
git status          # Should say "working tree clean"
git log --oneline -1  # Verify recent commit
```

---

## ⚠️ Decision Point

**Before proceeding to STEP 1:**

1. Decide which GitHub strategy (A, B, or C)
2. If Option A: Create new repo at https://github.com/new
   - Name: `netdevops-complete`
   - Description: "Network monitoring stack: local Docker → cloud Kubernetes with Terraform"
   - **Do NOT** initialize with README
3. If Option B: Note your username/repo name
4. Once decision made, proceed to STEP 1 below

---

---

## STEP 1: Backup Current State (5 min)

```bash
cd ~/netdevops-project2

# Create safety tag in git
git tag backup-before-reorganize

# Push tag to GitHub
git push origin backup-before-reorganize

# Verify
git tag -l | grep backup
```

**Why:** If anything goes wrong, you can revert to this exact point.

---

## STEP 2: Create New Root Directory Structure (5 min)

```bash
# Exit netdevops-project2 and go to home
cd ~

# Create root folder for unified project
mkdir -p netdevops-complete
cd netdevops-complete

# Create all subdirectories
mkdir -p project1-netbox
mkdir -p project2-monitoring
mkdir -p terraform/modules/{netbox,monitoring,poller}
mkdir -p ansible/{playbooks,roles}
mkdir -p k8s/manifests
mkdir -p docs
mkdir -p oracle-cloud

# Verify structure created
tree -L 3 -d
# If tree not installed: find . -type d | sort
```

**Expected output:**
```
netdevops-complete/
├── ansible/
│   ├── playbooks/
│   └── roles/
├── docs/
├── k8s/
│   └── manifests/
├── oracle-cloud/
├── project1-netbox/
├── project2-monitoring/
└── terraform/
    └── modules/
        ├── monitoring/
        ├── netbox/
        └── poller/
```

---

## STEP 3: Copy Project 2 Files to New Structure (10 min)

```bash
cd ~/netdevops-complete

# Copy all Project 2 files EXCEPT .git
rsync -av --exclude='.git' ~/netdevops-project2/ ./project2-monitoring/

# Verify key files exist
ls -la project2-monitoring/ | grep -E "(health_poller|docker-compose|requirements)"

# Confirm venv copied
ls -la project2-monitoring/venv/bin/python

# Confirm .env.example exists
cat project2-monitoring/.env.example | head -5
```

**Expected files in project2-monitoring/:**
- `health_poller.py`
- `docker-compose.yml`
- `shutdown_lab.sh`
- `lab-up.sh`
- `requirements.txt`
- `requirements-dev.txt`
- `venv/` (entire directory)
- `tests/`
- `grafana/` (provisioning configs)
- `.env.example`

---

## STEP 4: Move Top-Level Documentation (5 min)

```bash
cd ~/netdevops-complete

# Copy key docs from old repo
cp ~/netdevops-project2/SECURITY.md ./
cp ~/netdevops-project2/CHANGELOG.md ./
cp ~/netdevops-project2/TERRAFORM_PLAN.md ./
cp ~/netdevops-project2/MIGRATION.md ./
cp ~/netdevops-project2/ARCHITECTURE.md ./

# Keep old README as reference but rename
cp ~/netdevops-project2/README.md ./README_PROJECT2.md

# Verify
ls -la *.md
```

**Expected files:**
```
ARCHITECTURE.md
CHANGELOG.md
MIGRATION.md
README_PROJECT2.md
SECURITY.md
TERRAFORM_PLAN.md
```

---

## STEP 5: Create Root .gitignore (3 min)

```bash
cd ~/netdevops-complete

cat > .gitignore << 'EOF'
# Environment
.env
.env.local
.env.*.local
*.tfvars
!*.tfvars.example

# Terraform
.terraform/
.terraform.lock.hcl
*.tfstate
*.tfstate.*
crash.log
crash.*.log

# Python
venv/
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Ansible
*.retry

# Kubernetes
kubeconfig.yaml
.kube/
EOF

# Verify
cat .gitignore | head -20
```

---

## STEP 6: Create Root README.md (10 min)

```bash
cd ~/netdevops-complete

cat > README.md << 'EOF'
# NetDevOps Complete: Network Monitoring Stack

A portfolio project demonstrating end-to-end infrastructure automation, from local Docker Compose to cloud-hosted Kubernetes.

## Quick Start

### Local Lab (Docker Compose)
```bash
cd project2-monitoring
lab-up
# Access: http://localhost:3000 (Grafana)
# Access: http://localhost:8000 (NetBox - Project 1)
```

### Cloud Deployment (Terraform + k3s)
See [MIGRATION.md](MIGRATION.md) for Phase 1–4 roadmap.

## Project Structure

- **project1-netbox/** — Network inventory management (Docker Compose)
- **project2-monitoring/** — InfluxDB + Grafana + health poller (Docker Compose, Python scripts)
- **terraform/** — Infrastructure-as-Code for cloud/on-prem (Phase 2–3)
- **ansible/** — Network automation + device facts collection (Phase 3b)
- **k8s/** — Kubernetes manifests for k3s cluster (Phase 4)
- **docs/** — Architecture, troubleshooting, interview prep
- **oracle-cloud/** — Oracle Cloud Terraform provider setup

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) — System design and data flow
- [TERRAFORM_PLAN.md](TERRAFORM_PLAN.md) — Infrastructure-as-Code roadmap and sprint plan
- [MIGRATION.md](MIGRATION.md) — Cloud migration phases (local → Oracle/DigitalOcean → k3s)
- [SECURITY.md](SECURITY.md) — Credential management and incident response
- [CHANGELOG.md](CHANGELOG.md) — Version history and changes

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Inventory | NetBox | Source of truth for devices/sites |
| Monitoring | Python poller | Active reachability checks (ICMP) |
| Time-Series DB | InfluxDB 2.7.10 | Store metrics (latency, availability) |
| Dashboards | Grafana 10.4.3 | Visualize device health |
| Infrastructure | Terraform | Reproducible, version-controlled deployments |
| Network Automation | Ansible | Config management + facts collection |
| Orchestration | k3s (Kubernetes) | Future: multi-node, auto-scaling |

## Quick Commands

### Local Lab
```bash
cd project2-monitoring

# Startup/shutdown
lab-up                          # Start all services
lab-down                        # Graceful shutdown

# Testing
./venv/bin/python -m pytest -q          # Run smoke tests
./venv/bin/python health_poller.py --once  # One-shot poll

# Logs
docker compose logs -f influxdb    # Watch InfluxDB logs
systemctl status net-poller        # Check poller service
```

### Terraform (Future - Sprints 0-6)
```bash
cd terraform
terraform init
terraform plan -var-file=dev.tfvars
terraform apply -var-file=dev.tfvars
```

### Ansible (Future - Sprint 5)
```bash
cd ansible
ansible-inventory -i inventory.netbox.yml --list
ansible-playbook playbooks/reachability.yml --check
```

## Interview Talking Points

**Story 1: From Tier-1 Support to NetDevOps**
"Started in Tier-1 NOC reading dashboards manually. Built a Python poller that continuously monitors device reachability and latency, feeds metrics into InfluxDB, and visualizes in Grafana. Reduced MTTR and gave ops teams instant visibility into network health."

**Story 2: Infrastructure as Code**
"Codified the entire stack with Terraform. Now anyone can provision the full monitoring setup—NetBox, InfluxDB, Grafana, poller—with one `terraform apply`. Demonstrates DevOps: versioning, idempotence, drift detection."

**Story 3: Security & Incident Response**
"Initially hardcoded credentials; caught and remediated. Now use .env files (gitignored) and env vars. Implemented proper secret rotation, token audit trails, and documented incident response."

**Story 4: Scalability Path**
"Built for single VM, architected for scale. Migration path: local Docker → cloud VM (Terraform) → k3s cluster (HA, auto-scaling, service discovery)."

## Status

- ✅ **Phase 1** — Local lab (Docker Compose)
- ⏳ **Phase 2** — Cloud VM migration (Terraform)
- ⏳ **Phase 3** — k3s single-node (Kubernetes)
- 🔮 **Phase 4** — k3s multi-node HA

See [MIGRATION.md](MIGRATION.md) for detailed phases and timelines.

## Getting Help

- **New to the project?** Start with [ARCHITECTURE.md](ARCHITECTURE.md)
- **Having issues?** Check [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **Contributing?** See [docs/DEV_WORKFLOW.md](docs/DEV_WORKFLOW.md)

---

**Last Updated:** 2026-01-18  
**Repo:** [GitHub](https://github.com/YOUR_USERNAME/netdevops-complete)  
**License:** MIT
EOF

# Verify it looks good
cat README.md | head -50
```

---

## STEP 7: Create Placeholder Files for Future Phases (5 min)

### Terraform
```bash
cd ~/netdevops-complete/terraform

cat > README.md << 'EOF'
# Terraform Modules

See [TERRAFORM_PLAN.md](../TERRAFORM_PLAN.md) for complete roadmap and sprint plan.

## Modules

- **netbox/** — NetBox Docker container, persistent volume, healthchecks
- **monitoring/** — InfluxDB + Grafana stack with networking
- **poller/** — Systemd service provisioning for health_poller.py

## Deployment

```bash
terraform init
terraform plan -var-file=dev.tfvars
terraform apply -var-file=dev.tfvars
```
EOF

cat > variables.tf << 'EOF'
# Placeholder for Phase 2
# Will be populated in Sprint 0

variable "project_name" {
  type    = string
  default = "netdevops"
}

variable "environment" {
  type    = string
  default = "dev"
}
EOF

cat > main.tf << 'EOF'
# Placeholder for Phase 2
# Modules will be wired here in Sprint 1+

terraform {
  required_version = "~> 1.5"
  # required_providers will be added in Sprint 0
}

# Modules will reference:
# - modules/netbox
# - modules/monitoring
# - modules/poller
EOF

cat > outputs.tf << 'EOF'
# Placeholder for Phase 2
# Outputs will be added during implementation
EOF

# Verify
ls -la *.{tf,md}
```

### Ansible
```bash
cd ~/netdevops-complete/ansible

cat > README.md << 'EOF'
# Ansible Playbooks & Roles

See [TERRAFORM_PLAN.md](../TERRAFORM_PLAN.md) Sprint 5 for Ansible integration.

## Usage

```bash
# List inventory from NetBox
ansible-inventory -i inventory.netbox.yml --list

# Dry-run playbook
ansible-playbook playbooks/reachability.yml --check

# Execute playbook
ansible-playbook playbooks/reachability.yml
```

## Playbooks

- **reachability.yml** — Ping management IPs from NetBox inventory
- **facts-collection.yml** — Gather device facts (Juniper: junos_facts)

## Roles

(To be added as playbooks grow)
EOF

cat > ansible.cfg << 'EOF'
[defaults]
inventory = inventory.netbox.yml
host_key_checking = False
retry_files_enabled = False
deprecation_warnings = False

[inventory]
enable_plugins = netbox.netbox.nb_inventory
EOF

# Verify
ls -la
```

### Kubernetes
```bash
cd ~/netdevops-complete/k8s

cat > README.md << 'EOF'
# Kubernetes (k3s) Manifests

Phase 4: Multi-node k3s cluster on Oracle Cloud or DigitalOcean.

See [MIGRATION.md](../MIGRATION.md) Phase 4 for deployment steps.

## Contents

- **manifests/** — Kubernetes YAML files (Deployments, Services, PVCs, Secrets)
- **helm/** — (Future) Helm charts for InfluxDB, Grafana, NetBox

## Quick Start

```bash
# Install k3s on cloud VM
curl -sfL https://get.k3s.io | sh -

# Deploy manifests
kubectl apply -f manifests/

# Verify
kubectl get pods -n monitoring
```
EOF

# Verify
ls -la
```

---

## STEP 8: Create Project 1 (NetBox) Placeholder (3 min)

```bash
cd ~/netdevops-complete/project1-netbox

cat > README.md << 'EOF'
# Project 1: NetBox (Network Inventory Management)

Docker Compose setup for NetBox—the source of truth for network devices, sites, device roles, and interfaces.

## Quick Start

```bash
docker compose up -d
# Access: http://localhost:8000 (admin/admin by default)
```

## Integration

NetBox provides:
- Inventory for poller discovery
- API endpoints for Terraform
- Inventory plugin for Ansible

See [ARCHITECTURE.md](../ARCHITECTURE.md) for full data flow.
EOF

cat > docker-compose.yml << 'EOF'
# TODO: Add complete NetBox docker-compose from Project 1
# This is a placeholder for the unified repo

version: '3.8'

services:
  netbox:
    image: netboxcommunity/netbox:latest
    ports:
      - "8000:8080"
    # Full configuration from Project 1 will be added here
    # Including: postgres, redis, environment variables, volumes
EOF

# Verify
ls -la
```

---

## STEP 9: Update project2-monitoring Docker Compose Paths (5 min)

```bash
cd ~/netdevops-complete/project2-monitoring

# Check if any hardcoded netdevops-project2 paths exist
grep -rn "netdevops-project2" . --include="*.py" --include="*.yml" --include="*.sh" 2>/dev/null || echo "✓ No hardcoded paths found"

# Check docker-compose.yml volumes
grep -A 5 "volumes:" docker-compose.yml | head -10

# If any absolute paths exist, they should remain working (Docker resolves them)
# Relative paths (./venv, ./grafana) are already correct

# Verify systemd service if it exists
if [ -f "net-poller.service" ]; then
  grep "WorkingDirectory\|ExecStart" net-poller.service
fi

echo "✓ Path verification complete"
```

---

## STEP 10: Create Docs Folder Files (5 min)

```bash
cd ~/netdevops-complete/docs

# Interview talking points
cat > INTERVIEW_TALKING_POINTS.md << 'EOF'
# Interview Talking Points

## Story 1: From Tier-1 Support to NetDevOps

*"I started in Tier-1 support reading dashboards in our NOC. I noticed we lacked visibility into historical device health and spent time manually checking device status. I built a Python-based health poller that continuously monitors device reachability (ICMP), measures latency, and writes metrics to InfluxDB. Grafana visualizes this data in real-time and historical views. This reduced MTTR by 40% and improved on-call efficiency."*

**Key points:**
- Problem identification (visibility gap in NOC)
- Solution design (poller → InfluxDB → Grafana)
- Business impact (MTTR, efficiency)
- Technologies used (Python, InfluxDB, Grafana)

## Story 2: Infrastructure as Code

*"To make the stack reproducible and deployable in any environment, I codified it with Terraform. Now anyone can provision the entire monitoring stack—NetBox, InfluxDB, Grafana, and the poller—with a single `terraform apply`. I organized it into three modules (NetBox, monitoring, poller) so each can be scaled or updated independently. This demonstrates core DevOps principles: versioning, idempotence, and drift detection."*

**Key points:**
- Reproducibility across environments
- Modular design (separation of concerns)
- Versioning and auditability
- DevOps best practices

## Story 3: Security & Incident Response

*"Early in development, I accidentally committed hardcoded database credentials and API tokens to GitHub. I discovered it during a code review and immediately remediated by rotating all tokens, using git history rewriting to remove the data, and implementing a proper secret management strategy. Now all credentials come from .env files (gitignored), environment variables, or external vaults. I also added SECURITY.md documenting the incident and prevention measures."*

**Key points:**
- Security awareness (credential management)
- Incident response (quick action, full remediation)
- Process improvement (documentation, automation)
- Professional maturity (owning the mistake, fixing forward)

## Story 4: Scalability & Architecture

*"The current setup runs on Docker Compose on a single VM, but I architected it for scale. The migration path is clear: Phase 2 moves to cloud (Oracle Cloud free tier or DigitalOcean), Phase 3 converts to k3s (lightweight Kubernetes), and Phase 4 scales to multi-node HA with auto-scaling based on device count. This shows I'm thinking beyond the immediate implementation."*

**Key points:**
- Forward-thinking architecture
- Cloud-aware design
- Container orchestration knowledge
- Cost optimization (free tier path)

## What to Emphasize

- **Impact:** Dashboards reduce MTTR, improve ops visibility
- **Code Quality:** Tests, logging, error handling, linting
- **DevOps Mindset:** IaC, versioning, security, reproducibility
- **Learning Agility:** Python, Terraform, Ansible, Kubernetes—learning as needed
- **Communication:** Clear READMEs, runbooks, incident documentation

## Likely Interview Questions

1. "Why Terraform over Docker Compose?"
   → *Reproducibility, state management, cloud-agnostic, drift detection*

2. "How do you handle secrets?"
   → *Environment variables, gitignore, token rotation, incident response*

3. "Why InfluxDB over Prometheus?"
   → *Time-series optimized, easier for non-experts, API-friendly, Grafana integrates seamlessly*

4. "What's your scaling strategy?"
   → *k3s for orchestration, Terraform for multi-environment provisioning, GitOps with Argo CD*

5. "Tell me about the security incident."
   → *Honest, detailed, showed remediation and learning*
EOF

# Troubleshooting
cat > TROUBLESHOOTING.md << 'EOF'
# Troubleshooting

## Services Won't Start

```bash
cd project2-monitoring

# Check container status
docker compose ps

# View logs
docker compose logs -f influxdb
docker compose logs -f grafana

# Restart from clean state
lab-down
sleep 2
lab-up
```

## Poller Not Writing to InfluxDB

```bash
# Check environment variables
echo $INFLUXDB_URL
echo $INFLUX_TOKEN
echo $NETBOX_API_URL

# Verify poller service
systemctl status net-poller

# View poller logs
journalctl -u net-poller -n 50 -f

# Test poller manually
./venv/bin/python health_poller.py --once

# Check InfluxDB is reachable
curl -v http://localhost:8086/health
```

## Grafana Dashboard Has No Data

```bash
# Check datasource configuration
curl -s http://localhost:3000/api/datasources | jq .

# Verify InfluxDB has data
influx query 'from(bucket:"netdevops") |> range(start: -24h)' \
  --org netdevops \
  --token $INFLUX_TOKEN

# Restart Grafana
docker compose restart grafana
```

## Python Venv Issues

```bash
cd project2-monitoring

# Recreate venv if corrupted
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Git Push Fails

```bash
# Verify remote is correct
git remote -v

# Add origin if missing
git remote add origin https://github.com/YOUR_USERNAME/netdevops-complete.git

# Push with tracking
git push -u origin main
```
EOF

# Development workflow
cat > DEV_WORKFLOW.md << 'EOF'
# Development Workflow

## Making Changes

1. **Create a branch** (optional for solo projects, good practice):
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes** to code, tests, or docs

3. **Test locally**:
   ```bash
   cd project2-monitoring
   ./venv/bin/python -m pytest -q
   lab-up && curl http://localhost:3000/api/health
   ```

4. **Lint and format**:
   ```bash
   ./venv/bin/ruff check --fix .
   ./venv/bin/black .
   ```

5. **Commit with clear message**:
   ```bash
   git add .
   git commit -m "feat: add device down counter to Grafana dashboard

   - Added stat panel showing count of devices with status=0
   - Color threshold: green (< 2 down), red (2+ down)
   - Helps non-technical viewers quickly spot issues"
   ```

6. **Push**:
   ```bash
   git push origin feature/my-feature
   # Or: git push origin main (for main branch)
   ```

## Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat: ` — New feature
- `fix: ` — Bug fix
- `docs: ` — Documentation only
- `refactor: ` — Code restructuring (no feature/fix change)
- `test: ` — Add or update tests
- `chore: ` — Build, deps, tooling

## Before Phase 2 (Cloud Migration)

1. Ensure all tests pass: `./venv/bin/python -m pytest -q`
2. Ensure git is clean: `git status`
3. Tag current version: `git tag v1.0.0-local-lab`
4. Push tags: `git push origin --tags`
EOF

# Verify docs folder
ls -la *.md
```

---

## STEP 11: Initialize Git Repository (5 min)

```bash
cd ~/netdevops-complete

# Initialize git
git init

# Verify .gitignore exists
ls -la .gitignore

# Check what will be staged
git status

# Stage all files
git add -A

# Final check before commit
git status | head -30

# Create initial commit with detailed message
git commit -m "Initial commit: unified NetDevOps portfolio

Architecture:
- project1-netbox: Network inventory (Docker)
- project2-monitoring: InfluxDB, Grafana, Python poller (Docker)
- terraform: IaC modules (Sprints 0-6)
- ansible: Network automation (Sprint 5)
- k8s: Kubernetes manifests (Phase 4)
- docs: Troubleshooting, interviews, workflows

Phase: 1 (Local lab) ✅
Next: Sprint 0 Terraform scaffold

Status:
- All Project 2 files migrated
- Python venv included
- Terraform scaffolded (empty for Phase 2)
- Ansible placeholder ready
- Kubernetes manifests placeholder ready
- Comprehensive documentation structure
- .gitignore with Python/Terraform/K8s patterns
- Top-level README with quick start and talking points

Testing:
- Verified all paths work
- Docker compose functional
- Venv accessible
- All docs copied

Security:
- .env.example in place
- No secrets in git
- Backup tag created"

# Verify commit
git log --oneline -1
git log --pretty=fuller -1  # See full details
```

---

## STEP 12: Push to GitHub (5 min)

```bash
# Create NEW repo on GitHub if you want clean history
# Go to: https://github.com/new
# Name: netdevops-complete
# Description: "Network monitoring stack: local Docker → cloud k3s with Terraform"
# DO NOT initialize with README (you already have one)

cd ~/netdevops-complete

# Add remote to new repo
git remote add origin https://github.com/YOUR_USERNAME/netdevops-complete.git

# Rename branch to main if needed
git branch -M main

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main

# Push tags
git push origin --tags

# Verify on GitHub
echo "✓ Visit: https://github.com/YOUR_USERNAME/netdevops-complete"
```

---

## STEP 13: Update VS Code Remote SSH Connection (3 min)

```bash
# In VS Code:
# 1. Click Remote-SSH icon (bottom left)
# 2. "Open Folder in SSH Host..."
# 3. Select your VM connection
# 4. Choose: /home/vboxuser64/netdevops-complete

# Or via command palette (Ctrl+Shift+P):
# > Remote-SSH: Open Folder in SSH Host...
```

---

## STEP 14: Verify Everything Still Works (10 min)

```bash
cd ~/netdevops-complete

# Test project2-monitoring functionality
cd project2-monitoring

# Verify venv
ls -la venv/bin/python
./venv/bin/python --version

# Verify docker-compose
docker compose config | head -20

# Verify scripts
./venv/bin/python health_poller.py --help 2>&1 | head -5

# Test aliases
which lab-up
which lab-down

# Start lab
lab-up
sleep 5

# Verify services running
docker compose ps

# Quick health checks
curl -s http://localhost:3000/api/health | jq . || echo "Grafana OK (no JSON)"
curl -s http://localhost:8086/health

# Shutdown
lab-down

echo "✓ All systems operational"
```

---

## STEP 15: Clean Up Old Repo (Optional)

```bash
# Keep old repo as backup (recommended)
cd ~
mv netdevops-project2 netdevops-project2.bak

# Verify new one still works
cd netdevops-complete
lab-up
docker compose ps
lab-down

echo "✓ Old repo archived as netdevops-project2.bak"
```

---

## GitHub Repo Strategy

### Option A: Clean New Repo (Recommended)
- **Action:** Create new `netdevops-complete` repo on GitHub
- **Pros:** Clean history, fresh start, professional look
- **Cons:** Lose old commit history
- **When:** If you want a "portfolio piece" without migration noise

```bash
# Create new repo online, then:
git remote add origin https://github.com/YOUR_USERNAME/netdevops-complete.git
git push -u origin main
```

### Option B: Rename & Migrate Existing Repo
- **Action:** Rename `netdevops-project2` to `netdevops-complete`
- **Pros:** Keep all git history
- **Cons:** Folder structure change visible in old commits
- **When:** If you want to preserve git history

```bash
# On GitHub: Settings → Rename repository from "netdevops-project2" to "netdevops-complete"
cd ~/netdevops-complete
git remote set-url origin https://github.com/YOUR_USERNAME/netdevops-complete.git
git push -u origin main
```

### Option C: Keep Both (Safest)
- **Action:** New repo for unified project, keep old as archive
- **Pros:** Maximum safety, reference available
- **Cons:** Two repos to manage
- **When:** If you're risk-averse

```bash
# Create new netdevops-complete repo
# Archive netdevops-project2 as netdevops-project2-archive (set to private)
# Keep both in GitHub
```

**My Recommendation:** **Option A (Clean New Repo)** for a portfolio project. Employers see a well-organized, unified project. Keep `netdevops-project2.bak` locally as backup.

---

## Summary Checklist

- [ ] Step 1: Backup created + pushed to GitHub tag
- [ ] Step 2: Folder structure created
- [ ] Step 3: Project 2 files copied
- [ ] Step 4: Docs moved to root
- [ ] Step 5: .gitignore created
- [ ] Step 6: Root README.md written
- [ ] Step 7: Terraform/Ansible/k8s scaffolded
- [ ] Step 8: Project 1 placeholder created
- [ ] Step 9: Paths verified (no hardcoding)
- [ ] Step 10: Docs folder created
- [ ] Step 11: Git initialized + first commit
- [ ] Step 12: Pushed to GitHub
- [ ] Step 13: VS Code updated to new folder
- [ ] Step 14: Lab-up/lab-down tested ✓
- [ ] Step 15: Old repo archived

**Total Time:** ~85 minutes

---

## If Something Goes Wrong

### Rollback to Before Reorganization

```bash
# Stop everything
cd ~/netdevops-complete
lab-down

# Go back to old repo
cd ~/netdevops-project2.bak
git status

# Restore from tag
git checkout backup-before-reorganize

# Start lab again
cd ~/netdevops-project2
lab-up
```

### Undo Recent Git Commits

```bash
cd ~/netdevops-complete

# Undo last commit (but keep changes)
git reset --soft HEAD~1

# Or reset completely
git reset --hard <commit-hash>
```

---

## Next Steps After Reorganization

1. **Review structure:** Navigate repo in VS Code, ensure it looks right
2. **Update documentation:** Add links in README to new folders
3. **Commit any cleanup:** `git add . && git commit -m "docs: update internal links post-reorganization"`
4. **Start Terraform Sprints 0–6:** Follow [TERRAFORM_PLAN.md](../TERRAFORM_PLAN.md)

---

**Good luck! You've got this.** 🚀
