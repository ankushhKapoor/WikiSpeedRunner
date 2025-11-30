from sentence_transformers import SentenceTransformer
import numpy as np

class SBERTEncoder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, text: str):
        return self.model.encode(text, normalize_embeddings=True)

    def rank_list(self, target_emb, summaries):
        embs = self.model.encode(summaries, normalize_embeddings=True)
        scores = embs @ target_emb
        return np.argmax(scores)