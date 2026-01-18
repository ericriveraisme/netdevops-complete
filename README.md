# NetDevOps Complete

A unified, production-ready network monitoring and automation portfolio. It combines:
- Project 1: NetBox (Source of Truth)
- Project 2: Monitoring Stack (Python health poller → InfluxDB → Grafana)
- Sprint 0 (Next): Terraform/Cloud foundations (Oracle/OCI, Kubernetes, CI/CD)

## What This Project Delivers
- Single canonical repo and runtime with clean docs and scripts
- Device health telemetry in real time (status + latency)
- Demo automation to drive device states for reproducible showcases
- Audit discipline (serials, asset tags, MACs) to prevent duplication
- Systemd-managed poller with auto-restart and no duplicate processes
- Professional documentation and verified dashboards

## Components
- NetBox (Docker): canonical device inventory and audit fields
- Health Poller (Python): polls NetBox devices, writes to InfluxDB
- InfluxDB (Docker): time-series storage (bucket: NetworkHealth)
- Grafana (Docker): dashboards (NetDevOps Device Health)
- Scripts: lab-up/shutdown, demo device manager, token refresh

## Current Status (2026-01-18)
- Verified end-to-end: NetBox → Poller → InfluxDB → Grafana
- All devices UP (demo) at 1.5 ms latency
- Datasource health OK; dashboard shows accurate data
- Canonical location enforced; legacy scripts deprecated

## Getting Started

Prerequisites:
- Linux host with Docker, Docker Compose, Python 3.12

Setup:
```bash
cd ~/netdevops-project2/unified  # symlink to ~/netdevops-complete
./project2-monitoring/lab-up.sh  # starts NetBox, InfluxDB, Grafana, poller
```

Demo controls:
```bash
cd ~/netdevops-complete/project2-monitoring
python demo_device_manager.py up       # set all to UP (10.0.0.x)
python demo_device_manager.py down     # set all to DOWN (192.0.2.x)
python demo_device_manager.py random   # randomize per device
python demo_device_manager.py status   # print current state
```

Poller management (systemd):
```bash
sudo systemctl status net-poller
sudo systemctl restart net-poller
journalctl -u net-poller -f
```

Grafana:
- URL: http://localhost:3000
- Dashboard: NetDevOps Device Health

InfluxDB quick checks:
```bash
docker exec -it project2-influxdb influx bucket list
# Latest status (last 5m)
docker exec -it project2-influxdb influx query 'from(bucket:"NetworkHealth") |> range(start:-5m) |> filter(fn:(r) => r._measurement == "device_health" and r._field == "status") |> group(columns:["device_name"]) |> last()'
```

## Documentation Map
- Monitoring stack details: project2-monitoring/README.md
- Audit strategy: project2-monitoring/DEVICE_AUDIT_STRATEGY.md
- Demo manager: project2-monitoring/DEMO_DEVICE_MANAGER.md
- Script consolidation: project2-monitoring/SCRIPT_MANAGEMENT.md
- Verification report: project2-monitoring/FINAL_VERIFICATION_REPORT.md

## Development Practices
- Secrets are never committed (.env, .env.local, .secrets/ ignored)
- Canonical runtime only from netdevops-complete; legacy paths blocked
- Testing isolation under project2-monitoring/tests/staging/
- Use systemd for long-running poller (no nohup background processes)

## What’s Next (Sprint 0)
- Initialize Terraform providers and remote state
- Stand up OCI/VPC networking, security groups
- Deploy InfluxDB/Grafana via IaC to cloud
- Wire CI/CD and basic unit/e2e tests

## Final Outcome
A portfolio-grade, cloud-ready NetDevOps platform with:
- Strong SoT discipline (NetBox)
- Observability pipeline (Poller → InfluxDB → Grafana)
- Automation-first delivery (Terraform, Ansible, CI/CD)
- Clear docs for reviewers and teammates.
