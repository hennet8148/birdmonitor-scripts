#!/bin/bash

# Set up environment
export HOME="/Users/chuck"
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin"

# Log start
echo "[`date`] 🌤️ Starting fetch_weather.sh" >> /Users/chuck/BirdMonitor/logs/weather.log

# Run the weather fetch script with Python 3.11
/usr/local/bin/python3 /Users/chuck/BirdMonitor/scripts/fetch_weather_data.py >> /Users/chuck/BirdMonitor/logs/weather.log 2>&1

