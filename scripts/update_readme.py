import json
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

PROGRESS_FILE = "../data/progress.json"
README_FILE = "../README.md"
CHART_FILE = "../data/progress_chart.png"  # Relative path for embedding


def load_progress():
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)



def compute_delta(initial, latest):
    if initial is None or latest is None:
        return "N/A"
    delta = latest - initial
    if delta > 0:
        return f"+{delta} 🔼"
    elif delta < 0:
        return f"{delta} 🔽"
    return "0"


def get_latest_value(data):
    history = data.get("history", [])
    if history:
        return history[-1]["value"]
    return data.get("initial")


def generate_button_links(topic, skill):
    topic_enc = topic.replace(" ", "%20")
    skill_enc = skill.replace(" ", "_")
    plus_link = f"../../issues/new?title=Increase%20{skill_enc}&body=update%20{topic_enc}%20{skill_enc}%20+1"
    minus_link = f"../../issues/new?title=Decrease%20{skill_enc}&body=update%20{topic_enc}%20{skill_enc}%20-1"
    return f"[➕]({plus_link}) [➖]({minus_link})"


def generate_topic_markdown(topic, entries):
    """
    Generates a simple table for the topic with Current, Δ, and Actions.
    """
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


def compute_topic_averages(progress):
    """
    Computes average score for each major topic.
    """
    topic_names = []
    latest_avgs = []

    for topic, skills in progress.items():
        topic_names.append(topic.replace("_", " "))
        skill_values_latest = [get_latest_value(s) for s in skills.values() if get_latest_value(s) is not None]
        latest_avg = sum(skill_values_latest) / len(skill_values_latest) if skill_values_latest else 0
        latest_avgs.append(latest_avg)

    return topic_names, latest_avgs


def generate_topic_chart(progress, output_path=CHART_FILE):
    topic_names, latest_avgs = compute_topic_averages(progress)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(topic_names, latest_avgs, color="#4caf50", alpha=0.7, label="Current")
    ax.set_xlabel("Average Skill Score")
    ax.set_xlim(0, 10)
    ax.set_title("Residency Progress by Major Topic")
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Chart saved → {output_path}")


def update_readme(progress):
    # Generate chart first
    generate_topic_chart(progress)

    sections = []
    sections.append("# 📊 Residency Progress Dashboard\n")
    sections.append("Automatically generated progress overview.\n")
    sections.append(f"![Progress Chart]({CHART_FILE})\n")  # Embed chart at top

    for topic, skills in progress.items():
        print(topic)
        sections.append(generate_topic_markdown(topic, skills))

    markdown = "\n".join(sections)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"README updated → {README_FILE}")


if __name__ == "__main__":
    progress = load_progress()
    update_readme(progress)
