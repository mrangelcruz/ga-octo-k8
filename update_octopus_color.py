import yaml
import requests
import os


# === CONFIG ===
OCTOPUS_API_KEY = os.getenv("OCTOPUS_API_KEY")
OCTOPUS_SERVER = os.getenv("OCTOPUS_SERVER")
OCTOPUS_SPACE_ID = os.getenv("OCTOPUS_SPACE_ID")
OCTOPUS_PROJECT_ID = os.getenv("OCTOPUS_PROJECT_ID")

# === Load YAML ===
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

color_map = {
    "red": "#ff0000",
    "yellow": "#ffff00",
    "green": "#00ff00"
}

# === Get Project VariableSetId ===
project_url = f"{OCTOPUS_SERVER}/api/{OCTOPUS_SPACE_ID}/projects/{OCTOPUS_PROJECT_ID}"
headers = {"X-Octopus-ApiKey": OCTOPUS_API_KEY}
project_data = requests.get(project_url, headers=headers).json()
variable_set_id = project_data["VariableSetId"]

# === Get Environment IDs ===
env_url = f"{OCTOPUS_SERVER}/api/{OCTOPUS_SPACE_ID}/environments"
env_data = requests.get(env_url, headers=headers).json()
env_ids = {env["Name"]: env["Id"] for env in env_data["Items"]}

# === Get Current Variables ===
var_url = f"{OCTOPUS_SERVER}/api/{OCTOPUS_SPACE_ID}/variables/{variable_set_id}"
var_data = requests.get(var_url, headers=headers).json()

# === Update BG_COLOR per environment ===
for env_name, env_config in config["environment"].items():
    color_name = env_config["color"]
    hex_color = color_map.get(color_name.lower(), "#ffffff")
    env_id = env_ids.get(env_name)

    if not env_id:
        print(f"❌ Environment '{env_name}' not found in Octopus.")
        continue

    # Check if variable already exists with scope
    updated = False
    for var in var_data["Variables"]:
        if var["Name"] == "BG_COLOR" and env_id in var.get("Scope", {}).get("Environment", []):
            var["Value"] = hex_color
            updated = True
            print(f"🔄 Updated BG_COLOR for {env_name} to {hex_color}")
            break

    if not updated:
        # Add new scoped variable
        var_data["Variables"].append({
            "Name": "BG_COLOR",
            "Value": hex_color,
            "Type": "String",
            "Scope": {
                "Environment": [env_id]
            }
        })
        print(f"➕ Added BG_COLOR for {env_name} as {hex_color}")

# === Push Update ===
response = requests.put(var_url, headers=headers, json=var_data)
if response.ok:
    print("✅ BG_COLOR variables updated successfully.")
else:
    print("❌ Failed to update variables:", response.text)
