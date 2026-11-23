import csv
from pathlib import Path
from urllib.parse import urlparse
from collections import Counter

APPS_FILE = Path("data/apps.csv")
EVIDENCE_FILE = Path("reports/research_evidence.csv")
OUTPUT_FILE = Path("reports/classified_evidence.csv")


def get_domain(url):
    if not url:
        return ""

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return urlparse(url).hostname.lower().removeprefix("www.") or ""


# Load app names and their official website hints
with open(APPS_FILE, "r", encoding="utf-8-sig", newline="") as file:
    apps = list(csv.DictReader(file))

official_domains = {}

for app in apps:
    official_domains[app["app_name"]] = get_domain(
        app.get("website_hint", "")
    )


# Read collected search evidence
with open(EVIDENCE_FILE, "r", encoding="utf-8-sig", newline="") as file:
    evidence = list(csv.DictReader(file))

classified = []

for item in evidence:
    app_name = item["app_name"]
    result_domain = get_domain(item.get("evidence_url", ""))
    official_domain = official_domains.get(app_name, "")

    if official_domain and (
        result_domain == official_domain
        or result_domain.endswith("." + official_domain)
    ):
        source_type = "Official-domain match"
    else:
        source_type = "Not an official-domain match - review"

    item["source_domain"] = result_domain
    item["source_type"] = source_type
    classified.append(item)


# Save classified evidence
columns = list(classified[0].keys()) if classified else []

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(classified)


counts = Counter(item["source_type"] for item in classified)

print("Evidence classification completed!")
print("Total results:", len(classified))

for label, count in counts.items():
    print(f"{label}: {count}")

print("Saved to:", OUTPUT_FILE)
