#!/usr/bin/env python3

import os
import csv
import shutil
import mysql.connector
import json
from datetime import datetime

# Config for Station 2
CSV_FOLDER = '/Users/chuck/BirdMonitor/data/unprocessed_csv_s2'
PROCESSED_CSV_FOLDER = '/Users/chuck/BirdMonitor/data/processed_csv_s2'

# Load DB credentials from JSON
with open('/Users/chuck/BirdMonitor/config/db_secrets.json') as f:
    DB_CONFIG = json.load(f)

def get_processed_files(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS imported_csvs (
            filename VARCHAR(255) PRIMARY KEY,
            imported_at DATETIME
        )
    """)
    cursor.execute("SELECT filename FROM imported_csvs")
    return {row[0] for row in cursor.fetchall()}

def extract_relative_wav_path(full_path):
    return os.path.basename(full_path)

def insert_sighting(cursor, row):
    wav_filename = extract_relative_wav_path(row["File"])
    start_time = float(row["Start (s)"])
    end_time = float(row["End (s)"])
    scientific_name = row["Scientific name"]
    species_common_name = row["Common name"]
    confidence = float(row["Confidence"])
    mic_model = "Wildtronics PIP"
    location = "S2"

    cursor.execute("""
        INSERT IGNORE INTO sightings (
            wav_filename, timestamp,
            begin_time_sec, end_time_sec,
            species_common_name, scientific_name, confidence,
            mic_model, location
        ) VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s, %s)
    """, (
        wav_filename, start_time, end_time,
        species_common_name, scientific_name, confidence,
        mic_model, location
    ))

def mark_file_as_processed(cursor, filename):
    cursor.execute(
        "INSERT INTO imported_csvs (filename, imported_at) VALUES (%s, %s)",
        (filename, datetime.now())
    )

def main():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    processed_files = get_processed_files(cursor)

    for filename in os.listdir(CSV_FOLDER):
        if not filename.endswith('.BirdNET.results.csv'):
            continue
        if filename == 'BirdNET_CombinedTable.csv':
            continue
        if filename in processed_files:
            continue

        file_path = os.path.join(CSV_FOLDER, filename)
        print(f"📥 Importing: {filename}")
        success = True

        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    insert_sighting(cursor, row)
                except Exception as e:
                    print(f"⚠️ Error inserting row: {e}")
                    success = False
                    break

        if success:
            mark_file_as_processed(cursor, filename)
            connection.commit()
            shutil.move(file_path, os.path.join(PROCESSED_CSV_FOLDER, filename))

    cursor.close()
    connection.close()
    print("✅ S2 import to main sightings table complete.")

if __name__ == '__main__':
    main()

