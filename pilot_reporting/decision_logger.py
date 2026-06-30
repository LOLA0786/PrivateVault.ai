import json
import os

OUTPUT_FILE = "pilot_output/decision_records.json"

def append_decision(record):

    os.makedirs("pilot_output", exist_ok=True)

    data = []

    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE) as f:
            try:
                data = json.load(f)
            except:
                data = []

    data.append(record)

    with open(OUTPUT_FILE,"w") as f:
        json.dump(data,f,indent=2)
