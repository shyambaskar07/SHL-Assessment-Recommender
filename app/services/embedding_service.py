from sentence_transformers import SentenceTransformer
import numpy as np
import json
import faiss
import os


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def build_index(self):

        with open(
            "data/catalog.json",
            "r",
            encoding="utf-8"
        ) as f:
            catalog = json.load(f)

        texts = []

        for item in catalog:

            text = f"""
            {item.get("name", "")}
            {item.get("description", "")}
            {' '.join(item.get("job_levels", []))}
            {' '.join(item.get("keys", []))}
            """

            texts.append(text)

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True
        )

        embeddings = np.array(
            embeddings,
            dtype=np.float32
        )

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(
            dimension
        )

        index.add(embeddings)

        faiss.write_index(
            index,
            "data/faiss.index"
        )

        np.save(
            "data/embeddings.npy",
            embeddings
        )

        print(
            f"Indexed {len(catalog)} assessments"
        )