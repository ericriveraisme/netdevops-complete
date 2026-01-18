# Migrating NetBox Information from Project 1

This guide shows how to bring your Project 1 NetBox data (device lists, CSV/YAML inventories, any fixtures/scripts) into the unified repository cleanly and safely.

## What to Move
- Device inventory files: CSV/YAML/JSON with fields like `name`, `role`, `model`, `site`, `ip`
- NetBox-related scripts: import/export helpers, `pynetbox` scripts
- Optional: NetBox DB backup (PostgreSQL) if you want a full data copy

## Fast Path: File-Level Copy (Recommended)
Use this when Project 1 has files that describe devices rather than a DB export.

1) Set your Project 1 path
```bash
# Replace path as needed
export P1_ROOT=~/netdevops-project1
```

2) Create a staging area in the unified repo
```bash
cd ~/netdevops-complete
mkdir -p project1-netbox/netbox-data/{raw,processed}
```

3) Copy the data files (exclude secrets)
```bash
rsync -av --exclude='.git' --exclude='.env' \
  "$P1_ROOT"/netbox-data/ \
  ./project1-netbox/netbox-data/raw/

# If your data files live elsewhere, copy those paths instead, e.g.:
# rsync -av "$P1_ROOT"/inventories/ ./project1-netbox/netbox-data/raw/
```

4) Normalize names → slugs
- NetBox scripts in this repo expect slugs (e.g., `edge-router`, `generic-switch`, `main-office`).
- Run get_slugs.py against your current NetBox to list valid slugs.
```bash
cd ~/netdevops-project2
./venv/bin/python get_slugs.py | tee ~/netdevops-complete/docs/netbox-slugs.txt
```
- Update your copied CSV/YAML to use those slugs for `role`, `model`, and `site` (keep `name` and `ip` as-is).

5) Prepare a processed file for import
```bash
# Example: devices.csv with headers: name,role,model,site,ip
cp ~/netdevops-complete/project1-netbox/netbox-data/raw/devices.csv \
   ~/netdevops-complete/project1-netbox/netbox-data/processed/devices.csv
```

6) Import into NetBox via existing scripts
- Option A (quick): Convert the CSV to a Python list of dicts and paste into `new_devices` in bulk_provision.py.
- Option B (clean): Write a small helper that reads CSV and calls `provision_device_idempotent()`.

Example helper snippet (save as `csv_import.py` next to bulk_provision.py):
```python
import csv
from bulk_provision import provision_device_idempotent

with open('project1-netbox/netbox-data/processed/devices.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        payload = {
            'name': row['name'],
            'role': row['role'],     # slug required
            'model': row['model'],   # slug required
            'site': row['site'],     # slug required
            'ip': row['ip'],
        }
        provision_device_idempotent(payload)
```

Run the import:
```bash
cd ~/netdevops-project2
./venv/bin/python csv_import.py
```

7) Verify and reconcile
```bash
# Check devices exist and have primary IP set
./venv/bin/python bulk_ip_assign.py  # optional per-device adjustments

# UI check
# Open NetBox in your browser and spot-check devices, interfaces, and IPs
```

## Optional: Full DB Migration (pg_dump/pg_restore)
Use only if you need the entire NetBox dataset exactly as-is.

1) From Project 1 PostgreSQL, take a dump
```bash
# Inside the Postgres container for Project 1 NetBox
pg_dump -U netbox -d netbox -Fc -f /tmp/netbox.pgdump
```

2) Copy dump to the new environment and restore into the Project 2 NetBox Postgres
```bash
# Copy dump out of container, then into the new Postgres
docker cp project1-postgres:/tmp/netbox.pgdump ./
docker cp ./netbox.pgdump project2-postgres:/tmp/netbox.pgdump

# Inside Project 2 Postgres container
pg_restore -U netbox -d netbox --clean --if-exists /tmp/netbox.pgdump
```

3) Validate slugs and script compatibility
- After a DB restore, slugs, roles, and device types should match.
- Rerun get_slugs.py and ensure your import scripts use those values.

## Safety and Secrets
- Never copy `.env` or credentials from Project 1—recreate them in `.env.example` and personal `.env` files.
- Keep all secrets out of git; confirm `.gitignore` excludes `.env` and `*.tfvars`.

## Where This Fits in the Reorg Steps
- Perform this after STEP 2 (structure) and STEP 3 (copy Project 2) so the new repo has a place for Project 1 data.
- Then proceed with Terraform Sprints; NetBox will act as your source of truth.
