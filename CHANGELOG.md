# Changelog
All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [0.2.0] - 2026-01-18
### Added
- Demo device manager (`project2-monitoring/demo_device_manager.py`) with `up/down/random/status`.
- Audit trail script (`project2-monitoring/add_audit_fields.py`) to set serials, asset tags, MACs.
- Documentation: `DEVICE_AUDIT_STRATEGY.md`, `SCRIPT_MANAGEMENT.md`, `FINAL_VERIFICATION_REPORT.md`.
- Systemd service (`project2-monitoring/systemd/net-poller.service`) for auto-restart and single instance.
- Testing isolation under `project2-monitoring/tests/staging` with `.env.test` and lock mechanism.
- Token refresh script (`project2-monitoring/scripts/refresh_influx_token.sh`) to avoid manual token handling.

### Changed
- `health_poller.py`: Added demo mode (10.0.0.x → UP, 192.0.2.x → DOWN), removed duplicate logging, restored "(demo)" prefix.
- `lab-up.sh` and `shutdown_lab.sh`: Enforce canonical location; start/stop poller via systemd; kill orphaned processes.
- Grafana datasource provisioning to use env vars; validated datasource health.

### Fixed
- Duplicate poller processes causing inconsistent Influx data.
- Unreliable token usage; switched to `.env.local` overlay and container token sync.
- Primary IP persistence via `.save()` (NetBox API) when updating devices.

### Security
- Ensured `.env`, `.env.local`, `.secrets/` ignored by git.

## [0.1.0] - 2026-01-17
### Added
- Unified repo structure (`netdevops-complete`) with symlink from `netdevops-project2/unified`.
- Initial monitoring stack (Docker Compose for InfluxDB + Grafana).
- Health poller base implementation writing to Influx.
- NetBox CSV import and bulk provision scripts.

### Known Issues
- Early runs used multiple pollers; led to mixed data.
- Grafana dashboards initially unauthorized due to token mismatch.
