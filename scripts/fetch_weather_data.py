import requests
import mysql.connector
import json
from datetime import datetime
import warnings
from urllib3.exceptions import NotOpenSSLWarning

# Suppress warning about LibreSSL vs OpenSSL on macOS system Python
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

# Load DB credentials from external JSON file
with open('/Users/chuck/BirdMonitor/config/db_secrets.json') as f:
    DB_CONFIG = json.load(f)

# Helper to safely convert values to float, stripping units
def safe_float(val):
    if isinstance(val, str):
        val = val.replace('%', '').replace('inHg', '').replace('in', '').replace('mph', '').replace('W/m2', '').strip()
    try:
        return float(val)
    except:
        return 0.0

# Helper to find a value by ID in a list of dicts
def get_val(source, target_id):
    for item in source:
        if item.get('id') == target_id:
            return safe_float(item.get('val'))
    return 0.0

# Fetch live JSON data from the weather station
try:
    response = requests.get("http://192.168.5.165/get_livedata_info", timeout=10)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    print("Error fetching data:", e)
    exit(1)

# Parse fields
common = data.get('common_list', [])
rain = data.get('piezoRain', [])
wh25 = data.get('wh25', [{}])[0]
lightning = data.get('lightning', [{}])[0]

# Safely parse lightning timestamp
try:
    lightning_last_strike = datetime.strptime(lightning.get('timestamp', ''), "%m/%d/%Y %H:%M:%S")
except:
    lightning_last_strike = None

weather_entry = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'temperature_f': get_val(common, '0x02'),
    'humidity_percent': get_val(common, '0x07'),
    'dew_point_f': get_val(common, '0x03'),
    'wind_speed_mph': get_val(common, '0x19'),
    'wind_gust_mph': get_val(common, '0x0C'),
    'day_wind_max_mph': 0.0,  # Optional for now
    'solar_radiation_wm2': get_val(common, '0x15'),
    'uv_index': get_val(common, '0x17'),
    'barometric_pressure_inhg': safe_float(wh25.get('abs', '0.0')),
    'rain_event_in': get_val(rain, '0x0D'),
    'rain_rate_in_hr': get_val(rain, '0x0E'),
    'rain_day_in': get_val(rain, '0x10'),
    'rain_week_in': get_val(rain, '0x11'),
    'rain_month_in': get_val(rain, '0x12'),
    'rain_year_in': get_val(rain, '0x13'),
    'piezo_battery': int(rain[-1].get('battery', 0)),
    'lightning_strike_count': int(lightning.get('count', 0)),
    'lightning_distance_mi': safe_float(lightning.get('distance', '0.0')),
    'lightning_last_strike': lightning_last_strike.strftime('%Y-%m-%d %H:%M:%S') if lightning_last_strike else None,
    'lightning_battery': int(lightning.get('battery', 0))
}

# Insert into database with confirmation logging
try:
    print("ℹ️ Connecting to database...")
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    print("ℹ️ Attempting insert at", weather_entry['timestamp'])
    cursor.execute("""
        INSERT INTO weather_readings (
            timestamp, temperature_f, humidity_percent, dew_point_f,
            wind_speed_mph, wind_gust_mph, day_wind_max_mph,
            solar_radiation_wm2, uv_index, barometric_pressure_inhg,
            rain_event_in, rain_rate_in_hr, rain_day_in, rain_week_in,
            rain_month_in, rain_year_in, piezo_battery,
            lightning_strike_count, lightning_distance_mi,
            lightning_last_strike, lightning_battery
        ) VALUES (
            %(timestamp)s, %(temperature_f)s, %(humidity_percent)s, %(dew_point_f)s,
            %(wind_speed_mph)s, %(wind_gust_mph)s, %(day_wind_max_mph)s,
            %(solar_radiation_wm2)s, %(uv_index)s, %(barometric_pressure_inhg)s,
            %(rain_event_in)s, %(rain_rate_in_hr)s, %(rain_day_in)s, %(rain_week_in)s,
            %(rain_month_in)s, %(rain_year_in)s, %(piezo_battery)s,
            %(lightning_strike_count)s, %(lightning_distance_mi)s,
            %(lightning_last_strike)s, %(lightning_battery)s
        )
    """, weather_entry)

    conn.commit()

    # Double check if row was written
    cursor.execute("SELECT MAX(timestamp) FROM weather_readings")
    last_inserted = cursor.fetchone()[0]
    print("🧾 Last row in DB:", last_inserted)

    if str(last_inserted) == weather_entry['timestamp']:
        print("✅ Successfully inserted at", weather_entry['timestamp'])
    else:
        print("⚠️ Timestamp mismatch. Expected:", weather_entry['timestamp'], " but found:", last_inserted)

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ INSERT FAILED:", e)
    print("⚠️ Failed entry was:", weather_entry)

