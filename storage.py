import json
from datetime import datetime, timedelta

FILE = "history.json"


def save_entry(data):
    entry = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        **data
    }

    with open(FILE, "a") as f:
        json.dump(entry, f)
        f.write("\n")


def load_entries():
    entries = []
    try:
        with open(FILE, "r") as f:
            for line in f:
                entries.append(json.loads(line))
    except FileNotFoundError:
        pass

    return entries


def save_all_entries(entries):
    with open(FILE, "w") as f:
        for e in entries:
            json.dump(e, f)
            f.write("\n")


def delete_entry(entry_id):
    entries = load_entries()
    entries = [e for e in entries if e["id"] != entry_id]
    save_all_entries(entries)


def get_recent_entries(days=14):
    cutoff = datetime.now() - timedelta(days=days)
    entries = load_entries()

    return [
        e for e in entries
        if datetime.strptime(e["date"], "%Y-%m-%d") >= cutoff
    ]