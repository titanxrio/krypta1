import requests, os, time
from datetime import datetime
from tkinter import filedialog, Tk
from colorama import Fore, Style, init

# Initialize colorama for styled Terminal Output
init(autoreset=True)

# Farben (Blau-Lila Flair)
TIME_COLOR = Fore.LIGHTBLUE_EX
VALID_COLOR = Fore.LIGHTGREEN_EX
INVALID_COLOR = Fore.LIGHTRED_EX
UNKNOWN_COLOR = Fore.LIGHTYELLOW_EX
BANNER_COLOR = Fore.LIGHTMAGENTA_EX

def get_time():
    return f"{TIME_COLOR}[{time.strftime('%H:%M:%S')}]"

def censor_token(token):
    # Ersetzt die letzten 10 Zeichen mit '*'
    if len(token) > 10:
        return token[:-10] + "*" * 10
    return "*" * len(token)

def pick_file(title="Select a file"):
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=title)
    root.destroy()
    return file_path

def read_tokens(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def read_proxies(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def check_token(token, proxy=None):
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    proxies = {"http": proxy, "https": proxy} if proxy else None
    try:
        r = requests.get("https://discord.com/api/v9/users/@me", headers=headers, proxies=proxies, timeout=10)
        return r.status_code == 200
    except Exception:
        return None

def save_valid_tokens(valid_tokens):
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    output_file = os.path.join(downloads_path, "valid_tokens.txt")
    with open(output_file, "w") as f:
        for token in valid_tokens:
            f.write(censor_token(token) + "\n")
    print(f"\n{Fore.CYAN}[✓] Valid tokens saved to: {output_file}")

def run_checker():
    print(BANNER_COLOR + "\n=== TITAN TOKEN CHECKER V2 ===\n")
    print("1 - Check single token")
    print("2 - Check tokens from file")
    mode = input("\nChoose mode: ").strip()
    
    # Zuerst abfragen, ob Proxies genutzt werden sollen
    use_proxies = input("\nUse proxies? (y/n): ").strip().lower() == "y"
    proxies = []
    if use_proxies:
        print("\n[~] Please select your proxies file")
        proxy_file = pick_file("Select proxy list")
        if proxy_file:
            proxies = read_proxies(proxy_file)
            print(f"{Fore.CYAN}[~] Loaded {len(proxies)} proxies from file.")
        else:
            print(f"{Fore.YELLOW}[~] No proxies file selected. Proceeding without proxies.")
    
    if mode == "1":
        token = input("\nEnter token: ").strip()
        proxy = proxies[0] if proxies else None
        result = check_token(token, proxy)
        if result:
            print(f"{get_time()} > {VALID_COLOR}[VALID] {censor_token(token)}")
        elif result is False:
            print(f"{get_time()} > {INVALID_COLOR}[INVALID] {censor_token(token)}")
        else:
            print(f"{get_time()} > {UNKNOWN_COLOR}[UNKNOWN] {censor_token(token)}")

    elif mode == "2":
        print("\n[~] Please select your token list file")
        token_file = pick_file("Select token list")
        if not token_file:
            print(f"{Fore.RED}[!] No token file selected. Exiting.")
            return

        tokens = read_tokens(token_file)
        valid_tokens = []
        print(f"\n{Fore.CYAN}[~] Processing {len(tokens)} tokens...\n")
        for i, token in enumerate(tokens):
            proxy = proxies[i % len(proxies)] if proxies else None
            result = check_token(token, proxy)
            if result:
                print(f"{get_time()} > {VALID_COLOR}[VALID] {censor_token(token)}")
                valid_tokens.append(token)
            elif result is False:
                print(f"{get_time()} > {INVALID_COLOR}[INVALID] {censor_token(token)}")
            else:
                print(f"{get_time()} > {UNKNOWN_COLOR}[UNKNOWN] {censor_token(token)}")
                
        if valid_tokens:
            print(f"\n{VALID_COLOR}[✓] Valid Tokens Found: {len(valid_tokens)}")
            for token in valid_tokens:
                print(f"{Fore.CYAN}- {censor_token(token)}")
            save_valid_tokens(valid_tokens)
        else:
            print(f"\n{INVALID_COLOR}[x] No valid tokens found.")

    else:
        print(Fore.RED + "[!] Invalid mode selected.")

if __name__ == "__main__":
    run_checker()
