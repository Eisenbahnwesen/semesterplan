import json
import os

DATA_FILE = "semester.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return None, []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("modules"), data.get("logs", [])


def save_data(modules, logs):
    data = {"modules": modules, "logs": logs}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
