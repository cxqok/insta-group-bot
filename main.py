import os
import sys
import subprocess
import time

# --- Auto install pip, upgrade pip, install required modules ---
def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    except:
        pass
    modules = ["instagrapi", "rich"]
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])

install_requirements()

from instagrapi import Client
from rich import print

# --- Instagram credentials ---
USERNAME = "cxqo2"
PASSWORD = "pillow1234"

# --- Connect Instagram client ---
cl = Client()
cl.login(USERNAME, PASSWORD)

# --- Auto Fetch Groups ---
def fetch_groups():
    print("[bold green]Fetching Groups...[/bold green]")
    threads = cl.direct_threads(amount=50)
    groups = []
    for thread in threads:
        if len(thread.users) > 2:  # Group = more than 2 users
            groups.append(thread)
    return groups

groups = fetch_groups()

print(f"[bold cyan]Found {len(groups)} groups.[/bold cyan]")

# --- Custom Message ---
custom_message = "oye message mat kar warna pakistaan ko pani nhi dunga 😎😂"

# --- Listen to New Messages ---
def auto_reply():
    while True:
        try:
            new_groups = fetch_groups()  # Always update groups
            for group in new_groups:
                messages = cl.direct_messages(group.id, amount=10)
                for msg in messages:
                    if not msg.user_id == cl.user_id:
                        username = cl.user_info(msg.user_id).username
                        reply_text = f"@{username} {custom_message}"
                        cl.direct_send(reply_text, thread_ids=[group.id])
                        print(f"[bold yellow]Replied to @{username}[/bold yellow]")
                        time.sleep(2)
            time.sleep(15)
        except Exception as e:
            print(f"[bold red]Error: {e}[/bold red]")
            time.sleep(10)

auto_reply()
