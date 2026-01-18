#!/bin/bash
# Lab Shutdown Script - NetDevOps Project 2
# Gracefully stops all services (poller, monitoring, NetBox)
#
# CANONICAL LOCATION: /home/vboxuser64/netdevops-project2/unified/project2-monitoring/shutdown_lab.sh
# DO NOT RUN FROM: ~/netdevops-project2/shutdown_lab.sh or ~/netdevops-complete/shutdown_lab.sh
#
# FUTURE ENHANCEMENTS:
# - Add --force-reset flag for full teardown with `docker compose down -v` (destructive)
# - Add --terraform flag to call `terraform destroy` when Project 3 is scaffolded
# - Add timestamp logging to track shutdown history
# - Add verification step: retry status checks until all containers are stopped

set -e

CANONICAL_DIR="/home/vboxuser64/netdevops-project2/unified/project2-monitoring"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Safety check: Ensure we're running from canonical location
if [ "$SCRIPT_DIR" != "$CANONICAL_DIR" ]; then
    echo "❌ ERROR: shutdown_lab.sh must be run from canonical location:"
    echo "   Expected: $CANONICAL_DIR/shutdown_lab.sh"
    echo "   Found at: $SCRIPT_DIR/shutdown_lab.sh"
    exit 1
fi

echo "🛑 Starting Graceful Lab Shutdown from canonical location..."

# 1. Stop the ICMP Poller (System Service)
echo "--- Stopping Python Poller Service ---"
sudo systemctl stop net-poller.service || true
echo "✅ Poller Stopped."

# 2. Stop Project 2 Containers (Monitoring)
echo "--- Stopping InfluxDB & Grafana ---"
cd "$CANONICAL_DIR" && docker compose stop
echo "✅ Monitoring Stack Stopped."

# 3. Stop Project 1 Containers (NetBox)
echo "--- Stopping NetBox Source of Truth ---"
cd ~/netbox-docker && docker compose stop
echo "✅ NetBox Stack Stopped."

echo ""
echo "---------------------------------------"
echo "💤 All services are paused."
echo ""
echo "📋 Useful commands:"
echo "   Check status:     docker ps"
echo "   Restart services: cd $CANONICAL_DIR && ./lab-up.sh"
echo "   View data:        (InfluxDB and Grafana volumes preserved)"