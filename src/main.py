
import csv

input_file = "data/apps.csv"
output_file = "reports/app_research.csv"

with open(input_file, "r", encoding="utf-8") as file:
    apps = list(csv.DictReader(file))

fields = [
    "id",
    "app_name",
    "category",
    "description",
    "auth_methods",
    "access_model",
    "api_surface",
    "mcp_support",
    "buildability_verdict",
    "main_blocker",
    "evidence_url"
]

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()

    for app in apps:
        writer.writerow({
            "id": app["id"],
            "app_name": app["app_name"],
            "category": app["category"]
        })

print("Research template generated!")
print("Total apps prepared:", len(apps))
print("Saved to:", output_file)
