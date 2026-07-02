import json
import faiss
import numpy as np
from sentence_transformers import (
    SentenceTransformer
)


class Retriever:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.index = faiss.read_index(
            "data/faiss.index"
        )

        with open(
            "data/catalog.json",
            "r",
            encoding="utf-8"
        ) as f:
            self.catalog = json.load(f)

    def retrieve(
        self,
        query,
        top_k=5
    ):

        query_embedding = self.model.encode(
            [query]
        )

        query_embedding = np.array(
            query_embedding,
            dtype=np.float32
        )

        distances, indices = (
            self.index.search(
                query_embedding,
                top_k
            )
        )

        results = []

        for idx in indices[0]:
            results.append(
                self.catalog[idx]
            )

        return results