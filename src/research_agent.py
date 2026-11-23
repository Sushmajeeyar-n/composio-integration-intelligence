
import csv
import time
from pathlib import Path
from urllib.parse import urlparse
from ddgs import DDGS

INPUT_FILE = Path("data/apps.csv")
OUTPUT_FILE = Path("reports/research_evidence_v2.csv")

OUTPUT_FILE.parent.mkdir(exist_ok=True)

# Terms that suggest useful developer documentation
PRIORITY_TERMS = [
    "developer", "developers", "api", "docs",
    "documentation", "authentication", "oauth",
    "mcp", "reference", "getting started"
]

# Terms that suggest less authoritative results
LOW_PRIORITY_TERMS = [
    "reddit", "medium.com", "tutorial",
    "github.com", "comparison", "alternatives"
]


def score_result(title, url, snippet):
    text = f"{title} {url} {snippet}".lower()
    score = 0

    for term in PRIORITY_TERMS:
        if term in text:
            score += 2

    for term in LOW_PRIORITY_TERMS:
        if term in text:
            score -= 2

    domain = urlparse(url).hostname or ""

    if "developer" in domain or "docs" in domain:
        score += 3

    return score


with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as file:
    apps = list(csv.DictReader(file))

results = []

print(f"Starting improved research for {len(apps)} apps...\n")

with DDGS() as ddgs:
    for index, app in enumerate(apps, start=1):
        name = app["app_name"]
        print(f"[{index}/100] Searching: {name}")

        query = f"{name} official developer API documentation authentication MCP"

        try:
            search_results = list(ddgs.text(query, max_results=5))

            for item in search_results:
                title = item.get("title", "")
                url = item.get("href", "")
                snippet = item.get("body", "")

                score = score_result(title, url, snippet)

                results.append({
                    "app_name": name,
                    "evidence_title": title,
                    "evidence_url": url,
                    "evidence_snippet": snippet,
                    "priority_score": score,
                    "review_status": "Needs human verification"
                })

        except Exception as error:
            print("Search error:", error)

        time.sleep(1)

# Highest priority results first
results.sort(key=lambda row: row["priority_score"], reverse=True)

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as file:
    columns = [
        "app_name",
        "evidence_title",
        "evidence_url",
        "evidence_snippet",
        "priority_score",
        "review_status"
    ]

    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(results)

print("\nImproved research search completed!")
print("Apps processed:", len(apps))
print("Evidence collected:", len(results))
print("Saved to:", OUTPUT_FILE)
