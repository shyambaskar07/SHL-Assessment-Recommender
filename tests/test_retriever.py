from app.services.retriever import Retriever

retriever = Retriever()

results = retriever.retrieve(
    "Java developer with communication skills",
    top_k=5
)

for r in results:
    print(
        r["name"]
    )