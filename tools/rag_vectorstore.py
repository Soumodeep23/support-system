# tools/rag_vectorstore.py
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

def load_vector_db():
    embedding_model = OllamaEmbeddings(model="bge-m3")
    return FAISS.load_local("vectorstore", embedding_model, allow_dangerous_deserialization=True)
