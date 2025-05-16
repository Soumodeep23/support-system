# agents/confirmation_agent.py
def confirm_resolution(user_feedback: str) -> str:
    if "no" in user_feedback.lower():
        return "😥 Okay, please tell me more about the issue."
    else:
        return "🎉 I'm happy your problem is resolved! Have a great day!"
