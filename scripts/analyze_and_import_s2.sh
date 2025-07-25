#!/bin/bash

# Load environment
source ~/.zprofile
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$($PYENV_ROOT/bin/pyenv init --path)"
eval "$($PYENV_ROOT/bin/pyenv init -)"

LOGDIR=/Users/chuck/BirdMonitor/logs
echo "[`date`] 🚀 Starting analyze_and_import_s2.sh" >> $LOGDIR/analyze_s2.log

cd /Users/chuck/BirdMonitor/scripts || {
  echo "❌ Failed to cd into script dir" >> $LOGDIR/analyze_s2.log
  exit 1
}

echo "📂 Files in unprocessed_csv_s2 before import:" >> $LOGDIR/analyze_s2.log
ls -lh /Users/chuck/BirdMonitor/data/unprocessed_csv_s2 >> $LOGDIR/analyze_s2.log

echo "[`date`] 📊 Running analyze_wavs_s2.py..." >> $LOGDIR/analyze_s2.log
python3 analyze_wavs_s2.py >> $LOGDIR/analyze_s2.log 2>&1

if [ $? -eq 0 ]; then
    echo "[`date`] 📥 Running import_csv_to_db_s2.py..." >> $LOGDIR/analyze_s2.log
    /Users/chuck/.pyenv/versions/3.11.8/bin/python3 import_csv_to_db_s2.py >> $LOGDIR/import_s2.log 2>&1
else
    echo "[`date`] ❌ Skipping import due to analyzer failure." >> $LOGDIR/analyze_s2.log
fi

echo "[`date`] ✅ Wrapper script finished." >> $LOGDIR/analyze_s2.log

echo "[`date`] 🔎 Running monitor_file_flow_s2.py..." >> $LOGDIR/analyze_s2.log
#python3 monitor_file_flow_s2.py >> $LOGDIR/monitor_s2.log 2>&1

