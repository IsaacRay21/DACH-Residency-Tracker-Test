import json
import yaml
import os
from datetime import datetime

CONFIG_FILE = "../config/structure.yaml"
PROGRESS_FILE = "../data/progress.json"

os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)


def load_config():
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)


def initialize_progress_structure(config):
    """
    Builds a structured progress format for long-term tracking
    but leaves all values empty until the first survey.
    """
    progress = {}

    for topic, subsections in config["topics"].items():
        progress[topic] = {}
        for section in subsections["subsections"].keys():
            progress[topic][section] = {
                "initial": None,
                "history": []   # Will remain empty for initial survey
            }

    return progress


def run_initial_survey(config):
    """
    Runs ONLY the initial baseline survey.
    Does NOT update history.
    """

    progress = initialize_progress_structure(config)

    print("Rate your proficiency on a scale of 1–10.\n")

    timestamp = datetime.now().isoformat()

    for topic, subsections in config["topics"].items():
        print(f"\n{topic.upper()} :")

        for section, data in subsections["subsections"].items():

            while True:
                try:
                    score = int(input(f"{section} - {data.get('description', '')}: "))
                    if 0 <= score <= 10:
                        break
                except ValueError:
                    pass
                print("Please enter a number between 0 and 10.")

            # Set only the initial value
            progress[topic][section]["initial"] = score

            # DO NOT add to history — initial only
            progress[topic][section]["history"] = []  

    # Save baseline
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)

    print(f"\nInitial baseline saved → {PROGRESS_FILE}")


if __name__ == "__main__":
    config = load_config()
    run_initial_survey(config)
