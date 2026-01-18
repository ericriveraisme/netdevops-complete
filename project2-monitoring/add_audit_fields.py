#!/usr/bin/env python3
"""
Add audit trail fields (serial, asset_tag, MAC mockup) to demo devices.
This prevents duplicates and maintains compliance audit trail.
"""

import logging
import os
import sys

import pynetbox
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def build_netbox_client() -> pynetbox.api:
    """Create NetBox API client."""
    url = os.getenv("NETBOX_URL")
    token = os.getenv("NETBOX_TOKEN")
    if not url or not token:
        logging.error("Missing NETBOX_URL or NETBOX_TOKEN")
        sys.exit(1)
    return pynetbox.api(url=url, token=token)


def get_all_devices(nb: pynetbox.api):
    """Fetch all active devices from NetBox."""
    try:
        devices = list(nb.dcim.devices.filter(status="active"))
        return devices
    except Exception as e:
        logging.error("Failed to fetch devices: %s", e)
        sys.exit(1)


def add_audit_fields(nb: pynetbox.api) -> None:
    """Add serial, asset_tag to devices for audit trail."""
    devices = get_all_devices(nb)
    
    # Map device names to audit data
    audit_data = {
        "CORE-SW-01": {
            "serial": "DEMO-2026-01-0001",
            "asset_tag": "DEMO-SW-001",
            "mock_mac": "02:00:00:01:01:01",
        },
        "DIST-SW-02": {
            "serial": "DEMO-2026-01-0002",
            "asset_tag": "DEMO-SW-002",
            "mock_mac": "02:00:00:01:02:02",
        },
        "DIST-SW-03": {
            "serial": "DEMO-2026-01-0003",
            "asset_tag": "DEMO-SW-003",
            "mock_mac": "02:00:00:01:03:03",
        },
        "EDGE-ROUTER-02": {
            "serial": "DEMO-2026-01-0004",
            "asset_tag": "DEMO-RT-001",
            "mock_mac": "02:00:00:01:04:04",
        },
        "EDGE-RTR-01": {
            "serial": "DEMO-2026-01-0005",
            "asset_tag": "DEMO-RT-002",
            "mock_mac": "02:00:00:01:05:05",
        },
    }
    
    logging.info("Adding audit trail fields to %d devices...", len(devices))
    
    for device in devices:
        if device.name not in audit_data:
            logging.warning("Device %s not in audit mapping, skipping", device.name)
            continue
        
        data = audit_data[device.name]
        
        try:
            # Refresh to ensure latest state
            device = nb.dcim.devices.get(device.id)
            
            # Update fields
            device.serial = data["serial"]
            device.asset_tag = data["asset_tag"]
            device.comments = f"Demo device | MAC (mock): {data['mock_mac']} | Created for Grafana dashboarding"
            device.save()
            
            logging.info(
                "%s -> Serial: %s, AssetTag: %s, MAC: %s",
                device.name,
                data["serial"],
                data["asset_tag"],
                data["mock_mac"],
            )
        except Exception as e:
            logging.error("Failed to update %s: %s", device.name, e)


def show_audit_status(nb: pynetbox.api) -> None:
    """Show current audit trail status."""
    devices = get_all_devices(nb)
    
    print("\n" + "=" * 100)
    print(f"{'Device':<20} {'Serial':<20} {'Asset Tag':<20} {'Comments':<40}")
    print("=" * 100)
    
    for device in sorted(devices, key=lambda d: d.name):
        serial = device.serial or "(empty)"
        asset_tag = device.asset_tag or "(empty)"
        comments = (device.comments or "(empty)")[:37] + "..."
        print(f"{device.name:<20} {serial:<20} {asset_tag:<20} {comments:<40}")
    
    print("=" * 100 + "\n")


def main() -> None:
    nb = build_netbox_client()
    
    print("\nBefore audit update:")
    show_audit_status(nb)
    
    add_audit_fields(nb)
    
    print("After audit update:")
    show_audit_status(nb)


if __name__ == "__main__":
    main()
