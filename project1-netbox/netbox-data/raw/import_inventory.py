import os
from dotenv import load_dotenv
import pynetbox

# Load the variables from the .env file
load_dotenv()

nb = pynetbox.api(
    url=os.getenv('NETBOX_URL'),
    token=os.getenv('NETBOX_TOKEN')
)
def get_or_create_site(site_name):
    site = nb.dcim.sites.get(name=site_name)
    if not site:
        print(f"➕ Site '{site_name}' not found. Creating it...")
        site = nb.dcim.sites.create(name=site_name, slug=site_name.lower().replace(" ", "-"))
    return site

def get_or_create_role(role_name):
    role = nb.dcim.device_roles.get(name=role_name)
    if not role:
        print(f"➕ Role '{role_name}' not found. Creating it...")
        # Device roles also need a color; we'll use 'grey' as default
        role = nb.dcim.device_roles.create(name=role_name, slug=role_name.lower().replace(" ", "-"), color='808080')
    return role

def import_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Resolve dependencies automatically
                site = get_or_create_site(row['site'])
                role = get_or_create_role(row['role'])
                
                # Create the device (Note: device_type 1 is usually auto-created by NetBox Docker)
                nb.dcim.devices.create(
                    name=row['hostname'],
                    device_type=1, 
                    role=role.id,
                    site=site.id,
                    status=row['status'].lower()
                )
                print(f"✅ Created device: {row['hostname']}")
            except Exception as e:
                print(f"❌ Error adding {row['hostname']}: {e}")

if __name__ == "__main__":
    import_csv('inventory.csv')