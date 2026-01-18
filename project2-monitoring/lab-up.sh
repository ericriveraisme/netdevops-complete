#!/bin/bash
# Lab Startup Script - NetDevOps Project 2
# Brings all services online (NetBox, monitoring stack, poller)
# 
# CANONICAL LOCATION: /home/vboxuser64/netdevops-project2/unified/project2-monitoring/lab-up.sh
# DO NOT RUN FROM: ~/netdevops-project2/lab-up.sh or ~/netdevops-complete/lab-up.sh
#
# FUTURE ENHANCEMENTS:
# - Add --init flag to run initialization (create buckets, provision Grafana)
# - Add health check loop to verify all services are ready before starting poller
# - Add --verify flag to run smoke tests after startup
# - Add startup time tracking and progress indicators

set -e  # Exit on any error

CANONICAL_DIR="/home/vboxuser64/netdevops-project2/unified/project2-monitoring"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Safety check: Ensure we're running from canonical location
if [ "$SCRIPT_DIR" != "$CANONICAL_DIR" ]; then
    echo "❌ ERROR: lab-up.sh must be run from canonical location:"
    echo "   Expected: $CANONICAL_DIR/lab-up.sh"
    echo "   Found at: $SCRIPT_DIR/lab-up.sh"
    echo ""
    echo "Please use:"
    echo "   cd $CANONICAL_DIR && ./lab-up.sh"
    exit 1
fi

echo "🚀 Starting NetDevOps Lab from canonical location..."

# 1. Start Project 1 Containers (NetBox)
echo "--- Starting NetBox Source of Truth ---"
cd ~/netbox-docker && docker compose up -d
echo "✅ NetBox Stack Started. Waiting for API to be ready..."
sleep 10

# 2. Start Project 2 Containers (Monitoring)
echo "--- Starting InfluxDB & Grafana ---"
cd "$CANONICAL_DIR" && docker compose up -d
echo "✅ Monitoring Stack Started. Waiting for initialization..."
sleep 10

# 3. Start the ICMP Poller (System Service - prevents duplicates and enables auto-restart)
echo "--- Starting Python Poller Service (via systemd) ---"

# Kill any orphaned health_poller processes from old methods
pkill -9 -f "health_poller.py" || true

# Copy systemd service file
sudo cp "$CANONICAL_DIR/systemd/net-poller.service" /etc/systemd/system/
sudo systemctl daemon-reload

# Start or restart service
sudo systemctl restart net-poller.service
sleep 2

# Verify service started
if sudo systemctl is-active --quiet net-poller.service; then
    echo "✅ Poller Service Started (auto-restart enabled on reboot)."
else
    echo "⚠️  Poller service failed to start. Check logs with:"
    echo "   journalctl -u net-poller -f"
    exit 1
fi

echo ""
echo "---------------------------------------"
echo "✨ All services are online!"
echo ""
echo "📊 Access points:"
echo "   NetBox:  http://localhost:8000  (admin/admin)"
echo "   Grafana: http://localhost:3000  (admin/admin)"
echo ""
echo "📋 Useful commands:"
echo "   View poller logs:  journalctl -u net-poller -f"
echo "   Service status:    sudo systemctl status net-poller"
echo "   Restart poller:    sudo systemctl restart net-poller"
echo "   Container status:  docker ps"
echo ""
echo "⚠️  To use demo device manager:"
echo "   cd $CANONICAL_DIR && python demo_device_manager.py [up|down|random|status]"
