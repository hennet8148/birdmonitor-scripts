#!/usr/bin/env python3

import subprocess
import os
from datetime import datetime

# Static IP of the Pi
REMOTE_HOST = "192.168.4.99"
REMOTE_USER = "raspberry"
SSH_KEY_PATH = os.path.expanduser("~/.ssh/id_birdpi")
REMOTE_PATH = "/home/raspberry/recordings/"
LOCAL_DEST = os.path.expanduser("/Users/chuck/BirdMonitor/data/unprocessed")

# Ensure the destination folder exists
os.makedirs(LOCAL_DEST, exist_ok=True)

rsync_cmd = [
    "rsync",
    "-av",
    "-e", f"ssh -i {SSH_KEY_PATH}",
    "--remove-source-files",
    f"{REMOTE_USER}@{REMOTE_HOST}:{REMOTE_PATH}",
    LOCAL_DEST
]

def run_sync():
    try:
        print(f"[{datetime.now()}] 🔄 Syncing from {REMOTE_HOST}...")
        subprocess.run(rsync_cmd, check=True)
        print("✅ Sync successful.")
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now()}] ❌ Rsync failed: {e}")

if __name__ == "__main__":
    run_sync()

