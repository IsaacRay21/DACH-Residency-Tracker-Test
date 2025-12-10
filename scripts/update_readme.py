import json
from pathlib import Path
import matplotlib.pyplot as plt
import os

PROGRESS_FILE = "data/progress.json"
README_FILE = "README.md"
CHART_DIR = Path("charts")

CHART_DIR.mkdir(exist_ok=True)

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
        return 0
    return latest - initial

def compute_delta_text(initial, latest):
    if initial is None or latest is None:
        return "N/A"
    delta = latest - initial
    if delta > 0:
        return f"+{delta} 🔼"
    elif delta < 0:
        return f"{delta} 🔽"
    return "0 ➖"

def generate_button_links(topic, skill):
    topic_enc = topic.replace(" ", "%20")
    skill_enc = skill.replace(" ", "_")
    plus_url = f"../../issues/new?title=Increase%20{skill_enc}&body=update%20{topic_enc}%20{skill_enc}%20+1"
    minus_url = f"../../issues/new?title=Decrease%20{skill_enc}&body=update%20{topic_enc}%20{skill_enc}%20-1"
    return f"[➕]({plus_url}) [➖]({minus_url})"

# -------------------------------------------------
# NEW: Generate matplotlib charts per topic
# -------------------------------------------------
def generate_chart(topic, skills):
    labels = []
    current_values = []
    deltas = []

    for skill, data in skills.items():
        latest = get_latest_value(data)
        initial = data.get("initial")

        if latest is None:
            continue

        labels.append(skill.replace("_", " "))
        current_values.append(latest)
        deltas.append(compute_delta(initial, latest))

    if not labels:
        return None  # skip empty topics

    x = range(len(labels))
    width = 0.35

    plt.figure(figsize=(10, 5))
    plt.bar(x, current_values, width, label="Current", edgecolor="black")
    plt.bar([i + width for i in x], deltas, width, label="Delta", edgecolor="black")

    plt.xticks([i + width / 2 for i in x], labels, rotation=45, ha="right")
    plt.ylim(0, 10)
    plt.title(topic.replace("_", " "))
    plt.legend()
    plt.tight_layout()

    outfile = CHART_DIR / f"{topic}.png"
    plt.savefig(outfile, dpi=150)
    plt.close()

    return outfile


# -------------------------------------------------
# UPDATED: Topic Markdown section with chart
# -------------------------------------------------
def generate_topic_markdown(topic, entries):
    md = [f"## {topic.replace('_', ' ')}\n"]

    chart_path = generate_chart(topic, entries)
    if chart_path:
        md.append(f"![{topic} Chart]({chart_path.as_posix()})\n")

    md.append("| Skill | Current | Δ | Actions |")
    md.append("|-------|---------|----|---------|")

    for skill, data in entries.items():
        latest = get_latest_value(data)
        initial = data.get("initial")
        if latest is None:
            continue

        delta_text = compute_delta_text(initial, latest)
        buttons = generate_button_links(topic, skill)

        md.append(
            f"| **{skill.replace('_', ' ')}** | {latest} | {delta_text} | {buttons} |"
        )

    md.append("\n")
    return "\n".join(md)

# -------------------------------------------------
# Build README
# -------------------------------------------------
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
