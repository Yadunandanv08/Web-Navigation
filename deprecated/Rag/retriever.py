import faiss
import numpy as np


class Retriever:
    def __init__(self, embedder):
        self.embedder = embedder
        self.index = None
        self.texts = []
        self.metadata = []

    def index_data(self, texts: list[str], metadata: list[dict] | None = None):
        self.texts = texts
        self.metadata = metadata or [{} for _ in texts]

        vectors = np.array(self.embedder.embed(texts)).astype("float32")
        dim = vectors.shape[1]

        self.index = faiss.IndexFlatIP(dim)  # cosine (with normalized vectors)
        self.index.add(vectors)

    def retrieve(self, query: str, top_k: int = 5):
        if self.index is None:
            return []

        q = np.array(self.embedder.embed([query])).astype("float32")
        scores, indices = self.index.search(q, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            results.append({
                "score": float(score),
                "text": self.texts[idx],
                "metadata": self.metadata[idx],
            })

        return results
