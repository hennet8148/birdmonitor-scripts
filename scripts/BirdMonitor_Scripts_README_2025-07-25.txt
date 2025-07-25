BirdMonitor Scripts – Davidson Farm Bird Project
================================================

This folder contains all currently active and essential scripts used in the operation of the BirdMonitor audio processing and MySQL data ingestion pipeline.

Last updated: July 25, 2025

────────────────────────────────────────────
Core Workflow
────────────────────────────────────────────

Station 1:
----------
- sync_recordings.py  
  Rsyncs 30-second .wav files from the Raspberry Pi (Station 1) to the Mac.

- analyze_wavs.py  
  Runs BirdNET-Analyzer on unprocessed WAVs and generates result CSVs.

- import_csv_to_db.py  
  Imports detection data from CSVs into the MySQL `sightings` table.

- analyze_and_import.sh  
  Wraps the three steps above into a single pipeline. Cron target (every 5 min).

Station 2:
----------
- sync_recordings_s2.py  
  Rsyncs WAVs from Station 2 Pi to the Mac.

- analyze_wavs_s2.py  
  Runs BirdNET-Analyzer on S2 files.

- import_csv_to_db_s2.py  
  Imports S2 CSVs into MySQL (adds location = 'S2').

- analyze_and_import_s2.sh  
  Wraps the full S2 pipeline. Cron target (every 5 min).

Weather:
--------
- fetch_weather.sh  
  Calls fetch_weather_data.py.

- fetch_weather_data.py  
  Pulls JSON data from local WittBoy weather station, inserts into `weather_readings` table.

────────────────────────────────────────────
Maintenance Scripts
────────────────────────────────────────────

- monitor_file_flow.py and monitor_file_flow_s2.py  
  Monitor activity and log if no new files are seen. Useful for system health monitoring.

- backup_birdmonitor.sh  
  Archives all critical data (CSV, WAV, MySQL dumps, logs) to external USB drives.

- gentle_compare_backup_hashes.py  
  Compares backup volumes (ShopOne vs ShopTwo) by SHA1 without stressing the drives.

- safe_to_delete_*.txt  
  Lists of files that are safe to delete after successful import and backup.

- delete_safe_files.py  
  Parses the .txt lists and safely deletes WAVs and CSVs.

- delete_safe_files.sh  
  Calls the Python deletion script. Optional use.

- run_backup_and_cleanup.sh  
  Cron target (e.g., 08:42 + 15 min interval). Runs backup and cleanup routines.

────────────────────────────────────────────
Configuration and Secrets
────────────────────────────────────────────

- config/db_secrets.json  
  Stores MySQL connection info in structured JSON format.

  Example format:
  {
    "host": "45.55.56.67",
    "user": "birdnet_user",
    "password": "YOUR_PASSWORD_HERE",
    "database": "birdnet_db"
  }

  This file is .gitignore'd and should never be committed.

────────────────────────────────────────────
How to set up SSH key access from Pi
────────────────────────────────────────────

On the Pi:
  ssh-keygen -t ed25519
  ssh-copy-id -i ~/.ssh/id_ed25519.pub chuck@your-mac-ip

Ensure REMOTE_HOST, REMOTE_USER, and SSH_KEY_PATH are configured correctly in the sync_recordings*.py scripts.

────────────────────────────────────────────
Git Usage Notes
────────────────────────────────────────────

- This scripts/ directory can either be its own repo or added to the bird-dashboard repo.
- All archived/deprecated scripts have been moved to:
  /Users/chuck/Documents/BirdMonitorArchive_2025-07-25/
- Before pushing to GitHub, confirm all sensitive values are moved to db_secrets.json.

────────────────────────────────────────────

This system is a data-driven soundscape observatory, not a simple bird list. The goal is to uncover patterns of presence through signal processing, detection modeling, and ambient data collection.

Stay curious. 🐦

