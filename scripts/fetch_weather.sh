#!/bin/bash

set +x
export HOME="/Users/chuck"
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin"
export PYTHONPATH="/Users/chuck/Library/Python/3.13/lib/python/site-packages"

# Log start
echo "[`date`] 🌤️ Starting fetch_weather.sh" >> /Users/chuck/BirdMonitor/logs/weather.log

/opt/homebrew/bin/python3 /Users/chuck/BirdMonitor/scripts/fetch_weather_data.py >> /Users/chuck/BirdMonitor/logs/weather.log 2>&1

