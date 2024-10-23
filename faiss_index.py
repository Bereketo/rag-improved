import faiss
import numpy as np


def build_faiss_index(embeddings):
    """Build and return faiss IVF index"""
    dimensions = embeddings[0].shape[0]
    nlist = 30
    quantizer = faiss.IndexFlatL2(dimensions)
    index = faiss.IndexIVFFlat(quantizer, dimensions, nlist, faiss.METRIC_L2)

    embeddings_array = np.array(embeddings.tolist())

    assert not index.is_trained
    index.train(embeddings_array)
    assert index.is_trained

    index.add(embeddings_array)
    return index
