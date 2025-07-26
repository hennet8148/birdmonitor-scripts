#!/bin/bash

# Log start
echo "[`date`] 🌤️ Starting fetch_weather.sh" >> /Users/chuck/BirdMonitor/logs/weather.log

/opt/homebrew/bin/python3 /Users/chuck/BirdMonitor/scripts/fetch_weather_data.py >> /Users/chuck/BirdMonitor/logs/weather.log 2>&1

