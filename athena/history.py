import os
import json

from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.messages import HumanMessage, AIMessage

from dotenv import load_dotenv, set_key
from uuid import uuid4

store = {}
load_dotenv()

def get_session_id():
    session_id = os.getenv('SESSION_ID')
    
    if session_id is None:
        session_id = str(uuid4())
        dotenv_path = os.path.join(os.getcwd(), '.env')
        set_key(dotenv_path, 'SESSION_ID', session_id)
    
    return session_id

def save_history_to_file(session_id: str, history: BaseChatMessageHistory):
    filename = f"{session_id}_history.json"
    with open(filename, 'w') as file:
        json.dump([{"type": msg.type, "content": msg.content} for msg in history.messages], file)

def load_history_from_file(session_id: str) -> BaseChatMessageHistory:
    filename = f"{session_id}_history.json"
    history = InMemoryChatMessageHistory()
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                messages = json.load(file)
            except:
                return history

            for msg in messages:
                if msg["type"] == "humam":
                    history.add_message(HumanMessage(msg["content"]))
                elif msg["type"] == "ai":
                    history.add_ai_message(AIMessage(msg["content"]))
    return history

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = load_history_from_file(session_id)
    return store[session_id]