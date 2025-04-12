import os
import subprocess
import sys
import urllib.parse
import tkinter as tk
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(r"""
████████╗██╗████████╗ █████╗ ███╗   ██╗██╗███████╗██╗   ██╗
╚══██╔══╝██║╚══██╔══╝██╔══██╗████╗  ██║██║██╔════╝╚██╗ ██╔╝
   ██║   ██║   ██║   ███████║██╔██╗ ██║██║█████╗   ╚████╔╝ 
   ██║   ██║   ██║   ██╔══██║██║╚██╗██║██║██╔══╝    ╚██╔╝  
   ██║   ██║   ██║   ██║  ██║██║ ╚████║██║███████╗   ██║   
   ╚═╝   ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝   ╚═╝   

    TITANIFY v2 – Smart Spotify Downloader
    """)

def sanitize_url(url: str) -> str:
    """
    Bereinigt den Spotify-Link:
    - Entfernt Query-Parameter
    - Entfernt regionale Zusätze wie "/intl-de/"
    """
    parsed = urllib.parse.urlparse(url)
    scheme, netloc, path = parsed.scheme, parsed.netloc, parsed.path

    # Entferne "/intl-xx" im Pfad, z. B. /intl-de/track/... → /track/...
    path_parts = path.split('/')
    cleaned_parts = [part for part in path_parts if not part.startswith("intl-") and part]
    new_path = "/" + "/".join(cleaned_parts)
    
    return urllib.parse.urlunparse((scheme, netloc, new_path, '', '', ''))

def choose_folder():
    root = tk.Tk()
    root.withdraw()  # Hauptfenster ausblenden
    folder = filedialog.askdirectory(title="Wähle den Speicherort für deine Downloads")
    root.destroy()
    return folder

def download_song(url, output_folder):
    """
    Lädt einen einzelnen Song runter.
    Wenn rate requests auftreten, wartet der Worker kurz und versucht es erneut.
    """
    clean_url = sanitize_url(url)
    print(f"\n[🎵] Downloading → {clean_url}")
    cmd = [
        sys.executable, "-m", "spotdl", "download", 
        clean_url, 
        "--bitrate", "320k",
        "--output", output_folder
    ]
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        ret = subprocess.call(cmd)
        if ret == 0:
            # Download successfull
            print(f"[✓] Download abgeschlossen für {clean_url}")
            return
        else:
            # Bei Rate-Limit oder anderen Fehlern, warte eine Weile
            wait_time = 10 * attempt
            print(f"[!] Fehler bei {clean_url}. Versuch {attempt}/{max_retries}. Warte {wait_time} Sekunden...")
            time.sleep(wait_time)
    print(f"[✗] Download für {clean_url} schlug fehl nach {max_retries} Versuchen.")

def download_from_file(file_path, output_folder):
    tasks = []
    try:
        with open(file_path, 'r') as file:
            links = file.readlines()
        # Konkurrierendes Herunterladen – passe max_workers nach Bedarf an
        with ThreadPoolExecutor(max_workers=4) as executor:
            for link in links:
                link = link.strip()
                if link:
                    tasks.append(executor.submit(download_song, link, output_folder))
            # Warte, bis alle Downloads abgeschlossen sind und gib eventuelle Exceptions aus
            for future in as_completed(tasks):
                try:
                    future.result()
                except Exception as e:
                    print(f"[!] Exception: {e}")
    except FileNotFoundError:
        print(f"[!] File '{file_path}' not found.")

if __name__ == "__main__":
    clear()
    banner()
    
    # Wähle den Speicherort
    output_folder = choose_folder()
    if not output_folder:
        print("[!] Kein Speicherort ausgewählt – Abbruch.")
        sys.exit(1)
    
    print("\n[1] Einzelner Spotify-Link eingeben")
    print("[2] Link-Liste aus Datei laden (ein Link pro Zeile)\n")
    mode = input("[>] Auswahl (1/2): ").strip()

    if mode == "1":
        link = input("\n[>] Gib den Spotify-Link ein: ").strip()
        download_song(link, output_folder)
    elif mode == "2":
        file_path = input("\n[>] Pfad zur Datei mit Links: ").strip()
        download_from_file(file_path, output_folder)
    else:
        print("\n[!] Ungültige Auswahl – Restart.")
