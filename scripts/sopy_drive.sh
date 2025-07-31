#!/bin/bash

SOURCE="/Volumes/ShopTwo"
DEST="/Volumes/ShopOne"
LOG="/Users/chuck/BirdMonitor/logs/backup_shoptwo_to_shopone.log"

# Make sure both drives are mounted
if [ -d "$SOURCE" ] && [ -d "$DEST" ]; then
  echo "[`date`] 🟢 Starting full backup from ShopTwo to ShopOne" >> "$LOG"

  rsync -avh \
    --exclude ".DocumentRevisions-V100/" \
    --exclude ".TemporaryItems/" \
    --exclude ".fseventsd/" \
    --exclude ".Spotlight-V100/" \
    --exclude ".Trashes/" \
    --exclude ".DS_Store" \
    --filter='-!r .' \
    --out-format='%t %n' \
    "$SOURCE/" "$DEST/" >> "$LOG" 2>&1

  echo "[`date`] ✅ Backup complete" >> "$LOG"
else
  echo "[`date`] ❌ One or both volumes are not mounted!" >> "$LOG"
fi

