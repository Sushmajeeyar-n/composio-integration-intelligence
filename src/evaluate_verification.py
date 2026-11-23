
import csv
from pathlib import Path
from collections import Counter

EVIDENCE_FILE = Path("reports/classified_evidence.csv")
REVIEW_FILE = Path("verification/first_pass_review.csv")
OUTPUT_FILE = Path("verification/evaluation_report.csv")

# Load agent evidence
with open(EVIDENCE_FILE, "r", encoding="utf-8-sig", newline="") as file:
    evidence_rows = list(csv.DictReader(file))

# Load human review
with open(REVIEW_FILE, "r", encoding="utf-8-sig", newline="") as file:
    reviewed_rows = list(csv.DictReader(file))

# Match by exact app name and evidence title
evidence_lookup = {
    (row["app_name"], row["evidence_title"]): row
    for row in evidence_rows
}

results = []
excluded = 0

for review in reviewed_rows:
    key = (review["app_name"], review["evidence_title"])
    evidence = evidence_lookup.get(key)

    if not evidence:
        print("Could not find:", key)
        continue

    human_label = review["domain_check"]
    agent_label = evidence["source_type"]

    # Potentially official is uncertain, so exclude it from scoring
    if human_label == "Potentially official":
        excluded += 1
        agreement = "Not scored - uncertain"
    else:
        human_official = human_label == "Official"
        agent_official = agent_label == "Official-domain match"

        agreement = (
            "Match" if human_official == agent_official else "Mismatch"
        )

    results.append({
        "app_name": review["app_name"],
        "evidence_title": review["evidence_title"],
        "agent_classification": agent_label,
        "human_classification": human_label,
        "classification_agreement": agreement,
        "human_relevance_review": review["relevance_check"],
        "review_note": review["review_note"]
    })

scored = [
    row for row in results
    if row["classification_agreement"] != "Not scored - uncertain"
]

matches = sum(
    row["classification_agreement"] == "Match"
    for row in scored
)

print("\nVERIFICATION REPORT")
print("-------------------")
print("Matched review examples:", len(results))
print("Scored examples:", len(scored))
print("Excluded uncertain examples:", excluded)

if scored:
    print(
        "Classification agreement:",
        round(matches / len(scored) * 100, 2),
        "%"
    )

print("\nHuman relevance review:")
for label, count in Counter(
    row["human_relevance_review"] for row in results
).items():
    print(f"{label}: {count}")

print("\nIndividual results:")
for row in results:
    print(
        row["app_name"],
        "|",
        row["evidence_title"],
        "|",
        row["classification_agreement"],
        "| Relevance:",
        row["human_relevance_review"]
    )

if results:
    with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

print("\nSaved evaluation to:", OUTPUT_FILE)
