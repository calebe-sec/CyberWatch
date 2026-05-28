import json

def export_json(file, results):
    with open(file, "w") as f:
        json.dump(results ,f ,indent=4)