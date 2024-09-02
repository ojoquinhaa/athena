import athena.chat as chat
import athena.prompt as prompt

from athena.history import save_history_to_file

prompt.show_header()

SYSTEM_MESSAGE = chat.get_system_message()
SESSION_ID = chat.get_session_id()

chat.add_system_message(SYSTEM_MESSAGE)

if __name__ == "__main__":
    try:
        while True:
            user_input = prompt.get_user_input()
            
            response = prompt.ia_load(chat.messaging, user_input)
            prompt.aprint(response, "ia")
    except KeyboardInterrupt:
        prompt.aprint('Goodbye :)', "ia")

        history = chat.get_session_history(SESSION_ID)
        save_history_to_file(SESSION_ID, history)

        exit(0)
