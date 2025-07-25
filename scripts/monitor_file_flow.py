#!/usr/bin/env python3

import os
import time
import subprocess
import sys
from datetime import datetime

# === Configuration ===
WATCH_DIR = "/Users/chuck/BirdMonitor/data/unprocessed"
TIME_WINDOW_MINUTES = 10  # Set to 10 when you're ready
PHONE_NUMBER = "5708565105"  # AT&T number
SYNC_SCRIPT = "/Users/chuck/BirdMonitor/scripts/sync_recordings.py"

# === Run sync_recordings.py first ===
def run_sync():
    try:
        print(f"[{datetime.now()}] 🔄 Running sync_recordings.py...")
        subprocess.run([sys.executable, SYNC_SCRIPT], check=True)
        print(f"[{datetime.now()}] ✅ Sync complete.")
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now()}] ❌ Sync failed: {e}")

# === Check latest .wav file ===
def latest_wav_time(path):
    wav_files = [
        os.path.join(path, f) for f in os.listdir(path)
        if f.lower().endswith(".wav")
    ]
    if not wav_files:
        return None
    return max(os.path.getmtime(f) for f in wav_files)

# === Send alert via iMessage ===
def send_text_via_messages(phone_number, message_text):
    apple_script = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = SMS
        set targetBuddy to buddy "{phone_number}" of targetService
        send "{message_text}" to targetBuddy
    end tell
    '''
    subprocess.run(["osascript", "-e", apple_script])

def send_text_alert():
    message = f"⚠️ No new .wav files in the last {TIME_WINDOW_MINUTES} minutes."
    print(f"[{datetime.now()}] 📡 Sending alert: {message}")
    send_text_via_messages(PHONE_NUMBER, message)

# === Main workflow ===
def main():
    run_sync()

    now = time.time()
    threshold = now - (TIME_WINDOW_MINUTES * 60)
    last_seen = latest_wav_time(WATCH_DIR)

    if last_seen is None or last_seen < threshold:
        send_text_alert()
    else:
        print(f"[{datetime.now()}] ✅ Last file seen at {datetime.fromtimestamp(last_seen)}")

if __name__ == "__main__":
    main()

