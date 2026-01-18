#!/usr/bin/env python3
"""
Demo Device Manager: Control device UP/DOWN status for dashboarding demos.

Devices are marked UP when their primary_ip is localhost (pingable).
Devices are marked DOWN when their primary_ip is in IANA reserved range (192.0.2.0/24).

Usage:
    python demo_device_manager.py up              # All devices UP
    python demo_device_manager.py down            # All devices DOWN
    python demo_device_manager.py status          # Show current status
    python demo_device_manager.py random          # Randomize 50% UP/DOWN
    python demo_device_manager.py up CORE-SW-01   # Specific device UP
    python demo_device_manager.py down DIST-SW-02 # Specific device DOWN
"""

import argparse
import logging
import os
import random
import sys
from typing import List, Tuple

import pynetbox
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# IP addresses used for demo
LOCALHOST_BASE = "10.0.0."  # Mock UP IPs (pingable to localhost)
DOWN_IP_BASE = "192.0.2."  # IANA TEST-NET-1, unreachable (DOWN)


def build_netbox_client() -> pynetbox.api:
    """Create NetBox API client."""
    url = os.getenv("NETBOX_URL")
    token = os.getenv("NETBOX_TOKEN")
    if not url or not token:
        logging.error("Missing NETBOX_URL or NETBOX_TOKEN")
        sys.exit(1)
    return pynetbox.api(url=url, token=token)


def get_all_devices(nb: pynetbox.api) -> List:
    """Fetch all active devices from NetBox."""
    try:
        devices = list(nb.dcim.devices.filter(status="active"))
        return devices
    except Exception as e:
        logging.error("Failed to fetch devices: %s", e)
        sys.exit(1)


def set_device_ip(nb: pynetbox.api, device, ip_addr: str) -> bool:
    """
    Update device primary IP by managing IP addresses and interface assignments.
    The IP must be assigned to the interface before setting as primary_ip4.
    """
    try:
        # Get interfaces for this device
        interfaces = list(nb.dcim.interfaces.filter(device_id=device.id))
        if not interfaces:
            logging.warning("%s has no interfaces; skipping", device.name)
            return False

        interface = interfaces[0]

        # Delete old IP if present (unassign from interface first)
        if device.primary_ip4:
            try:
                old_ip_id = str(device.primary_ip4.id)
                # Clear the device primary_ip4 first
                device.update({"primary_ip4": None})
                # Delete the IP object
                nb.ipam.ip_addresses.delete(old_ip_id)
                logging.debug("Deleted old IP for %s", device.name)
            except Exception as e:
                logging.debug("Could not delete old IP for %s: %s", device.name, e)

        # Check if IP already exists (from previous runs)
        try:
            ip_list = list(nb.ipam.ip_addresses.filter(address=ip_addr))
            if ip_list:
                ip_obj = ip_list[0]
                # Make sure it's assigned to this interface
                ip_obj.update(
                    {
                        "assigned_object_type": "dcim.interface",
                        "assigned_object_id": interface.id,
                    }
                )
                logging.debug("Reusing and assigning existing IP %s to %s", ip_addr, device.name)
            else:
                raise IndexError("Not found")
        except:
            # Create new IP address AND assign to interface in one call
            try:
                ip_obj = nb.ipam.ip_addresses.create(
                    address=ip_addr,
                    interface_id=interface.id,
                    assigned_object_type="dcim.interface",
                    assigned_object_id=interface.id,
                    status="active",
                )
                logging.debug("Created new IP %s for %s", ip_addr, device.name)
            except Exception as e:
                logging.error("Could not create IP %s for %s: %s", ip_addr, device.name, e)
                return False

        # Now assign as primary (use ID not object)
        try:
            # Refresh device to ensure we have the latest state
            device = nb.dcim.devices.get(device.id)
            # Update via the API directly
            device.primary_ip4 = ip_obj.id
            device.save()
            logging.info("%s -> %s", device.name, ip_addr)
            return True
        except Exception as e:
            logging.error("Could not set primary_ip4 for %s: %s", device.name, e)
            return False

    except Exception as e:
        logging.error("Failed to update %s: %s", device.name, e)
        return False


def get_device_status(device) -> Tuple[str, str]:
    """Return (device_name, status_string) for current IP."""
    if not device.primary_ip4:
        return (device.name, "NO_IP")
    
    ip = str(device.primary_ip4.address).split("/")[0]
    if ip.startswith("10.0.0."):
        status = "UP"
    elif ip.startswith("192.0.2."):
        status = "DOWN"
    else:
        status = f"OTHER ({ip})"
    return (device.name, status)


def cmd_up(nb: pynetbox.api, args) -> None:
    """Set all (or specified) devices to UP."""
    devices = get_all_devices(nb)
    targets = (
        [d for d in devices if d.name in args.devices]
        if args.devices
        else devices
    )

    if not targets:
        logging.warning("No devices found")
        return

    logging.info("Setting %d device(s) to UP (10.0.0.x)...", len(targets))
    for i, device in enumerate(targets, start=1):
        up_ip = f"{LOCALHOST_BASE}{i}/32"
        set_device_ip(nb, device, up_ip)


def cmd_down(nb: pynetbox.api, args) -> None:
    """Set all (or specified) devices to DOWN."""
    devices = get_all_devices(nb)
    targets = (
        [d for d in devices if d.name in args.devices]
        if args.devices
        else devices
    )

    if not targets:
        logging.warning("No devices found")
        return

    logging.info("Setting %d device(s) to DOWN (192.0.2.x)...", len(targets))
    for i, device in enumerate(targets, start=1):
        down_ip = f"{DOWN_IP_BASE}{i}/32"
        set_device_ip(nb, device, down_ip)


def cmd_random(nb: pynetbox.api, args) -> None:
    """Randomize device status: ~50% UP, ~50% DOWN."""
    devices = get_all_devices(nb)
    logging.info("Randomizing %d device(s)...", len(devices))
    for i, device in enumerate(devices, start=1):
        if random.choice([True, False]):
            set_device_ip(nb, device, LOCALHOST_IP)
        else:
            down_ip = f"{DOWN_IP_BASE}{i}/32"
            set_device_ip(nb, device, down_ip)


def cmd_status(nb: pynetbox.api, args) -> None:
    """Show current status of all devices."""
    devices = get_all_devices(nb)
    if not devices:
        logging.info("No active devices found")
        return

    logging.info("Device Status:")
    print("\n" + "=" * 50)
    for device in devices:
        name, status = get_device_status(device)
        print(f"  {name:<20} {status}")
    print("=" * 50 + "\n")

    up_count = sum(1 for d in devices if get_device_status(d)[1] == "UP")
    down_count = sum(1 for d in devices if get_device_status(d)[1] == "DOWN")
    logging.info("Summary: %d UP, %d DOWN", up_count, down_count)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Demo Device Manager: Control device UP/DOWN status"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # up command
    up_parser = subparsers.add_parser("up", help="Set device(s) to UP")
    up_parser.add_argument("devices", nargs="*", help="Device names (default: all)")

    # down command
    down_parser = subparsers.add_parser("down", help="Set device(s) to DOWN")
    down_parser.add_argument("devices", nargs="*", help="Device names (default: all)")

    # status command
    subparsers.add_parser("status", help="Show device status")

    # random command
    subparsers.add_parser("random", help="Randomize device status")

    args = parser.parse_args()

    nb = build_netbox_client()

    if args.command == "up":
        cmd_up(nb, args)
    elif args.command == "down":
        cmd_down(nb, args)
    elif args.command == "status":
        cmd_status(nb, args)
    elif args.command == "random":
        cmd_random(nb, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
