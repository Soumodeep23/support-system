# chat_history.py
import os
import json
import uuid
from datetime import datetime, timedelta

HISTORY_DIR = "chat_history"
RETENTION_DAYS = 3

os.makedirs(HISTORY_DIR, exist_ok=True)

def _get_history_files():
    return [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]

def save_chat(message: str, response: str):
    now = datetime.now()
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": now.isoformat(),
        "message": message,
        "response": response,
    }
    filename = f"{now.strftime('%Y%m%d')}.json"
    path = os.path.join(HISTORY_DIR, filename)

    data = []
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)

    data.append(entry)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_recent_chats():
    recent_chats = []
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)

    for file in _get_history_files():
        file_date = datetime.strptime(file.replace(".json", ""), "%Y%m%d")
        if file_date >= cutoff:
            with open(os.path.join(HISTORY_DIR, file), "r") as f:
                recent_chats.extend(json.load(f))

    return sorted(recent_chats, key=lambda x: x["timestamp"], reverse=True)

def clean_old_chats():
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)
    for file in _get_history_files():
        file_date = datetime.strptime(file.replace(".json", ""), "%Y%m%d")
        if file_date < cutoff:
            os.remove(os.path.join(HISTORY_DIR, file))
