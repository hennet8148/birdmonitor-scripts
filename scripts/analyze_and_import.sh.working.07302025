#!/bin/bash

# Load zsh environment
source ~/.zprofile

# Properly initialize pyenv for non-interactive shells
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$($PYENV_ROOT/bin/pyenv init --path)"
eval "$($PYENV_ROOT/bin/pyenv init -)"

# Log start
echo "[`date`] 🚀 Starting analyze_and_import.sh" >> /Users/chuck/BirdMonitor/logs/analyze.log

# Log current user and working directory
echo "User: $(whoami)" >> /Users/chuck/BirdMonitor/logs/analyze.log
echo "PWD before cd: $(pwd)" >> /Users/chuck/BirdMonitor/logs/analyze.log

# Ensure we’re in the scripts directory
cd /Users/chuck/BirdMonitor/scripts || {
  echo "❌ Failed to cd into script dir" >> /Users/chuck/BirdMonitor/logs/analyze.log
  exit 1
}
echo "PWD after cd: $(pwd)" >> /Users/chuck/BirdMonitor/logs/analyze.log

# Log current input files
echo "📂 Files in unprocessed_csv before import:" >> /Users/chuck/BirdMonitor/logs/analyze.log
ls -lh /Users/chuck/BirdMonitor/data/unprocessed_csv >> /Users/chuck/BirdMonitor/logs/analyze.log

# Run analysis
echo "[`date`] 📊 Running analyze_wavs.py..." >> /Users/chuck/BirdMonitor/logs/analyze.log
python3 analyze_wavs.py >> /Users/chuck/BirdMonitor/logs/analyze.log 2>&1

# If successful, import results
if [ $? -eq 0 ]; then
    echo "[`date`] 📥 Running import_csv_to_db.py..." >> /Users/chuck/BirdMonitor/logs/analyze.log
   /Users/chuck/.pyenv/versions/3.11.8/bin/python3 import_csv_to_db.py >> /Users/chuck/BirdMonitor/logs/import.log 2>&1
else
    echo "[`date`] ❌ Skipping import due to analyzer failure." >> /Users/chuck/BirdMonitor/logs/analyze.log
fi

# Final log
echo "[`date`] ✅ Wrapper script finished." >> /Users/chuck/BirdMonitor/logs/analyze.log

# Final step: monitor file flow (after sync + import)
echo "[`date`] 🔎 Running monitor_file_flow.py..." >> /Users/chuck/BirdMonitor/logs/analyze.log
python3 /Users/chuck/BirdMonitor/scripts/monitor_file_flow.py >> /Users/chuck/BirdMonitor/logs/monitor.log 2>&1

