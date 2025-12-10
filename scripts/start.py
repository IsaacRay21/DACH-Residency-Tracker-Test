#!/usr/bin/env python3
import os

# Import your other scripts as modules
from init_repo import create_topic_folders_with_files, load_config
from baseline_survey import load_config as load_survey_config, initialize_progress_structure, run_initial_survey
from update_readme import update_readme, load_progress

CONFIG_FILE = "../config/structure.yaml"

def main():
    # Step 1: Load config
    config = load_config()

    # Step 2: Initialize repo folders and files
    print("\n=== Initializing repo structure ===")
    create_topic_folders_with_files(config)

    # Step 3: Run baseline survey
    print("\n=== Running baseline survey ===")
    # Initialize progress.json if it doesn't exist
    progress_file = "../data/progress.json"
    if not os.path.exists(progress_file):
        run_initial_survey(config)
    
    progress = load_progress()

    # Step 4: Update README
    print("\n=== Updating README ===")
    update_readme(progress)

    print("\n🎉 Repository initialized, baseline survey complete, README updated!")

if __name__ == "__main__":
    main()
