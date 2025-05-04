import os
import json
import numpy as np

def use_config(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("File not found.")
        raise

def create_config(data: dict, path="config.json"):
    cols    = data.get("columns", [])
    missing = data.get("missing-data", [])
    text    = data.get("text-columns", [])
    numeric = data.get("numeric-columns", [])
    pot = data.get("potential-categorical", [])

    cleaned_missing = []
    for col, pct, strategy in missing:
        pct = float(pct) if isinstance(pct, np.generic) else pct
        cleaned_missing.append([col, f"{float(pct):.1f}%", strategy])

    cleaned_pot = []
    for col, num in pot:
        pct = int(num) if isinstance(num, np.generic) else num
        cleaned_pot.append([col, f"{int(num)} Categories"])

    cleaned_text = []
    for entry in text:
        col, su, sl, sn, so = entry
        cleaned_text.append({
            "column":    col,
            "uppercase": su,
            "lowercase": sl,
            "numbers":   sn,
            "special":   so
        })

    cleaned_numeric = []
    for entry in numeric:
        if not (isinstance(entry, (list, tuple)) and len(entry) == 4):
            continue
        col, mn, mean, mx = entry
        cleaned_numeric.append({
            "column": col,
            "min":    float(mn),
            "mean":   float(mean),
            "max":    float(mx)
        })

    if os.path.exists(path):
        with open(path, "r") as f:
            cfg = json.load(f)
    else:
        cfg = {
            "Guide": {
                "missing-data": [
                    "apply the strategy in the 3rd element of each entry to all missing rows, it can be one of the following:",
                    ["mean", "none", "medium", "delete"]
                ],
                "phone-number": "leave only numbers, +- and spaces",
                "name": "delete all numbers and replace special characters with spaces",
                "potential-categorical": "the data type of these columns will be set to categorical",
                "id": "delete redundancies and turn into int",
                "broken-id": "constructs or re-construct the id column if left empty"
            }
        }

    # remove
    for k in ("columns", "missing-data", "text-columns", "numeric-columns", "potential-categorical"):
        cfg.pop(k, None)

    # recrate
    cfg["columns"] = cols
    cfg["missing-data"] = cleaned_missing
    cfg["potential-categorical"] = cleaned_pot
    cfg["text-columns"] = cleaned_text
    cfg["numeric-columns"] = cleaned_numeric

    # save
    with open(path, "w") as f:
        json.dump(cfg, f, indent=2)

    print(f"\n{path} created/updated successfully.")


