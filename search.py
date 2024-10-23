import numpy as np
import google.generativeai as genai
import os

Gemini_key = os.getenv('GEMINI_API_KEY')

if not Gemini_key:
    raise ValueError("API_KEY not set")

genai.configure(api_key=Gemini_key)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def search_query(query, model, index, df, k=5, nprobe=10, use_rag=False, rag_model=None, rag_tokenizer=None):
    query_embedding = model.encode(query)
    query_embedding = np.array([query_embedding])

    index.nprobe = nprobe
    distances, indices = index.search(query_embedding, k)
    results = df.iloc[indices[0]]
    
    if use_rag:
        retrieved_docs = "\n".join(results["Overview"].values.tolist())
        prompt = f"Query: {query}\n\nRelevant movie overviews:\n{retrieved_docs}\n\nGenerate a relevant response."

        gemini_response = model.generate_content(prompt)
        response_text = gemini_response.text
        
        return response_text
    else:
        return results

