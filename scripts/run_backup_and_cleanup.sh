#!/bin/bash

LOGFILE="/Users/chuck/BirdMonitor/logs/backup_and_cleanup.log"
echo "🕒 [`date`] Starting full backup + cleanup run" >> "$LOGFILE"

/Users/chuck/BirdMonitor/scripts/backup_birdmonitor.sh >> "$LOGFILE" 2>&1

# Only run deletion step if backup succeeded
if [ $? -eq 0 ]; then
  echo "📦 Backup successful, proceeding to compare + delete" >> "$LOGFILE"
  /Users/chuck/.pyenv/shims/python3 /Users/chuck/BirdMonitor/scripts/gentle_compare_backup_hashes.py >> "$LOGFILE" 2>&1
  /Users/chuck/BirdMonitor/scripts/delete_safe_files.sh >> "$LOGFILE" 2>&1
else
  echo "❌ Backup failed — skipping deletion" >> "$LOGFILE"
fi

echo "✅ [`date`] Full backup + cleanup complete" >> "$LOGFILE"
echo "----------------------------------------" >> "$LOGFILE"

