import os
import yaml

CONFIG_FILE = "../config/structure.yaml"
TOPICS_DIR = "../topics"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

def create_structure(config):
    os.makedirs(TOPICS_DIR, exist_ok=True)
    for topic, subsections in config['topics'].items():
        topic_path = os.path.join(TOPICS_DIR, topic)
        os.makedirs(topic_path, exist_ok=True)
        for subsection in subsections:
            subsection_path = os.path.join(topic_path, subsection)
            os.makedirs(subsection_path, exist_ok=True)
            for file in config.get('files', []):
                file_path = os.path.join(subsection_path, file)
                if not os.path.exists(file_path):
                    with open(file_path, 'w') as f:
                        f.write(f"# {subsection} - {file}\n")

if __name__ == "__main__":
    config = load_config()
    create_structure(config)
    print("Repo structure initialized successfully.")
