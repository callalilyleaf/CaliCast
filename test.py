import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime
import pytz

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Location mapping with location_id
locations = [
    (0, 32.724075, 117.14286),
    (1, 32.864674, 114.895966),
    (2, 33.07557, 116.646194),
    (3, 33.848858, 116.56289),
    (4, 34.059753, 118.125),
    (5, 36.801403, 119.802895),
    (6, 37.785587, 122.409645),
    (7, 38.558872, 121.54891),
    (8, 39.191563, 120.20633),
    (9, 39.753952, 121.79416),
    (10, 41.300526, 122.281204),
    (11, 41.722317, 124.2547)
]

# Open-Meteo API URL and parameters
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": [lat for _, lat, _ in locations],
    "longitude": [lon for _, _, lon in locations],
    "current": [
        "temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature",
        "precipitation", "rain", "snowfall", "snow_depth", "weather_code",
        "pressure_msl", "surface_pressure", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high",
        "wind_speed_10m", "wind_speed_100m", "wind_direction_10m", "wind_direction_100m", "wind_gusts_10m",
        "boundary_layer_height", "wet_bulb_temperature_2m", "is_day", "sunshine_duration",
        "shortwave_radiation", "direct_radiation", "diffuse_radiation", "direct_normal_irradiance",
        "global_tilted_irradiance", "terrestrial_radiation"
    ]
}
responses = openmeteo.weather_api(url, params=params)

# Process all locations
weather_data = []
for i, response in enumerate(responses):
    location_id, _, _ = locations[i]
    
    current = response.Current() #access current weather
    # in UTC
    current_time_utc = pd.Timestamp.utcnow()
    # to Pacific Time (handles PST/PDT automatically)
    pacific = pytz.timezone("America/Los_Angeles")
    current_time_pacific = current_time_utc.tz_convert(pacific)
    current_time = current_time_pacific
    
    weather_data.append({
        "location_id": location_id,
        "time": current_time,
        "temperature_2m (°C)": current.Variables(0).Value(),
        "relative_humidity_2m (%)": current.Variables(1).Value(),
        "dew_point_2m (°C)": current.Variables(2).Value(),
        "apparent_temperature (°C)": current.Variables(3).Value(),
        "precipitation (mm)": current.Variables(4).Value(),
        "rain (mm)": current.Variables(5).Value(),
        "snowfall (cm)": current.Variables(6).Value(),
        "snow_depth (m)": current.Variables(7).Value(),
        "weather_code (wmo code)": current.Variables(8).Value(),
        "pressure_msl (hPa)": current.Variables(9).Value(),
        "surface_pressure (hPa)": current.Variables(10).Value(),
        "cloud_cover (%)": current.Variables(11).Value(),
        "cloud_cover_low (%)": current.Variables(12).Value(),
        "cloud_cover_mid (%)": current.Variables(13).Value(),
        "cloud_cover_high (%)": current.Variables(14).Value(),
        "wind_speed_10m (km/h)": current.Variables(15).Value(),
        "wind_speed_100m (km/h)": current.Variables(16).Value(),
        "wind_direction_10m (°)": current.Variables(17).Value(),
        "wind_direction_100m (°)": current.Variables(18).Value(),
        "wind_gusts_10m (km/h)": current.Variables(19).Value(),
        "boundary_layer_height (m)": current.Variables(20).Value(),
        "wet_bulb_temperature_2m (°C)": current.Variables(21).Value(),
        "is_day ()": current.Variables(22).Value(),
        "sunshine_duration (s)": current.Variables(23).Value(),
        "shortwave_radiation (W/m²)": current.Variables(24).Value()
    })
    
    print(f"Location ID: {location_id}, Time: {current_time} UTC")
    print(f"Temperature: {current.Variables(0).Value()}°C, Humidity: {current.Variables(1).Value()}%")
    print(f"Wind Speed: {current.Variables(15).Value()} km/h, Wind Direction: {current.Variables(17).Value()}°")
    print("---")

# Convert to DataFrame
weather_df = pd.DataFrame(weather_data)

# Save latest data (overwrite)
weather_df.to_csv("current_weather_data.csv", index=False)
print("\nCurrent weather data saved to 'current_weather_data.csv'.")

# Append to historical data file (if exists, append; else create)
historical_file = "historical_weather_data.csv"
try:
    existing_df = pd.read_csv(historical_file)
    updated_df = pd.concat([existing_df, weather_df], ignore_index=True)
    updated_df.to_csv(historical_file, index=False)
except FileNotFoundError:
    weather_df.to_csv(historical_file, index=False)
    
print("Historical weather data updated in 'historical_weather_data.csv'.")
