from sentence_transformers import SentenceTransformer
import numpy as np
from datasets import Dataset
from faiss_index import build_faiss_index
import faiss


def generate_embeddings(df, model_name="all-mpnet-base-v2"):
    """Generate embeddings using SentenceTransformer model."""
    model = SentenceTransformer(model_name)
    df["Overview_Embeddings"] = df["Overview"].apply(
        lambda x: model.encode(x).astype(np.float32)
    )
    return df, model
