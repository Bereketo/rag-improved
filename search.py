import numpy as np
import os


def search_query(query, model, index, df, k=5, nprobe=10, use_rag=False, rag_model=None, rag_tokenizer=None):
    query_embedding = model.encode(query)
    query_embedding = np.array([query_embedding])

    index.nprobe = nprobe
    distances, indices = index.search(query_embedding, k)
    results = df.iloc[indices[0]]
    
    return results

