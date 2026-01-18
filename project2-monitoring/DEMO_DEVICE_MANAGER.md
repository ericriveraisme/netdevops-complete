# Demo Device Manager

Script to manage device status for Grafana dashboarding demos.

## Overview

Devices are automatically classified by their primary IP address:

- **10.0.0.x** → UP (health_poller mocks them as reachable with 1.5ms latency)
- **192.0.2.x** → DOWN (health_poller mocks them as unreachable)
- **Other IPs** → Real ping-based health checks

## Usage

```bash
# Set all devices to UP
python demo_device_manager.py up

# Set all devices to DOWN
python demo_device_manager.py down

# Randomize ~50% UP, ~50% DOWN
python demo_device_manager.py random

# Check current status
python demo_device_manager.py status

# Set specific device to UP
python demo_device_manager.py up CORE-SW-01 EDGE-RTR-01

# Set specific device to DOWN
python demo_device_manager.py down DIST-SW-02
```

## How It Works

1. **Script updates NetBox**: Assigns demo IPs (10.0.0.x for UP, 192.0.2.x for DOWN) to device primary_ip4
2. **Health poller queries NetBox**: Fetches active devices and their IPs
3. **Poller detects demo IPs**: For 10.0.0.x/192.0.2.x ranges, uses mock status instead of real ping
4. **Metrics flow to InfluxDB**: Status (1=UP, 0=DOWN) and latency are written
5. **Grafana queries InfluxDB**: Dashboard displays real-time device health

## Demo Workflow

1. **Start lab**: `./lab-up.sh`
2. **Bring devices UP**: `python demo_device_manager.py up`
3. **Open Grafana**: http://100.89.136.43:3000 (Tailscale IP)
4. **View dashboard**: Wait ~30s for health_poller to run; dashboard auto-refreshes
5. **Toggle devices**: `python demo_device_manager.py down DEVICE-NAME` to simulate outages
6. **Check status anytime**: `python demo_device_manager.py status`

## Notes

- Changes take effect after the next health_poller cycle (~30s default interval)
- To view all available devices: `python demo_device_manager.py status`
- Script is idempotent; safe to run multiple times
- IPs are reused if they already exist in NetBox (safe for repeated runs)
