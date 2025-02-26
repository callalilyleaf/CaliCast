import sqlalchemy
from sqlalchemy import text
import pandas as pd

# Your database credentials
db_user = "mitchell"
db_password = "password"
db_name = "310weather"
db_host = "34.60.163.168"

# Create the database connection URL
db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"

# Create SQLAlchemy engine
engine = sqlalchemy.create_engine(db_url)
def get_weather_sql_df(queryText):
    # Execute the query and load the result into a Pandas DataFrame
    
    with engine.connect() as conn:
        df = pd.read_sql_query(queryText, conn)
    return df


# Testing query code:
# query = """ 
#     SELECT
#     wd.*,
#     l.city,
#     l.county
# FROM
#     (SELECT location_id FROM weather_data LIMIT 1) AS wd_distinct
# LEFT JOIN
#     weather_data wd ON wd.location_id = wd.location_id
# LEFT JOIN
#     location l ON wd.location_id = l.location_id
# WHERE wd.location_id = 1;
# """
    
        
# --ALL Locations HOURLY Data
# -- Don't worry about AVG and MIN and such, it does not affect the value
ALLLOCATIONSHOURLYDATA = """
SELECT
    wd.location_id,
    AVG(temperature_2m) AS temperature,
    MIN(time) AS observation_date,
    AVG(relative_humidity_2m) AS humidity,
    AVG(apparent_temperature) AS apparent_temperature,
    MAX(weather_code) AS weather_code,
    AVG(surface_pressure) AS surface_pressure,
    AVG(cloud_cover) AS cloud_cover,
    AVG(wind_speed_10m) AS wind_speed,
    MIN(sunshine_duration) AS sunshine_duration
FROM
    weather_data wd
INNER JOIN
    location l ON l.location_id = wd.location_id
WHERE
    l.city IN ('Ramona', 'San Diego','Lemoore','Palm Springs','Los Angeles','Fresno','San Francisco','Sacramento','Truckee','Chico','Mount Shasta','Crescent City')
    AND DATE(time) BETWEEN '2015-02-13' AND '2025-02-13'
    AND HOUR(time) = 13
GROUP BY
    wd.location_id, DATE(time)
ORDER BY
    observation_date DESC;
"""

ALLLOCATIONSHOURLYDATA1W = """
SELECT
    wd.location_id,
    AVG(temperature_2m) AS temperature,
    MIN(time) AS observation_date,
    AVG(relative_humidity_2m) AS humidity,
    AVG(apparent_temperature) AS apparent_temperature,
    MAX(weather_code) AS weather_code,
    AVG(surface_pressure) AS surface_pressure,
    AVG(cloud_cover) AS cloud_cover,
    AVG(wind_speed_10m) AS wind_speed,
    MIN(sunshine_duration) AS sunshine_duration
FROM
    weather_data wd
INNER JOIN
    location l ON l.location_id = wd.location_id
WHERE
    l.city IN ('Ramona', 'San Diego','Lemoore','Palm Springs','Los Angeles','Fresno','San Francisco','Sacramento','Truckee','Chico','Mount Shasta','Crescent City')
    AND DATE(time) BETWEEN '2025-02-07' AND '2025-02-13'
    AND HOUR(time) = 13
GROUP BY
    wd.location_id, DATE(time)
ORDER BY
    observation_date DESC;
"""

ALLLOCATIONSHOURLYDATA1M = """
SELECT
    wd.location_id,
    AVG(temperature_2m) AS temperature,
    MIN(time) AS observation_date,
    AVG(relative_humidity_2m) AS humidity,
    AVG(apparent_temperature) AS apparent_temperature,
    MAX(weather_code) AS weather_code,
    AVG(surface_pressure) AS surface_pressure,
    AVG(cloud_cover) AS cloud_cover,
    AVG(wind_speed_10m) AS wind_speed,
    MIN(sunshine_duration) AS sunshine_duration
FROM
    weather_data wd
INNER JOIN
    location l ON l.location_id = wd.location_id
WHERE
    l.city IN ('Ramona', 'San Diego','Lemoore','Palm Springs','Los Angeles','Fresno','San Francisco','Sacramento','Truckee','Chico','Mount Shasta','Crescent City')
    AND DATE(time) BETWEEN '2025-01-13' AND '2025-02-13'
    AND HOUR(time) = 13
GROUP BY
    wd.location_id, DATE(time)
ORDER BY
    observation_date DESC;
"""

ALLLOCATIONSHOURLYDATA6M = """
SELECT
    wd.location_id,
    AVG(temperature_2m) AS temperature,
    MIN(time) AS observation_date,
    AVG(relative_humidity_2m) AS humidity,
    AVG(apparent_temperature) AS apparent_temperature,
    MAX(weather_code) AS weather_code,
    AVG(surface_pressure) AS surface_pressure,
    AVG(cloud_cover) AS cloud_cover,
    AVG(wind_speed_10m) AS wind_speed,
    MIN(sunshine_duration) AS sunshine_duration
FROM
    weather_data wd
INNER JOIN
    location l ON l.location_id = wd.location_id
WHERE
    l.city IN ('Ramona', 'San Diego','Lemoore','Palm Springs','Los Angeles','Fresno','San Francisco','Sacramento','Truckee','Chico','Mount Shasta','Crescent City')
    AND DATE(time) BETWEEN '2024-08-13' AND '2025-02-13'
    AND HOUR(time) = 13
GROUP BY
    wd.location_id, DATE(time)
ORDER BY
    observation_date DESC;
"""

ALLLOCATIONSHOURLYDATA1Y = """
SELECT
    wd.location_id,
    AVG(temperature_2m) AS temperature,
    MIN(time) AS observation_date,
    AVG(relative_humidity_2m) AS humidity,
    AVG(apparent_temperature) AS apparent_temperature,
    MAX(weather_code) AS weather_code,
    AVG(surface_pressure) AS surface_pressure,
    AVG(cloud_cover) AS cloud_cover,
    AVG(wind_speed_10m) AS wind_speed,
    MIN(sunshine_duration) AS sunshine_duration
FROM
    weather_data wd
INNER JOIN
    location l ON l.location_id = wd.location_id
WHERE
    l.city IN ('Ramona', 'San Diego','Lemoore','Palm Springs','Los Angeles','Fresno','San Francisco','Sacramento','Truckee','Chico','Mount Shasta','Crescent City')
    AND DATE(time) BETWEEN '2024-02-13' AND '2025-02-13'
    AND HOUR(time) = 13
GROUP BY
    wd.location_id, DATE(time)
ORDER BY
    observation_date DESC;
"""

# And here, simply made the location one value for the single location query hourly data:

# -- Don't worry about AVG and MIN and such, it does not affect the value
# Change the location name in line 91 for each location (line 91: l.city IN ('Ramona') -- Location needs to be variable)
SINGLELOCATIONHOURLYDATA = """
SELECT
    wd.location_id,
    AVG(temperature_2m) AS temperature,
    MIN(time) AS observation_date,
    AVG(relative_humidity_2m) AS humidity,
    AVG(apparent_temperature) AS apparent_temperature,
    MAX(weather_code) AS weather_code,
    AVG(surface_pressure) AS surface_pressure,
    AVG(cloud_cover) AS cloud_cover,
    AVG(wind_speed_10m) AS wind_speed,
    MIN(sunshine_duration) AS sunshine_duration
FROM
    weather_data wd
INNER JOIN
    location l ON l.location_id = wd.location_id
WHERE
    l.city IN ('Ramona') -- Location needs to be variable
    AND DATE(time) BETWEEN '2002-12-08' AND '2003-12-08'
    AND HOUR(time) = 13
GROUP BY
    wd.location_id, DATE(time)
ORDER BY
    observation_date DESC;
"""

SINGLELOCATIONHOURLYDATA1W = """
SELECT
    wd.location_id,
    AVG(temperature_2m) AS temperature,
    MIN(time) AS observation_date,
    AVG(relative_humidity_2m) AS humidity,
    AVG(apparent_temperature) AS apparent_temperature,
    MAX(weather_code) AS weather_code,
    AVG(surface_pressure) AS surface_pressure,
    AVG(cloud_cover) AS cloud_cover,
    AVG(wind_speed_10m) AS wind_speed,
    MIN(sunshine_duration) AS sunshine_duration
FROM
    weather_data wd
INNER JOIN
    location l ON l.location_id = wd.location_id
WHERE
    l.city IN ('Ramona') -- Location needs to be variable
    AND DATE(time) BETWEEN '2025-02-07' AND '2025-02-13'
    AND HOUR(time) = 13
GROUP BY
    wd.location_id, DATE(time)
ORDER BY
    observation_date DESC;
"""

SINGLELOCATIONHOURLYDATA1M = """
SELECT
    wd.location_id,
    AVG(temperature_2m) AS temperature,
    MIN(time) AS observation_date,
    AVG(relative_humidity_2m) AS humidity,
    AVG(apparent_temperature) AS apparent_temperature,
    MAX(weather_code) AS weather_code,
    AVG(surface_pressure) AS surface_pressure,
    AVG(cloud_cover) AS cloud_cover,
    AVG(wind_speed_10m) AS wind_speed,
    MIN(sunshine_duration) AS sunshine_duration
FROM
    weather_data wd
INNER JOIN
    location l ON l.location_id = wd.location_id
WHERE
    l.city IN ('Ramona') -- Location needs to be variable
    AND DATE(time) BETWEEN '2025-01-13' AND '2025-02-13'
    AND HOUR(time) = 13
GROUP BY
    wd.location_id, DATE(time)
ORDER BY
    observation_date DESC;
"""

SINGLELOCATIONHOURLYDATA6M = """
SELECT
    wd.location_id,
    AVG(temperature_2m) AS temperature,
    MIN(time) AS observation_date,
    AVG(relative_humidity_2m) AS humidity,
    AVG(apparent_temperature) AS apparent_temperature,
    MAX(weather_code) AS weather_code,
    AVG(surface_pressure) AS surface_pressure,
    AVG(cloud_cover) AS cloud_cover,
    AVG(wind_speed_10m) AS wind_speed,
    MIN(sunshine_duration) AS sunshine_duration
FROM
    weather_data wd
INNER JOIN
    location l ON l.location_id = wd.location_id
WHERE
    l.city IN ('Ramona') -- Location needs to be variable
    AND DATE(time) BETWEEN '2024-08-07' AND '2025-02-13'
    AND HOUR(time) = 13
GROUP BY
    wd.location_id, DATE(time)
ORDER BY
    observation_date DESC;
"""

SINGLELOCATIONHOURLYDATA1Y = """
SELECT
    wd.location_id,
    AVG(temperature_2m) AS temperature,
    MIN(time) AS observation_date,
    AVG(relative_humidity_2m) AS humidity,
    AVG(apparent_temperature) AS apparent_temperature,
    MAX(weather_code) AS weather_code,
    AVG(surface_pressure) AS surface_pressure,
    AVG(cloud_cover) AS cloud_cover,
    AVG(wind_speed_10m) AS wind_speed,
    MIN(sunshine_duration) AS sunshine_duration
FROM
    weather_data wd
INNER JOIN
    location l ON l.location_id = wd.location_id
WHERE
    l.city IN ('Ramona') -- Location needs to be variable
    AND DATE(time) BETWEEN '2024-02-13' AND '2025-02-13'
    AND HOUR(time) = 13
GROUP BY
    wd.location_id, DATE(time)
ORDER BY
    observation_date DESC;
"""

get_weather_sql_df(ALLLOCATIONSHOURLYDATA)