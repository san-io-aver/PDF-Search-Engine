import fitz
import streamlit as st
import faiss
from pdf_text import extract_text
from sentence_transformers import SentenceTransformer


@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()
def get_text():
    files = st.file_uploader("Upload a PDF file", type=["pdf"],accept_multiple_files=True)
    text=""
    for file in files:
        if file:
            try:    
                for page in fitz.open(stream=file.read(), filetype="pdf"):
                    text += page.get_text()    
            except Exception as e:
                st.warning(f"Error reading PDF file: {e}")  
    return text if text.strip() else None
     
def get_chunks(text,chunk_size=600,overlap=100):
    chunks=[]
    for i in range(0,len(text),chunk_size-overlap):
        chunk=text[i:i+chunk_size]
        if len(chunk)>0:
            chunks.append(chunk)
    return chunks

def get_embeddings(chunks):
    chunk_embeddings = model.encode(chunks)
    return chunk_embeddings

def add_to_index(embeddings):
    embedding_dim = len(embeddings[0])
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(embeddings)
    st.success("Embeddings added to index successfully!")
    return index

def get_query():
    query=st.text_input("Enter your query:")
    if query:
        query_embedding = model.encode([query])
        return query_embedding
    st.warning("Please enter a query to search.")
    return None   
def search_index(query_embedding,index,chunks):
    dist, indices = index.search(query_embedding, k=3)
    results=[]
    for idx in indices[0]:
        results.append(chunks[idx])
    return results

def display_results(result):
    if result:
        with st.expander("Search Results"):
            for res in result:
                st.write(res)
    else:
        st.warning("No results found for the query.")
st.set_page_config(page_title="Personal PDF Search Engine", layout="wide")
st.title("Personal PDF Search Engine")
model = load_model()

text = get_text()
if text:
    chunks = get_chunks(text)
    chunk_embeddings = get_embeddings(chunks)
    index = add_to_index(chunk_embeddings)
    
    query_embedding=get_query()
    if query_embedding is not None:
        result = search_index(query_embedding,index,chunks)
        display_results(result)
    

