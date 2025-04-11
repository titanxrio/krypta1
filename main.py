import os
import sys
import time
import requests
from io import BytesIO
from PIL import Image, ImageSequence

# Farben + Styling (pystyle wird genutzt, falls nicht vorhanden, wird es installiert)
try:
    from pystyle import Colorate, Colors
except ImportError:
    os.system("pip install pystyle")
    from pystyle import Colorate, Colors

# Raw URLs für alle Tools – 8 Tools, verteilt auf 4 Seiten
tools = {
    "discord": {
        "tool1": "https://raw.discordtool1.com/code.py",
        "tool2": "https://raw.discordtool2.com/code.py"
    },
    "updates": {
        "tool1": "https://raw.updatetool1.com/code.py",
        "tool2": "https://raw.updatetool2.com/code.py"
    },
    "info": {
        "tool1": "https://raw.infotool1.com/code.py",
        "tool2": "https://raw.infotool2.com/code.py"
    },
    "settings": {
        "tool1": "https://raw.settingstool1.com/code.py",
        "tool2": "https://raw.settingstool2.com/code.py"
    }
}

# URL zur globalen Loading-Animation (Python-Code in load.py)
LOADING_ANIMATION_CODE_URL = "https://raw.githubusercontent.com/titanxrio/krypta1/refs/heads/main/load.py"

# Erforderlicher Schlüssel für den globalen Zugang
REQUIRED_KEY = "titan"

def clear():
    os.system('cls' if os.name == "nt" else "clear")

def styled_left(text):
    return Colorate.Horizontal(Colors.purple_to_blue, text)

def execute_loading_animation_code(url):
    """
    Lädt den Python-Code für die Loading-Animation von der Remote-URL
    und führt ihn aus, sodass auch __main__ korrekt getriggert wird.
    """
    try:
        import requests
    except ImportError:
        os.system("pip install requests")
        import requests

    try:
        response = requests.get(url)
        if response.status_code == 200:
            code = response.text
            # __name__ als '__main__' setzen, damit load.py korrekt startet
            exec(code, {'__name__': '__main__'})
        else:
            print(styled_left(f"Error loading animation code (Status Code: {response.status_code})"))
            time.sleep(1)
    except Exception as e:
        print(styled_left(f"Animation code error: {e}"))
        time.sleep(1)

def key_prompt():
    """
    Zeigt einen Key-Prompt in ASCII-Art an und fragt nach dem Schlüssel.
    """
    clear()
    key_art = r"""
██╗  ██╗██████╗ ██╗   ██╗██████╗ ████████╗ █████╗ 
██║ ██╔╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔══██╗
█████╔╝ ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ███████║
██╔═██╗ ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██╔══██║
██║  ██╗██║  ██║   ██║   ██║        ██║   ██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   ╚═╝  ╚═╝
    """
    print(styled_left(key_art))
    return input(styled_left("Enter key to access tool system: ")).strip().lower()

def landing_page():
    """
    Zeigt die Updates-Landing-Page an.
    """
    clear()
    page_content = r"""
██   ██ ██████  ██    ██ ██████  ████████  █████
██  ██  ██   ██  ██  ██  ██   ██    ██    ██   ██
█████   ██████    ████   ██████     ██    ███████
██  ██  ██   ██    ██    ██         ██    ██   ██
██   ██ ██   ██    ██    ██         ██    ██   ██

─────────────────────────────[ UPDATES ]─────────────────────────────

> update the checker
> Update discord tool

[PRESS ENTER TO ACCESS]
"""
    print(styled_left(page_content))
    input()

def run_tool(category, tool_option):
    """
    Ruft den Code des gewählten Tools von der Remote-URL ab und führt ihn aus.
    """
    try:
        import requests
    except ImportError:
        os.system("pip install requests")
        import requests
    url = tools[category]["tool" + tool_option]
    try:
        response = requests.get(url)
        if response.status_code == 200:
            code = response.text
            exec(code)
        else:
            print(styled_left("Error: Could not fetch tool (Status Code: {})".format(response.status_code)))
    except Exception as e:
        print(styled_left("Error executing tool: {}".format(e)))
    input(styled_left("Press Enter to return to the main menu..."))

def discord_page(page, total_pages):
    clear()
    ascii_art = r"""

██╗  ██╗██████╗ ██╗   ██╗██████╗ ████████╗ █████╗ 
██║ ██╔╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔══██╗
█████╔╝ ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ███████║
██╔═██╗ ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██╔══██║
██║  ██╗██║  ██║   ██║   ██║        ██║   ██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   ╚═╝  ╚═╝
                                                  
"""
    page_content = rf"""{ascii_art}
─────────────────────────────[ DISCORD ]───────────────────────────── [PAGE {page}/{total_pages}]

[1] > Discord Tool 1
[2] > Discord Tool 2

[N] Next Page   |   [B] Back Page   |   [Q] Quit
"""
    print(styled_left(page_content))

def updates_page(page, total_pages):
    clear()
    ascii_art = r"""

██╗  ██╗██████╗ ██╗   ██╗██████╗ ████████╗ █████╗ 
██║ ██╔╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔══██╗
█████╔╝ ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ███████║
██╔═██╗ ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██╔══██║
██║  ██╗██║  ██║   ██║   ██║        ██║   ██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   ╚═╝  ╚═╝
                                                  
"""
    page_content = rf"""{ascii_art}
─────────────────────────────[ UPDATES ]───────────────────────────── [PAGE {page}/{total_pages}]

[1] > Update Tool 1
[2] > Update Tool 2

[N] Next Page   |   [B] Back Page   |   [Q] Quit
"""
    print(styled_left(page_content))

def info_page(page, total_pages):
    clear()
    ascii_art = r"""

██╗  ██╗██████╗ ██╗   ██╗██████╗ ████████╗ █████╗ 
██║ ██╔╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔══██╗
█████╔╝ ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ███████║
██╔═██╗ ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██╔══██║
██║  ██╗██║  ██║   ██║   ██║        ██║   ██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   ╚═╝  ╚═╝
                                                  
"""
    page_content = rf"""{ascii_art}
─────────────────────────────[ INFO ]───────────────────────────── [PAGE {page}/{total_pages}]

[1] > Info Tool 1
[2] > Info Tool 2

[N] Next Page   |   [B] Back Page   |   [Q] Quit
"""
    print(styled_left(page_content))

def settings_page(page, total_pages):
    clear()
    ascii_art = r"""

██╗  ██╗██████╗ ██╗   ██╗██████╗ ████████╗ █████╗ 
██║ ██╔╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔══██╗
█████╔╝ ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ███████║
██╔═██╗ ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██╔══██║
██║  ██╗██║  ██║   ██║   ██║        ██║   ██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   ╚═╝  ╚═╝
                                                  
"""
    page_content = rf"""{ascii_art}
─────────────────────────────[ SETTINGS ]───────────────────────────── [PAGE {page}/{total_pages}]

[1] > Settings Tool 1
[2] > Settings Tool 2

[N] Next Page   |   [B] Back Page   |   [Q] Quit
"""
    print(styled_left(page_content))

def main():
    # Global Startup: Lade den Remote-Loading-Animation Code und führe ihn aus.
    execute_loading_animation_code(LOADING_ANIMATION_CODE_URL)
    # Nach der Animation: Bildschirm leeren und Key-Prompt anzeigen.
    clear()
    if key_prompt() != REQUIRED_KEY:
        print(styled_left("Invalid key. Exiting..."))
        time.sleep(1)
        return

    # Zeige die Updates-Landing-Page
    landing_page()
    
    current_page = 1
    total_pages = 4
    pages = {
        1: discord_page,
        2: updates_page,
        3: info_page,
        4: settings_page
    }
    categories = {1: "discord", 2: "updates", 3: "info", 4: "settings"}
    
    # Starte mit der Discord-Seite als Hauptmenü
    pages[current_page](current_page, total_pages)
    
    while True:
        user_input = input(styled_left("$ ")).strip().lower()
        if user_input in {"1", "2"}:
            tool_option = user_input
            run_tool(categories[current_page], tool_option)
            pages[current_page](current_page, total_pages)
        elif user_input == "n":
            current_page = current_page + 1 if current_page < total_pages else 1
            pages[current_page](current_page, total_pages)
        elif user_input == "b":
            current_page = current_page - 1 if current_page > 1 else total_pages
            pages[current_page](current_page, total_pages)
        elif user_input == "q":
            print(styled_left("Exiting... Stay dominant."))
            time.sleep(1)
            break
        else:
            print(styled_left("Invalid input. Try again."))

if __name__ == "__main__":
    main()
