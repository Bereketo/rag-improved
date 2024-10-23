import streamlit as st
from data_loader import load_data, preprocess_data
from embeddings_generator import generate_embeddings
from faiss_index import build_faiss_index
from search import search_query
import  google.generativeai as genai
import os


data_path = "./data/imdb_top_1000.csv"

gemini_api_key = os.getenv('GEMINI_API_KEY')

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not set")

genai.configure(api_key=gemini_api_key)
gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')

@st.cache_data
def load_and_prepare_data():
    df = load_data(data_path)
    df_selected = preprocess_data(df)
    df_selected, embedding_model = generate_embeddings(df_selected)
    index = build_faiss_index(df_selected["Overview_Embeddings"])
    return df_selected, embedding_model, index

df_selected, embedding_model, index = load_and_prepare_data()

st.title("Movie Search App")

st.write("Enter a movie description or plot to find similar movies:")

query = st.text_input("Search query", "")

use_rag = st.checkbox("Use Retrieval-Augmented Generation (RAG)")

if query:
    st.write("Searching for movies similar to your query...")

    results = search_query(query, embedding_model, index, df_selected, use_rag=use_rag)

    if use_rag:
        st.subheader("Generated Response:")
        rag_prompt = f"give more overview for the top 5 movies retrieved but don't explain columns {results}"
        
        response = gemini_model.generate_content(rag_prompt)
        st.write(response.text)
    
    else:
        st.write(f"Top {len(results)} results:")
        for idx, row in results.iterrows():
            st.subheader(row["Series_Title"])
            st.write(f"**Genre:** {row['Genre']}")
            st.write(f"**Director:** {row['Director']}")
            st.write(f"**Overview:** {row['Overview']}")
            st.write(f"**Stars:** {row['Star1']}, {row['Star2']}, {row['Star3']}, {row['Star4']}")
            st.write("---")

if st.checkbox("Show dataset"):
    st.write(df_selected.head(10))

