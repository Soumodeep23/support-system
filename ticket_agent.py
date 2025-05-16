# from langchain.chains import RetrievalQA
# from langchain_community.llms import Ollama
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import OllamaEmbeddings

# embedding_model = OllamaEmbeddings(model="nomic-embed-text")
# db = FAISS.load_local("vectorstore", embedding_model, allow_dangerous_deserialization=True)

# llm = Ollama(model="mistral")

# def query_ticket_knowledgebase(query: str) -> str:
#     # If the user hasn't said enough, don't suggest a fix yet
#     vague_starters = [
#         "i'm facing", "i have a problem", "something's wrong", 
#         "help me", "can you help", "issue", "problem"
#     ]
#     if any(phrase in query.lower() for phrase in vague_starters) and len(query.split()) < 10:
#         return "Of course! 😊 Can you tell me a bit more about the issue you're facing?"

#     # Otherwise continue with the normal RAG response
#     prompt = f"""You're a helpful and friendly AI support agent. Use knowledge from past tickets to help the user.
# Be conversational and wait for enough context before suggesting solutions.

# Conversation so far:
# {query}

# Your reply:"""
#     return llm.invoke(prompt)

# ticket_agent.py
# ticket_agent.py
# ticket_agent.py
from agents.user_input_agent import classify_user_intent
from agents.troubleshooting_agent import suggest_basic_troubleshooting
from agents.retriever_agent import retrieve_similar_tickets
from agents.confirmation_agent import confirm_resolution
from chat_history import save_chat

def query_ticket_knowledgebase(user_input: str, chat_id=None) -> str:
    intent = classify_user_intent(user_input)
    if chat_id:
        save_chat(user_input, f"[Detected Intent: {intent}]")

    if intent == "AskSolution":
        similar = retrieve_similar_tickets(user_input)
        suggestion = suggest_basic_troubleshooting(user_input)
        response = (
            f"{similar}\n\n\ud83d\udca1 Here's a possible fix you can try:\n{suggestion}\n\n"
            "✅ Let me know if that helps or if you need more assistance."
        )

    elif intent == "AskTicketStatus":
        response = (
            "📬 I'd be glad to help with your ticket status. "
            "Could you please provide your Ticket ID?"
        )

    elif intent == "Frustration":
        response = (
            "😟 I'm really sorry you're feeling this way. "
            "Let’s work through it together. Can you tell me more about the issue you're facing?"
        )

    elif intent == "GeneralGreeting":
        response = "👋 Hey there! How can I assist you today with your support concern?"

    elif intent == "Approved" or intent == "Unapproved":
        response = confirm_resolution(user_input)
        if intent == "Approved":
            response = "🎉 I'm happy your problem is resolved! Have a great day!"
        else:
            response = "😥 Okay, please tell me more about the issue."
    else:
        response = (
            "Of course! 😊 Can you tell me a bit more about the issue you're facing? "
            "I’d love to help once I understand better."
        )

    if chat_id:
        save_chat(user_input, response)

    return response

