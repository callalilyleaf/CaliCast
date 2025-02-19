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

today_date = datetime.utcnow().strftime('%Y-%m-%d')

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": [lat for _, lat, _ in locations],
    "longitude": [lon for _, _, lon in locations],
    "hourly": [
        "temperature_2m", "relative_humidity_2m", "dew_point_2m",
        "apparent_temperature", "precipitation_probability", "precipitation",
        "rain", "snowfall", "snow_depth", "weather_code", "pressure_msl", 
        "surface_pressure", "cloud_cover", "cloud_cover_low", "cloud_cover_mid",
        "cloud_cover_high", "wind_speed_10m", "wind_speed_80m", "wind_speed_120m",
        "wind_direction_10m", "wind_direction_80m", "wind_direction_120m",
        "wind_gusts_10m", "is_day", "sunshine_duration", "wet_bulb_temperature_2m",
        "boundary_layer_height", "shortwave_radiation"
    ],
    "timezone": "America/Los_Angeles",
    "start_date": today_date,
    "end_date": today_date  
}

# Fetch data from Open-Meteo
responses = openmeteo.weather_api(url, params=params)

# Pacific timezone
pacific_tz = pytz.timezone("America/Los_Angeles")

# Process responses for each location
all_weather_data = []

for i, response in enumerate(responses):
    print(f"Processing data for Location {i}: {response.Latitude()}°N, {response.Longitude()}°E")

    hourly = response.Hourly()
    
    # Convert timestamps to readable format
    time_series = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ).tz_convert(pacific_tz)

    # Extract variables in correct order
    hourly_data = {
        "location_id": i,
        "time": time_series,
        "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
        "relative_humidity_2m": hourly.Variables(1).ValuesAsNumpy(),
        "dew_point_2m": hourly.Variables(2).ValuesAsNumpy(),
        "apparent_temperature": hourly.Variables(3).ValuesAsNumpy(),
        "precipitation_probability": hourly.Variables(4).ValuesAsNumpy(),
        "precipitation": hourly.Variables(5).ValuesAsNumpy(),
        "rain": hourly.Variables(6).ValuesAsNumpy(),
        "snowfall": hourly.Variables(7).ValuesAsNumpy(),
        "snow_depth": hourly.Variables(8).ValuesAsNumpy(),
        "weather_code": hourly.Variables(9).ValuesAsNumpy(),
        "pressure_msl": hourly.Variables(10).ValuesAsNumpy(),
        "surface_pressure": hourly.Variables(11).ValuesAsNumpy(),
        "cloud_cover": hourly.Variables(12).ValuesAsNumpy(),
        "cloud_cover_low": hourly.Variables(13).ValuesAsNumpy(),
        "cloud_cover_mid": hourly.Variables(14).ValuesAsNumpy(),
        "cloud_cover_high": hourly.Variables(15).ValuesAsNumpy(),
        "wind_speed_10m": hourly.Variables(16).ValuesAsNumpy(),
        "wind_speed_80m": hourly.Variables(17).ValuesAsNumpy(),
        "wind_speed_120m": hourly.Variables(18).ValuesAsNumpy(),
        "wind_direction_10m": hourly.Variables(19).ValuesAsNumpy(),
        "wind_direction_80m": hourly.Variables(20).ValuesAsNumpy(),
        "wind_direction_120m": hourly.Variables(21).ValuesAsNumpy(),
        "wind_gusts_10m": hourly.Variables(22).ValuesAsNumpy(),
        "is_day": hourly.Variables(23).ValuesAsNumpy(),
        "sunshine_duration": hourly.Variables(24).ValuesAsNumpy(),
        "wet_bulb_temperature_2m": hourly.Variables(25).ValuesAsNumpy(),
        "boundary_layer_height": hourly.Variables(26).ValuesAsNumpy(),
        "shortwave_radiation": hourly.Variables(27).ValuesAsNumpy(),
    }

    # Convert to DataFrame
    df = pd.DataFrame(hourly_data)
    all_weather_data.append(df)

# Combine all locations into one DataFrame
final_df = pd.concat(all_weather_data, ignore_index=True)

# Save to CSV (optional)
final_df.to_csv("hourly_weather_data.csv", index=False)

print("Hourly weather data saved successfully!")
