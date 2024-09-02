from colorama import Fore, init, Style
from ascii_magic import AsciiArt
from time import sleep
from sys import stdout
from threading import Thread

init(autoreset=True)

def aprint(message: str, category: str):
    templates = {
        "warning": f"{Fore.YELLOW}[!] - {message}",
        "error": f"{Fore.RED}[-] - {message}",
        "ok": f"{Fore.GREEN}[+] - {message}",
        "system": f"{Fore.BLUE}[*] - {message}",
        "question": f"{Fore.CYAN}[?] - {message}",
        "ia": f"${Fore.BLUE}athenas: {Fore.MAGENTA}{message}"
    }
    
    print(templates.get(category.lower(), message))

def show_header():
    logo = AsciiArt.from_image('img/logo.jpeg')
    logo.to_terminal()

def get_user_input():
    prefix = f"{Fore.BLUE}: {Fore.RESET}"
    return input(prefix).strip()

def ia_load(response_callable, *args, **kwargs):
    def loading_bar():
        while not response_ready:
            for char in "|/-\\":
                stdout.write(f'\r{Fore.YELLOW}{char} {Fore.CYAN}Thinking...{Style.RESET_ALL}')
                stdout.flush()
                sleep(0.2)

    global response_ready
    response_ready = False
    
    loader = Thread(target=loading_bar)
    loader.start()

    response = response_callable(*args, **kwargs)

    response_ready = True  
    loader.join()  

    print('')
    return response
