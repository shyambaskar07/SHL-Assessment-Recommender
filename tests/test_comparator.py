import json

from app.services.comparator import Comparator

with open(
    "data/catalog.json",
    "r",
    encoding="utf-8"
) as f:
    catalog = json.load(f)

java = None
javascript = None

for item in catalog:

    if (
        "java 8"
        in item["name"].lower()
    ):
        java = item

    if (
        "javascript"
        in item["name"].lower()
    ):
        javascript = item

if java and javascript:

    comparison = (
        Comparator()
        .compare(
            java,
            javascript
        )
    )

    print(comparison)