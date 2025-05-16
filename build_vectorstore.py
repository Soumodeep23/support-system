import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
import os

# ✅ Load your CSV file
df = pd.read_csv("Historical_ticket_data.csv")
df.columns = df.columns.str.strip()  # ✨ Fix column names

# ✅ Combine relevant fields
texts = [
    f"Ticket ID: {row['Ticket ID']}\nIssue: {row['Issue Category']}\nSentiment: {row['Sentiment']}\nPriority: {row['Priority']}\nSolution: {row['Solution']}"
    for _, row in df.iterrows()
]
metadata = [{"ticket_id": row["Ticket ID"]} for _, row in df.iterrows()]

# ✅ Generate embeddings and store them
embedding_model = OllamaEmbeddings(model="bge-m3")
vector_db = FAISS.from_texts(texts, embedding_model, metadatas=metadata)

os.makedirs("vectorstore", exist_ok=True)
vector_db.save_local("vectorstore")

print("✅ Vectorstore built and saved!")
