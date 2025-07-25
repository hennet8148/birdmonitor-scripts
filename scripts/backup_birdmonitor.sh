#!/bin/bash

# Directories to back up
SOURCE_CSV="/Users/chuck/BirdMonitor/data/processed_csv"
SOURCE_WAV="/Users/chuck/BirdMonitor/data/processed_wav"
SOURCE_CSV_S2="/Users/chuck/BirdMonitor/data/processed_csv_s2"
SOURCE_WAV_S2="/Users/chuck/BirdMonitor/data/processed_wav_s2"

# Backup destinations
DEST1="/Volumes/ShopOne/BirdMonitor"
DEST2="/Volumes/ShopTwo/BirdMonitor"

DEST1_CSV="$DEST1/processed_csv"
DEST1_WAV="$DEST1/processed_wav"
DEST1_CSV_S2="$DEST1/processed_csv_s2"
DEST1_WAV_S2="$DEST1/processed_wav_s2"

DEST2_CSV="$DEST2/processed_csv"
DEST2_WAV="$DEST2/processed_wav"
DEST2_CSV_S2="$DEST2/processed_csv_s2"
DEST2_WAV_S2="$DEST2/processed_wav_s2"

# Check if both volumes are mounted
if [ ! -d "$DEST1" ] || [ ! -d "$DEST2" ]; then
  echo "$(date): One or both backup volumes are not mounted. Exiting."
  exit 1
fi

# Create destination dirs if they don’t exist
mkdir -p "$DEST1_CSV" "$DEST1_WAV" "$DEST1_CSV_S2" "$DEST1_WAV_S2"
mkdir -p "$DEST2_CSV" "$DEST2_WAV" "$DEST2_CSV_S2" "$DEST2_WAV_S2"

# Sync processed_csv
rsync -av --ignore-existing "$SOURCE_CSV/" "$DEST1_CSV/"
RSYNC1_CSV=$?
rsync -av --ignore-existing "$SOURCE_CSV/" "$DEST2_CSV/"
RSYNC2_CSV=$?

# Sync processed_wav
rsync -av --ignore-existing "$SOURCE_WAV/" "$DEST1_WAV/"
RSYNC1_WAV=$?
rsync -av --ignore-existing "$SOURCE_WAV/" "$DEST2_WAV/"
RSYNC2_WAV=$?

# Sync processed_csv_s2
rsync -av --ignore-existing "$SOURCE_CSV_S2/" "$DEST1_CSV_S2/"
RSYNC1_CSV_S2=$?
rsync -av --ignore-existing "$SOURCE_CSV_S2/" "$DEST2_CSV_S2/"
RSYNC2_CSV_S2=$?

# Sync processed_wav_s2
rsync -av --ignore-existing "$SOURCE_WAV_S2/" "$DEST1_WAV_S2/"
RSYNC1_WAV_S2=$?
rsync -av --ignore-existing "$SOURCE_WAV_S2/" "$DEST2_WAV_S2/"
RSYNC2_WAV_S2=$?

# Confirm success
if [[ $RSYNC1_CSV -eq 0 && $RSYNC2_CSV -eq 0 && \
      $RSYNC1_WAV -eq 0 && $RSYNC2_WAV -eq 0 && \
      $RSYNC1_CSV_S2 -eq 0 && $RSYNC2_CSV_S2 -eq 0 && \
      $RSYNC1_WAV_S2 -eq 0 && $RSYNC2_WAV_S2 -eq 0 ]]; then
  echo "$(date): Backup completed successfully to both destinations."
else
  echo "$(date): WARNING — One or more backup operations failed."
fi

