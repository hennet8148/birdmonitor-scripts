#!/usr/bin/env python3

import subprocess
import os
import shutil
from datetime import datetime

# Paths
BIRDNET_DIR = "/Users/chuck/BirdNET-Analyzer"
INPUT_DIR = "/Users/chuck/BirdMonitor/data/unprocessed"
OUTPUT_DIR = "/Users/chuck/BirdMonitor/data/unprocessed_csv"
PROCESSED_WAV_DIR = "/Users/chuck/BirdMonitor/data/processed_wav"

# Settings
LAT = "41.0"
LON = "-75.0"
WEEK = "25"  # TODO: Externalize or auto-calculate this later
MIN_CONF = "0.1"
SENSITIVITY = "1.0"

def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}", flush=True)

def move_wavs_with_results():
    log("📂 Moving processed .wav files...")
    for filename in os.listdir(INPUT_DIR):
        if not filename.endswith(".wav"):
            continue

        base = os.path.splitext(filename)[0]
        expected_csv = f"{base}.BirdNET.results.csv"
        expected_csv_path = os.path.join(OUTPUT_DIR, expected_csv)

        if os.path.exists(expected_csv_path):
            src_wav = os.path.join(INPUT_DIR, filename)
            dst_wav = os.path.join(PROCESSED_WAV_DIR, filename)
            shutil.move(src_wav, dst_wav)
            log(f"✅ Moved: {filename}")
        else:
            log(f"⚠️ Skipping (no result): {filename}")

def main():
    log("📊 Starting batch BirdNET analysis...")

    cmd = [
        "python3", "-m", "birdnet_analyzer.analyze", INPUT_DIR,
        "-o", OUTPUT_DIR,
        "--lat", LAT,
        "--lon", LON,
        "--week", WEEK,
        "--min_conf", MIN_CONF,
        "--sensitivity", SENSITIVITY,
        "--rtype", "csv",
        "--combine_results",
        "--overlap", "0.7"
    ]

    try:
        subprocess.run(cmd, cwd=BIRDNET_DIR, check=True)
        log("✅ Batch analysis complete.")
        move_wavs_with_results()
    except subprocess.CalledProcessError as e:
        log(f"❌ Error during analysis: {e}")

if __name__ == "__main__":
    main()

