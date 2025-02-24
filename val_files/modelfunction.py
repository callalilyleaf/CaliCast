#%%
import pandas as pd
import numpy as np
import joblib

def prepare_weather_data(df, target_var, past_hours=12):
    """
    Prepare dataset by creating only past weather features.
    """
    df = df.copy()

    # Create past hour features
    for i in range(1, past_hours + 1):
        df[f'{target_var}_lag_{i}'] = df[target_var].shift(i)

    # Drop rows with NaN values due to shifting
    df = df.dropna()

    return df


def transform_datetime(df, datetime_col):
    # Convert to datetime if it's not already
    df[datetime_col] = pd.to_datetime(df[datetime_col])

    # Extract basic time components
    df["year"] = df[datetime_col].dt.year
    df["month"] = df[datetime_col].dt.month
    df["day"] = df[datetime_col].dt.day
    df["hour"] = df[datetime_col].dt.hour  # Hour stays as 0-23

    # Extract day of the week (0 = Monday, 6 = Sunday)
    df["day_of_week"] = df[datetime_col].dt.weekday

    # Sin/Cos encoding for cyclical features
    df["day_of_week_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
    df["day_of_week_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)
    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

    return df
#%%
def predict_weather_for_locations(location_ids):
    """
    Takes a list of unique location IDs (0-11), processes weather data, 
    and returns a dataframe with predictions for all locations.

    Args:
        location_ids (list of int): Unique numbers between 0-11 representing location IDs.

    Returns:
        pd.DataFrame: Dataframe containing predictions for all provided locations.
    """

    # Ensure that only valid location ids will be allowed to be used in the model.
    # assert all(isinstance(x, int) and 0 <= x <= 11 for x in location_ids), "IDs must be integers between 0-11."
    location_ids = [x for x in location_ids if isinstance(x, int) and 0 <= x <= 11]




    # Load the necessary data
    model_temp = joblib.load('xgboost_weather_model.pkl')
    current_data = pd.read_csv("hourly_weather_data.csv")
    location_data = pd.read_csv("location.csv")
    
    all_predictions = []

    rename_dict = {
            "location_id": "location_id",
            "time": "time",
            "temperature_2m": "temperature_2m (°C)",
            "relative_humidity_2m": "relative_humidity_2m (%)",
            "dew_point_2m": "dew_point_2m (°C)",
            "apparent_temperature": "apparent_temperature (°C)",
            "precipitation_probability": "precipitation (mm)",  # Adjusted based on missing mapping
            "precipitation": "rain (mm)",  
            "rain": "snowfall (cm)",
            "snowfall": "snow_depth (m)",
            "snow_depth": "weather_code (wmo code)",
            "weather_code": "pressure_msl (hPa)",
            "pressure_msl": "surface_pressure (hPa)",
            "surface_pressure": "cloud_cover (%)",
            "cloud_cover": "cloud_cover_low (%)",
            "cloud_cover_low": "cloud_cover_mid (%)",
            "cloud_cover_mid": "cloud_cover_high (%)",
            "cloud_cover_high": "wind_speed_10m (km/h)",
            "wind_speed_10m": "wind_speed_100m (km/h)",
            "wind_speed_100m": "wind_direction_10m (°)",
            "wind_direction_10m": "wind_direction_100m (°)",
            "wind_direction_100m": "wind_gusts_10m (km/h)",
            "wind_gusts_10m": "boundary_layer_height (m)",
            "is_day": "wet_bulb_temperature_2m (°C)",
            "sunshine_duration": "is_day ()",
            "wet_bulb_temperature_2m": "sunshine_duration (s)",
            "boundary_layer_height": "shortwave_radiation (W/m²)",
            "shortwave_radiation": "direct_radiation (W/m²)",
            "direct_radiation": "diffuse_radiation (W/m²)",
            "diffuse_radiation": "direct_normal_irradiance (W/m²)",
            "direct_normal_irradiance": "global_tilted_irradiance (W/m²)",
            "global_tilted_irradiance": "terrestrial_radiation (W/m²)",
        }

        # Apply renaming to your DataFrame
    current_data = current_data.rename(columns=rename_dict)

    for location_id in location_ids:
        # Get the most recent 13 rows for the given location
        clean_data = current_data.query(f"location_id == {location_id}").sort_values(by="time").tail(13)

        

        # Prepare data for ML model
        new_data = prepare_weather_data(clean_data, "temperature_2m (°C)", past_hours=12)
        new_data = transform_datetime(new_data, "time")
        new_data = pd.merge(new_data, location_data, on='location_id', how='left')

        
        prediction_input = new_data.tail(1)
        X_new = prediction_input[list(model_temp.feature_names_in_)]

        # Predict 12 future time steps
        num_predictions = 12
        predictions = []
        current_input = X_new.copy()

        for i in range(num_predictions):
            next_pred = model_temp.predict(current_input)[0]
            predictions.append(next_pred)

            # Manually shift all lag features
            for lag in range(12, 1, -1):  # Move values down the chain
                current_input[f'temperature_2m (°C)_lag_{lag}'] = current_input[f'temperature_2m (°C)_lag_{lag - 1}']
            
            # Insert new prediction at lag_1
            current_input[f'temperature_2m (°C)_lag_1'] = next_pred

        # Store results in a dataframe
        pred_df = pd.DataFrame({
            "location_id": location_id,
            "predicted_temperature": predictions,
            "hour_ahead": range(1, num_predictions + 1)
        })

        # Merge with location details
        merged_df = pd.merge(pred_df, location_data, on="location_id", how="left")
        all_predictions.append(merged_df)

    # Combine all results into a single dataframe
    final_df = pd.concat(all_predictions, ignore_index=True)
    return final_df




#%%
location_ids = [0,1,2,3,4,5,6,7,8,9,10,11,12,23, ' dupser dotggg']
df = predict_weather_for_locations(location_ids)
print(df.head(20))
# %%
# print(df.columns)