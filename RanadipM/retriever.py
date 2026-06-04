"""
Lightweight RAG retriever.

Uses TF-IDF + cosine similarity over the seed knowledge base so the demo
needs no external vector DB. The interface (retrieve -> top-k passages)
mirrors what a production ChromaDB / pgvector layer would expose, so the
rest of the app is agnostic to the backend.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data.knowledge_base import KNOWLEDGE_BASE


class Retriever:
    def __init__(self):
        self.docs = KNOWLEDGE_BASE
        corpus = [f"{d['title']}. {d['text']}" for d in self.docs]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(corpus)

    def retrieve(self, query: str, k: int = 3, category: str | None = None):
        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.matrix)[0]
        ranked = sorted(
            range(len(self.docs)), key=lambda i: sims[i], reverse=True
        )
        results = []
        for i in ranked:
            doc = self.docs[i]
            if category and doc["category"] != category:
                continue
            if sims[i] <= 0.0:
                continue
            results.append(
                {
                    "id": doc["id"],
                    "title": doc["title"],
                    "text": doc["text"],
                    "category": doc["category"],
                    "score": round(float(sims[i]), 3),
                }
            )
            if len(results) >= k:
                break
        return results


# Singleton so the index is built once per session.
_retriever = None


def get_retriever() -> Retriever:
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever
