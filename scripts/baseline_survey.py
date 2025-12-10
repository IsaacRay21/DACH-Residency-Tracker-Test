import json
import yaml
import os

CONFIG_FILE = "../config/structure.yaml"
BASELINE_FILE = "../data/baseline.json"

os.makedirs(os.path.dirname(BASELINE_FILE), exist_ok=True)

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

def run_survey(config):
    print("Please rate your profficiency on the following topics on  a scale of 1-10")
    results = {}
    for topic, subsections in config['topics'].items():
        results[topic] = {}
        print(topic.upper() + " :")
        for section, data in subsections['subsections'].items():
            print(section+ " (1-10)")
            while True:
                try:
                    score = int(input(q))
                    if 0 <= score <= 10:
                        break
                except ValueError:
                    pass
                print("Please enter a number between 0 and 10.")
            results[topic][section] = score
    with open(BASELINE_FILE, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Baseline saved to {BASELINE_FILE}")

if __name__ == "__main__":
    config = load_config()
    run_survey(config)
