import json
import sys
from datetime import datetime
from pathlib import Path
import subprocess

PROGRESS_FILE = Path("data/progress.json")
README_UPDATE_SCRIPT = Path("scripts/update_readme.py")


def load_progress():
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)


def apply_update(topic, skill, delta):
    progress = load_progress()

    if topic not in progress:
        raise ValueError(f"Topic '{topic}' not found in progress.json")

    if skill not in progress[topic]:
        raise ValueError(f"Skill '{skill}' not found in topic '{topic}'")

    # Apply update
    latest = (
        progress[topic][skill]["history"][-1]["value"]
        if progress[topic][skill]["history"]
        else progress[topic][skill]["initial"]
    )

    new_value = max(0, min(10, latest + delta))

    progress[topic][skill]["history"].append({
        "value": new_value,
        "date": datetime.utcnow().isoformat()
    })

    save_progress(progress)

    # Regenerate README
    subprocess.run(["python", str(README_UPDATE_SCRIPT)], check=True)


def parse_issue_body(body):
    """
    Expected format:
    update <topic> <skill> <delta>
    Example:
    update systems Linux_Basics +1
    """
    parts = body.strip().split()
    if len(parts) != 4 or parts[0] != "update":
        raise ValueError(f"Invalid issue body: {body}")

    topic = parts[1]
    skill = parts[2]
    delta = int(parts[3])

    return topic, skill, delta


if __name__ == "__main__":
    body = sys.argv[1]
    topic, skill, delta = parse_issue_body(body)
    apply_update(topic, skill, delta)
