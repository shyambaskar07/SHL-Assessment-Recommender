import json
import requests
from bs4 import BeautifulSoup

with open(
    "data/raw_urls.json",
    "r",
    encoding="utf-8"
) as f:
    urls = json.load(f)

catalog = []

for url in urls:

    try:
        response = requests.get(
            url,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )

        title = soup.find("h1")

        if title:
            name = title.text.strip()
        else:
            continue

        description = ""

        meta = soup.find(
            "meta",
            attrs={
                "name": "description"
            }
        )

        if meta:
            description = meta.get(
                "content",
                ""
            )

        catalog.append(
            {
                "name": name,
                "url": url,
                "description": description
            }
        )

        print(name)

    except Exception as e:
        print(url, e)

with open(
    "data/catalog.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        catalog,
        f,
        indent=4,
        ensure_ascii=False
    )

print(
    f"Saved {len(catalog)} assessments"
)