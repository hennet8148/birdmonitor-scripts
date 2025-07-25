#!/bin/bash

# Log start
echo "[`date`] 🌤️ Starting fetch_weather.sh as root" >> /Users/chuck/BirdMonitor/logs/weather.log


# Run the Python script using Chuck's pyenv shim path
/usr/bin/env -i PATH="/usr/bin:/bin:/usr/sbin:/sbin:/Users/chuck/.pyenv/shims" \
  /Users/chuck/.pyenv/shims/python3 /Users/chuck/BirdMonitor/scripts/fetch_weather_data.py \
  >> /Users/chuck/BirdMonitor/logs/weather.log 2>&1

