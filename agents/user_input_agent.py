from langchain_community.llms import Ollama

llm = Ollama(model="mistral")

def classify_user_intent(user_input: str) -> str:
    prompt = f"""
You are a helpful and intelligent AI support assistant. Classify the user's intent strictly into one of these categories:
1. AskSolution - If user is reporting a technical problem or asking for help with something not working.
2. AskTicketStatus - If user is asking about a Ticket ID or wants to know the ticket progress.
3. GeneralGreeting - If the user is just greeting or saying hello, hi, hey in the sentence.
4. Frustration - If the user seems upset, angry, or in a hurry.
5. Approved - If the user is satisfied with the solution or has no further questions, or saying thank you in the sentence.
6. Unapproved - If the user is not satisfied with the solution or has further questions, or saying not satisfied in the sentence.
Respond ONLY with the exact label: AskSolution, AskTicketStatus, GeneralGreeting, Frustration, Approved or Unapproved .
If user is just greeting, respond with GeneralGreeting.
if user is asking for a solution, respond with AskSolution in detail with a long solution.
if user is saying not satisfied, respond with appologies and Unapproved.
User Input: {user_input}
Intent:"""
    result = llm.invoke(prompt).strip()
    return result.split()[0]  # just to be safe
