# agents/retriever_agent.py
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from tools.rag_vectorstore import load_vector_db

llm = Ollama(model="mistral")
db = load_vector_db()

retriever_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

def retrieve_similar_tickets(query):
    return retriever_chain.run(query)
