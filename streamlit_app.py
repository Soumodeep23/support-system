# streamlit_app.py
import streamlit as st
from PIL import Image
from io import BytesIO

from chat_history import save_chat, load_recent_chats, clean_old_chats
from ticket_agent import query_ticket_knowledgebase
from vision_agent import handle_image_query

# Custom CSS for dark theme and styling
st.set_page_config(page_title="Support Assistant", layout="centered")
st.title("🧠 AI Support Assistant")

st.markdown(
    """
    <style>
    .stApp { background-color: #1a1a1a; color: #ffffff; }
    .user-message { background-color: #ff6b6b; padding: 10px; border-radius: 10px; margin: 5px 0; }
    .ai-message { background-color: #f4a261; padding: 10px; border-radius: 10px; margin: 5px 0; }
    .stSidebar { background-color: #2a2a2a; color: #ffffff; }
    .stTextInput > div > div > input { background-color: #333333; color: #ffffff; border-radius: 10px; }
    .stButton > button { background-color: #e76f51; color: #ffffff; border-radius: 10px; width: 100%; }
    </style>
    """,
    unsafe_allow_html=True
)

# Clean up old chats
clean_old_chats()

# Initialize session state
if "chat_log" not in st.session_state:
    st.session_state.chat_log = [("🧠 AI Support Assistant", "Hi there! How can I help you today? 😊")]

# Sidebar Chat History
with st.sidebar:
    st.markdown("### 🕒 Chat History")
    history = load_recent_chats()
    if history:
        for entry in history[:7]: # we can increase or decrease the number of saved chat histories here
            st.markdown(f"**🧑 You:** {entry['message']}", unsafe_allow_html=True)
            st.markdown(f"**🤖 AI:** {entry['response']}", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.info("No chat history yet.")

# Main Interface
# Input area
with st.container():
    st.markdown("<hr>", unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Type your message here:", label_visibility="collapsed", key="user_input")
        uploaded_image = st.file_uploader("Attach an image (optional)", type=["jpg", "png", "jpeg"], key="file_uploader")
    with col2:
        send_clicked = st.button("Send")

# Process response
if send_clicked:
    if not user_input.strip() and not uploaded_image:
        st.warning("Please type a message or upload an image.")
    else:
        with st.spinner("Thinking..."):
            if uploaded_image:
                image = Image.open(BytesIO(uploaded_image.read()))
                response = handle_image_query(user_input or "Please describe this image", image)
            else:
                response = query_ticket_knowledgebase(user_input)

            st.session_state.chat_log.append((user_input, response))
            save_chat(user_input, response)
            st.rerun()

# Display chat log
st.markdown("---")
for message, reply in st.session_state.chat_log:
    sanitized_message = message.encode("utf-8", "ignore").decode("utf-8")
    sanitized_reply = reply.encode("utf-8", "ignore").decode("utf-8")
    st.chat_message("user", avatar="🧑").markdown(f"<div class='user-message'>{sanitized_message}</div>", unsafe_allow_html=True)
    st.chat_message("ai", avatar="🤖").markdown(f"<div class='ai-message'>{sanitized_reply}</div>", unsafe_allow_html=True)