import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime
import pytz

# Setup request caching and retries
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Define locations (ID, Latitude, Longitude)
locations = [
    (0, 32.724075, -117.14286),  
    (1, 32.864674, -114.895966),
    (2, 33.07557, -116.646194),
    (3, 33.848858, -116.56289),
    (4, 34.059753, -118.125),
    (5, 36.801403, -119.802895),
    (6, 37.785587, -122.409645),
    (7, 38.558872, -121.54891),
    (8, 39.191563, -120.20633),
    (9, 39.753952, -121.79416),
    (10, 41.300526, -122.281204),
    (11, 41.722317, -124.2547)
]

# API Request Parameters
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": [lat for _, lat, _ in locations],
    "longitude": [lon for _, _, lon in locations],
    "current": [
        "temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day",
        "precipitation", "rain", "showers", "snowfall", "weather_code",
        "cloud_cover", "pressure_msl", "surface_pressure",
        "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"
    ],
    "timezone": "America/Los_Angeles"
}

# Fetch data from Open-Meteo
responses = openmeteo.weather_api(url, params=params)

# Process responses for each location
weather_data = []
pacific_tz = pytz.timezone("America/Los_Angeles")

for i, response in enumerate(responses):
    location_id, _, _ = locations[i]
    
    # Extract current weather data
    current_weather = response.Current()  # Use OpenMeteo SDK method
    timestamp = current_weather.Time()  # This is a Unix timestamp (int)
    
    # Convert Unix timestamp to Pacific Time
    dt_object = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    dt_pacific = dt_object.astimezone(pacific_tz)
    formatted_time = dt_pacific.strftime("%Y-%m-%d %H:%M:%S %Z")  # Readable format

    # Append weather data to list
    weather_data.append({
        "location_id": location_id,
        "time": formatted_time,
        "temperature_2m": current_weather.Variables(0).Value(), #C
        "relative_humidity_2m": current_weather.Variables(1).Value(),#%
        "apparent_temperature": current_weather.Variables(2).Value(), #C
        "is_day": current_weather.Variables(3).Value(),
        "precipitation": current_weather.Variables(4).Value(), #mm
        "rain": current_weather.Variables(5).Value(), #mm
        "showers": current_weather.Variables(6).Value(), #mm
        "snowfall": current_weather.Variables(7).Value(), #cm
        "weather_code": current_weather.Variables(8).Value(), #wmo code
        "cloud_cover": current_weather.Variables(9).Value(), #%
        "pressure_msl": current_weather.Variables(10).Value(), #hPa
        "surface_pressure": current_weather.Variables(11).Value(), #hPa
        "wind_speed_10m": current_weather.Variables(12).Value(), #km/h
        "wind_direction_10m": current_weather.Variables(13).Value(), #°
        "wind_gusts_10m": current_weather.Variables(14).Value(), #km/h
    })

    # Debugging output
    print(f"Location ID: {location_id}, Time: {formatted_time}")
    print(f"Temperature: {current_weather.Variables(0).Value()}°C, Humidity: {current_weather.Variables(1).Value()}%")
    print(f"Wind Speed: {current_weather.Variables(12).Value()} km/h, Wind Direction: {current_weather.Variables(13).Value()}°")
    print("---")

# Convert list to DataFrame
weather_df = pd.DataFrame(weather_data)

# Save latest weather data (overwrite)
weather_df.to_csv("current_weather_data.csv", index=False)
print("\nCurrent weather data saved to 'current_weather_data.csv'.")

# # Append to historical weather data (if exists, append; else create)
# historical_file = "historical_weather_data.csv"
# try:
#     existing_df = pd.read_csv(historical_file)
#     updated_df = pd.concat([existing_df, weather_df], ignore_index=True)
#     updated_df.to_csv(historical_file, index=False)
# except FileNotFoundError:
#     weather_df.to_csv(historical_file, index=False)
