#!/bin/bash
set -e
# Sync the active InfluxDB token from the running container into a local, gitignored file (.env.local).
# This avoids manual token creation and keeps secrets out of git.

CANONICAL_DIR="/home/vboxuser64/netdevops-project2/unified/project2-monitoring"
ENV_LOCAL="$CANONICAL_DIR/.env.local"
CONTAINER="project2-influxdb"

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
  echo "InfluxDB container ${CONTAINER} is not running. Start lab first (./lab-up.sh)."
  exit 1
fi

token=$(docker exec ${CONTAINER} sh -c "awk -F '=' '/token =/{print \$2; exit}' /etc/influxdb2/influx-configs" | tr -d ' \r\n')
if [ -z "$token" ]; then
  echo "Could not read token from /etc/influxdb2/influx-configs"
  exit 1
fi

# Write/replace INFLUX_TOKEN in .env.local (gitignored)
mkdir -p "$(dirname "$ENV_LOCAL")"
if [ -f "$ENV_LOCAL" ]; then
  grep -v '^INFLUX_TOKEN=' "$ENV_LOCAL" > "$ENV_LOCAL.tmp" || true
  mv "$ENV_LOCAL.tmp" "$ENV_LOCAL"
fi
echo "INFLUX_TOKEN=$token" >> "$ENV_LOCAL"

echo "Updated $ENV_LOCAL with active InfluxDB token."
echo "Next steps:"
echo "  1) source $ENV_LOCAL (or export INFLUX_TOKEN)"
echo "  2) sudo systemctl restart net-poller.service"
echo "  3) docker compose --env-file .env --env-file .env.local up -d grafana"