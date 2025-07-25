#!/bin/bash


# Log start
echo "[`date`] 🌤️ Starting fetch_weather.sh" >> /Users/chuck/BirdMonitor/logs/weather.log
# Suppress NotOpenSSLWarning globally
PYTHONWARNINGS="ignore::NotOpenSSLWarning"

# Run the weather data fetch script using system Python
/usr/local/bin/python3 /Users/chuck/BirdMonitor/scripts/fetch_weather_data.py >> /Users/chuck/BirdMonitor/logs/weather.log 2>&1


