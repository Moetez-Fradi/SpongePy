#load the yaml file
import yaml
import numpy as np

def use_config(path):
    try:
        with open(path, 'r') as f:
            loaded = yaml.safe_load(f)
            return loaded
    except FileNotFoundError:
        print("File not found.")
        raise FileNotFoundError


def create_config(data: dict):
    cleaned_missing = []
    for col, val in data["missing-data"]:
        if isinstance(val, np.generic):
            val = int(val)
        cleaned_missing.append([col, str(val) + "%"])
    
    config_data = {
        "columns": data["columns"],
        "missing-data": cleaned_missing
    }

    with open("config.yaml", "w") as f:
        yaml.safe_dump(config_data, f, default_flow_style=False, sort_keys=False)

    print("\nconfig.yaml created successfully")

