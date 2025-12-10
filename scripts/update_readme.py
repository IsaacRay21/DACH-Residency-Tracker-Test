import json
from pathlib import Path

PROGRESS_FILE = "data/progress.json"
README_FILE = "README.md"

# Set your GitHub repository URL here
GITHUB_REPO_URL = "IsaacRay21/DACH-Residency-Tracker-Test"
def load_progress():
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_latest_value(data):
    history = data.get("history", [])
    if history:
        return history[-1]["value"]
    return data.get("initial")

def compute_delta(initial, latest):
    if initial is None or latest is None:
        return "N/A"
    delta = latest - initial
    if delta > 0:
        return f"+{delta} 🔼"
    elif delta < 0:
        return f"{delta} 🔽"
    return "0 ➖"

def generate_button_links(topic, skill):
    """
    Generates absolute GitHub issue URLs for increasing/decreasing a skill score.
    """
    topic_enc = topic.replace(" ", "%20")
    skill_enc = skill.replace(" ", "_")
    plus_url = f"/issues/new?title=Increase%20{skill_enc}&body=update%20{topic_enc}%20{skill_enc}%20+1"
    minus_url = f"/issues/new?title=Decrease%20{skill_enc}&body=update%20{topic_enc}%20{skill_enc}%20-1"
    return f"[➕]({plus_url}) [➖]({minus_url})"

def generate_topic_markdown(topic, entries):
    md = [f"## {topic.replace('_', ' ')}\n"]
    md.append("| Skill | Current | Δ | Actions |")
    md.append("|-------|---------|----|---------|")

    for skill, data in entries.items():
        latest = get_latest_value(data)
        initial = data.get("initial")
        if latest is None:
            continue

        delta = compute_delta(initial, latest)
        buttons = generate_button_links(topic, skill)

        md.append(
            f"| **{skill.replace('_', ' ')}** | {latest} | {delta} | {buttons} |"
        )

    md.append("\n")
    return "\n".join(md)

def update_readme(progress):
    sections = []
    sections.append("# 📊 Residency Progress Dashboard\n")
    sections.append("Automatically generated progress overview.\n")

    for topic, skills in progress.items():
        sections.append(generate_topic_markdown(topic, skills))

    markdown = "\n".join(sections)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"README updated → {README_FILE}")

if __name__ == "__main__":
    progress = load_progress()
    update_readme(progress)
