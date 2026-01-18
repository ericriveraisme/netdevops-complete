# Device Naming & Audit Trail Strategy

## Purpose
Ensure unique device identification, prevent duplicates, and maintain audit trail for compliance and operational tracking.

## Naming Convention

### Device Name Format
```
{SITE}-{CATEGORY}-{FUNCTION}-{SEQ}

Examples:
  HQ-SW-CORE-01       (Headquarters, Switch, Core function, sequence 01)
  BR-SW-DIST-03       (Branch, Switch, Distribution, sequence 03)
  HQ-RT-EDGE-02       (Headquarters, Router, Edge function, sequence 02)
  DC-FW-MAIN-01       (Data Center, Firewall, Main, sequence 01)
```

### Categories
- `SW` = Switch
- `RT` = Router
- `FW` = Firewall
- `LB` = Load Balancer
- `SRV` = Server
- `SG` = Security Gateway

### Functions
- `CORE` = Core switching
- `DIST` = Distribution
- `EDGE` = Edge/Border
- `ACC` = Access
- `MAIN` = Primary
- `BKP` = Backup

## Unique Identification Fields (NetBox)

### 1. **Serial Number** (Primary Audit Trail)
**Required field.** Format: `{SITE}-{YEAR}-{MONTH}-{SEQ}`

Example: `HQ-2026-01-00012` means Headquarters device #12 from January 2026

Advantages:
- Unique, immutable
- Matches real hardware SKUs
- Primary index for asset tracking
- Compliance/audit requirement

### 2. **Asset Tag** (Inventory Tracking)
**Optional but recommended.** Format: `{ORG}-{REGION}-{CATEGORY}-{SEQ}`

Example: `NETOPS-US-SW-001` = NetDevOps US region Switch 001

Advantages:
- Physical asset reference
- Can be printed on device labels
- Inventory/accounting link

### 3. **MAC Address** (Hardware Fingerprinting)
**Optional but recommended for physical devices.** Format: `00:11:22:{SITE}:{CATEGORY}:{SEQ}`

Example: `00:11:22:01:01:0A` (Headquarters, Switch, device 10)

Advantages:
- Prevents duplicate MAC registrations
- Physical device identification
- Network switching lookup

For demo/virtual devices, use reserved range:
- `02:00:00:xx:xx:xx` (locally administered, not globally unique)

### 4. **Description Field**
Include metadata:
```
"HQ Core Switch - Primary | Location: Building A Room 205 | Vendor: Vendor-X | Contract: 2024-5432"
```

## Implementation

### For New Devices
1. Assign serial number (unique, immutable)
2. Assign asset tag (for inventory)
3. Assign MAC if hardware device
4. Name device following naming convention
5. Document in comments (physical location, vendor, contract ID)

### For Demo/Virtual Devices
Use demo prefix in names to clearly indicate non-production:
```
DEMO-SW-CORE-01     (Serial: DEMO-2026-01-00001)
DEMO-RT-EDGE-02     (Serial: DEMO-2026-01-00002)
```

## NetBox API Example (Python)

```python
device_data = {
    "name": "HQ-SW-CORE-01",
    "device_type": 5,  # Generic Switch ID
    "site": 1,         # Headquarters ID
    "role": 4,         # Core-Switch role ID
    "serial": "HQ-2026-01-00001",      # Unique serial
    "asset_tag": "NETOPS-US-SW-001",   # Inventory tag
    "comments": "Primary core switch | Location: Bldg A Rm 205 | Vendor: Cisco | Contract: 2024-5432"
}

device = nb.dcim.devices.create(**device_data)
```

## Preventing Duplicates

### Before Creating Device
```bash
# Check if serial already exists
curl -s -H "Authorization: Token $TOKEN" \
  "http://netbox-url/api/dcim/devices/?serial=HQ-2026-01-00001"

# Should return count=0 if new
```

### In csv_import.py / Provisioning Scripts
Add validation:
```python
# Check for duplicate serials
existing = list(nb.dcim.devices.filter(serial=device_data['serial']))
if existing:
    logging.error(f"Device with serial {device_data['serial']} already exists!")
    return False
```

## Audit Trail Fields (NetBox)
- `created` = Device creation timestamp (auto)
- `last_updated` = Last modification timestamp (auto)
- `comments` = Manual audit trail (vendor info, contract, location)
- NetBox tracks all API changes in activity log (if enabled)

## Current Status

### Demo Devices (to update)
| Device | Current Serial | Proposed Serial | Asset Tag | MAC |
|--------|----------------|-----------------|-----------|-----|
| CORE-SW-01 | (empty) | DEMO-2026-01-0001 | DEMO-SW-001 | 02:00:00:01:01:01 |
| DIST-SW-02 | (empty) | DEMO-2026-01-0002 | DEMO-SW-002 | 02:00:00:01:02:02 |
| DIST-SW-03 | (empty) | DEMO-2026-01-0003 | DEMO-SW-003 | 02:00:00:01:03:03 |
| EDGE-ROUTER-02 | (empty) | DEMO-2026-01-0004 | DEMO-RT-001 | 02:00:00:01:04:04 |
| EDGE-RTR-01 | (empty) | DEMO-2026-01-0005 | DEMO-RT-002 | 02:00:00:01:05:05 |

## Next Steps
1. Update demo devices with serials + asset tags
2. Create device provisioning script with duplicate checks
3. Document in DEVICES.md inventory file
4. Add serial validation to bulk_provision.py
