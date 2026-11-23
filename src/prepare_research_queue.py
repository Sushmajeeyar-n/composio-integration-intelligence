
import csv
from pathlib import Path
from collections import defaultdict

EVIDENCE_FILE = Path("reports/research_evidence_v2.csv")
APPS_FILE = Path("data/apps.csv")
RESEARCH_FILE = Path("reports/app_research.csv")
OUTPUT_FILE = Path("reports/research_queue.csv")

# Load the app list
with open(APPS_FILE, "r", encoding="utf-8-sig", newline="") as file:
    apps = list(csv.DictReader(file))

# Load the improved evidence
with open(EVIDENCE_FILE, "r", encoding="utf-8-sig", newline="") as file:
    evidence = list(csv.DictReader(file))

# Check which apps already have research
with open(RESEARCH_FILE, "r", encoding="utf-8-sig", newline="") as file:
    research = list(csv.DictReader(file))

researched_apps = {
    row["app_name"]
    for row in research
    if row.get("description", "").strip()
}

# Group evidence by app
grouped = defaultdict(list)

for item in evidence:
    grouped[item["app_name"]].append(item)

queue = []

for app in apps:
    name = app["app_name"]
    candidates = grouped.get(name, [])

    # Keep the three highest-scoring results
    candidates.sort(
        key=lambda item: int(item.get("priority_score") or 0),
        reverse=True
    )

    for rank, item in enumerate(candidates[:3], start=1):
        queue.append({
            "app_name": name,
            "category": app["category"],
            "research_status": (
                "Existing research - review"
                if name in researched_apps
                else "Needs research"
            ),
            "evidence_rank": rank,
            "evidence_title": item["evidence_title"],
            "evidence_url": item["evidence_url"],
            "priority_score": item["priority_score"],
            "review_status": item["review_status"]
        })

columns = [
    "app_name",
    "category",
    "research_status",
    "evidence_rank",
    "evidence_title",
    "evidence_url",
    "priority_score",
    "review_status"
]

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(queue)

print("Research queue created!")
print("Apps processed:", len(apps))
print("Evidence links queued:", len(queue))
print("Apps with existing research:", len(researched_apps))
print("Saved to:", OUTPUT_FILE)
