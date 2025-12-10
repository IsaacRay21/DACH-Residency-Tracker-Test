import os
import yaml

CONFIG_FILE = "../config/structure.yaml"
TOPICS_DIR = "../topics"

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def create_topic_folders_with_files(config):
    """
    Create folders for major topics and populate them with files from YAML.
    """
    os.makedirs(TOPICS_DIR, exist_ok=True)
    
    for topic in config['topics'].keys():
        topic_path = os.path.join(TOPICS_DIR, topic)
        os.makedirs(topic_path, exist_ok=True)
        print(f"Created folder: {topic_path}")

        # Populate files
        for file in config.get('files', []):
            file_path = os.path.join(topic_path, file)
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {topic} - {file}\n")
                print(f"  Created file: {file_path}")

if __name__ == "__main__":
    config = load_config()
    create_topic_folders_with_files(config)
    print("Major topic folders and files initialized successfully.")
