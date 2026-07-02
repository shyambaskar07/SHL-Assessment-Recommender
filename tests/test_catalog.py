import json

with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

print(f"Loaded {len(catalog)} assessments")

print("\nFirst assessment:")
print(catalog[0]["name"])