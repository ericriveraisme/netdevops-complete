# Script Management & Deprecation Strategy

## Canonical Script Locations

All production and development scripts are managed from:
```
/home/vboxuser64/netdevops-project2/unified/project2-monitoring/
```

**Canonical Scripts:**
- `health_poller.py` - NetDevOps health poller with demo mode
- `lab-up.sh` - Lab startup with systemd service coordination
- `shutdown_lab.sh` - Lab graceful shutdown
- `demo_device_manager.py` - Device UP/DOWN/random/status control
- `add_audit_fields.py` - Bulk audit field management

## Deprecated Locations (DO NOT USE)

❌ `/home/vboxuser64/netdevops-project2/` (root level)
- `health_poller.py` (OLD, no demo mode)
- `lab-up.sh` (OLD)
- `shutdown_lab.sh` (OLD)

❌ `/home/vboxuser64/netdevops-complete/project2-monitoring/`
- All scripts (LEGACY from incomplete migration)

**Status:** These will be archived but kept for reference. Never run directly.

## Environment Isolation

### Production/Lab Environment
- Location: `/home/vboxuser64/netdevops-project2/unified/project2-monitoring/`
- Virtual Env: `venv/` (only for ad-hoc Python scripts; see "When to use venv" below)
- Configuration: `.env`
- Docker Compose: `docker-compose.yml` (Project 1 NetBox + Project 2 monitoring)

### Testing/Staging Environment
- Location: `/home/vboxuser64/netdevops-project2/unified/project2-monitoring/tests/staging/`
- Virtual Env: `tests/staging/venv_test/` (only for isolated test code; see "When to use venv" below)
- Configuration: `tests/staging/.env.test`
- Docker Compose: `tests/staging/docker-compose.test.yml`
- Lock File: `tests/staging/.test_lock` (prevents concurrent runs)
- Logs: `tests/staging/test.log`

## When to Use venv (Orchestration vs. Ad-hoc Work)

### ❌ DO NOT use venv for orchestration scripts
**Scripts that manage the lab (no venv needed):**
- `lab-up.sh` - Run bare from canonical location
- `shutdown_lab.sh` - Run bare from canonical location

These are pure bash scripts that control Docker and systemd. Run them directly:
```bash
cd /home/vboxuser64/netdevops-project2/unified/project2-monitoring
./lab-up.sh
./shutdown_lab.sh
```

### ✅ USE venv only for ad-hoc Python utilities
**When you need to run Python code directly (use venv):**
- `demo_device_manager.py` - Controlling device state manually
- `add_audit_fields.py` - Bulk operations on devices
- `csv_import.py` - Data imports or one-off scripts
- Any new utility scripts you write

**Example workflow:**
```bash
cd /home/vboxuser64/netdevops-project2/unified/project2-monitoring
source venv/bin/activate                    # Activate venv
python demo_device_manager.py status        # Run utility
python add_audit_fields.py --help           # Ad-hoc script
deactivate                                  # Exit venv
```

### ✅ Systemd service auto-handles Python environment
**The `health_poller.py` (running via systemd) does NOT require manual venv activation:**
- Systemd service manages Python environment internally
- Service config in `systemd/net-poller.service` specifies the full path
- Started/stopped via `./lab-up.sh` and `./shutdown_lab.sh`
- Logs viewable via: `journalctl -u net-poller -f`

**You don't activate venv to start the poller—the scripts do that automatically.**

## Concurrent Execution Prevention

### Lock Mechanism
All scripts check for lock file before execution:
```bash
LOCK_FILE=".test_lock"
if [ -f "$LOCK_FILE" ]; then
    echo "ERROR: Test already running. Remove $LOCK_FILE to force reset."
    exit 1
fi
trap "rm -f $LOCK_FILE" EXIT
touch "$LOCK_FILE"
```

### Auto-restart on Reboot
Health poller runs via systemd service (not background processes):
- Service: `net-poller.service`
- Type: `simple`
- ExecStart: `python /home/vboxuser64/netdevops-project2/unified/project2-monitoring/health_poller.py`
- Restart: `on-failure`
- RestartSec: `5`

**Never start health_poller via:**
- `nohup python health_poller.py &` (old method, prevents cleanup)
- Background processes in lab-up.sh (can create duplicates)

## Code Review & Testing Workflow

### Before Committing
1. Make changes in staging environment (`tests/staging/`)
2. Run isolated tests with lock file mechanism
3. Verify no duplicate processes (check `ps aux`)
4. Run full verification suite

### Verification Commands
```bash
# Check for duplicate scripts running
ps aux | grep -E "health_poller|lab-up|shutdown_lab" | grep -v grep

# Check for orphaned processes
lsof -p <PID> | grep health_poller

# Verify only canonical location is active
cd ~/netdevops-project2/unified/project2-monitoring && pwd
```

### Before Merging to Main
1. Confirm canonical scripts in unified repo working
2. Verify no processes running from deprecated locations
3. Systemd service auto-restart tested
4. InfluxDB data consistency verified
5. Grafana dashboard displays correct demo status

## Migration Path: Old → New

### Step 1: Identify Running Processes
```bash
ps aux | grep health_poller
ps aux | grep lab-up
```

### Step 2: Stop Old Instances
```bash
pkill -9 -f "/netdevops-project2/health_poller.py"  # Root version
pkill -9 -f "/netdevops-complete/health_poller.py"  # Legacy version
```

### Step 3: Start Canonical Version (via systemd)
```bash
sudo systemctl start net-poller.service
sudo systemctl status net-poller.service
journalctl -u net-poller -f  # View logs
```

### Step 4: Cleanup Old Data
- Archive InfluxDB metrics older than 30 minutes
- Clear any duplicate device records in NetBox
- Verify Grafana dashboard refreshes with new data

## File Structure After Consolidation

```
unified/project2-monitoring/
├── health_poller.py          ✅ CANONICAL
├── lab-up.sh                 ✅ CANONICAL
├── shutdown_lab.sh           ✅ CANONICAL
├── demo_device_manager.py    ✅ CANONICAL
├── add_audit_fields.py       ✅ CANONICAL
├── docker-compose.yml
├── .env                      (production)
├── venv/
├── tests/
│   └── staging/              🧪 TESTING ISOLATION
│       ├── .env.test
│       ├── docker-compose.test.yml
│       ├── venv_test/
│       ├── test_lock
│       └── test.log
└── systemd/
    └── net-poller.service    ⚙️ AUTO-RESTART CONFIG
```

## Best Practices

✅ **DO:**
- Use unified repo canonical scripts only
- Run `lab-up.sh` and `shutdown_lab.sh` bare (no venv needed)
- Activate venv only when running ad-hoc Python utilities (`demo_device_manager.py`, `add_audit_fields.py`, etc.)
- Use systemd service for auto-restart (`health_poller.py` runs via `net-poller.service`)
- Use staging environment for code review
- Check lock file before running tests
- Archive old data periodically

❌ **DON'T:**
- Run scripts directly from root or legacy folders
- Try to manually start `health_poller.py`—use `lab-up.sh` (which starts systemd service)
- Activate venv to run `lab-up.sh` or `shutdown_lab.sh`
- Start health_poller with `nohup` (use systemd via `lab-up.sh`)
- Run testing without lock file
- Mix .env files (use .env for prod, .env.test for staging)
- Commit test data to main repo

## Troubleshooting

### Multiple health_poller processes running
```bash
# Kill all
pkill -9 -f health_poller.py

# Verify only systemd one exists
ps aux | grep health_poller

# Check systemd status
sudo systemctl status net-poller.service
```

### InfluxDB showing mixed/old data
```bash
# Check poller version in use
cat /proc/$(pgrep -f health_poller.py)/cmdline | tr '\0' ' '

# Should be: /home/vboxuser64/netdevops-project2/unified/project2-monitoring/health_poller.py

# View active poller logs
journalctl -u net-poller -f
```

### Testing code changes
```bash
cd ~/netdevops-project2/unified/project2-monitoring/tests/staging/
# Test changes in isolation
# Verify no lock file left behind
rm -f .test_lock
```
