from typing import List
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS = 384

_model_instance = None

def get_embedding_model() -> SentenceTransformer:
    global _model_instance
    if _model_instance is None:
        print(f"[RAGLens] Loading SentenceTransformer model: {MODEL_NAME}...")
        _model_instance = SentenceTransformer(MODEL_NAME)
        print(f"[RAGLens] Model {MODEL_NAME} loaded successfully ({EMBEDDING_DIMENSIONS} dimensions).")
    return _model_instance

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate 384-dimensional dense embeddings for a list of text strings.
    """
    if not texts:
        return []
    model = get_embedding_model()
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    return embeddings.tolist()

def generate_single_embedding(text: str) -> List[float]:
    """
    Generate embedding vector for a single query text string.
    """
    model = get_embedding_model()
    embedding = model.encode(text, convert_to_numpy=True, show_progress_bar=False)
    return embedding.tolist()
