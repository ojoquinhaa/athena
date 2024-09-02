from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.history import RunnableWithMessageHistory

from athena.model import ollama as model
from athena.history import get_session_history, get_session_id
from athena.prompt import aprint

session_id = get_session_id()
history = get_session_history(session_id)

chat = RunnableWithMessageHistory(model, get_session_history)
config = {"configurable": {"session_id": session_id}}

def get_system_message():
    try:
        with open('system.txt', 'r') as system_file:
            system_message = system_file.read()

            if system_message == "":
                raise FileNotFoundError

            return system_message
        
    except FileExistsError:
        aprint(f"The file {FileExistsError.filename} is required.", "error")

def add_system_message(system_message:str):
    global history
    history.add_message(SystemMessage(content=system_message))

def messaging(message:str) -> str:
    global config, history

    response = chat.invoke([HumanMessage(content=message)], config=config)

    return response.content