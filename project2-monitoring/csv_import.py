import csv
import logging
from typing import Dict

from bulk_provision import provision_device_idempotent

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Map names to slugs for NetBox
ROLE_MAP = {
    'Core-Switch': 'core-switch',
    'Distribution-Switch': 'distribution-switch',
    'Edge-Router': 'edge-router',
}
SITE_MAP = {
    'Main-Office': 'main-office',
    'Remote-Branch': 'remote-branch',
}

# Infer device model slug if not present
def infer_model_slug(role_slug: str) -> str:
    # Use a known existing device type slug to avoid missing-slug errors
    # Adjust later if NetBox has specific types provisioned
    return 'generic-switch'

# Transform a CSV row into payload expected by provision_device_idempotent
def row_to_payload(row: Dict[str, str]) -> Dict[str, str]:
    name = row.get('hostname') or row.get('name') or ''
    role_name = row.get('role', '')
    site_name = row.get('site', '')

    role_slug = ROLE_MAP.get(role_name, role_name.lower().replace(' ', '-'))
    site_slug = SITE_MAP.get(site_name, site_name.lower().replace(' ', '-'))
    model_slug = infer_model_slug(role_slug)

    payload: Dict[str, str] = {
        'name': name,
        'role': role_slug,
        'model': model_slug,
        'site': site_slug,
    }
    # Optional IP if provided in CSV as 'ip'
    ip = row.get('ip')
    if ip:
        payload['ip'] = ip
    return payload

if __name__ == '__main__':
    path = 'project1-netbox/netbox-data/raw/inventory.csv'
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                data = row_to_payload(row)
                provision_device_idempotent(data)
            except Exception as e:
                logging.error('Failed to import %s: %s', row, e)
