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
query = """
SELECT temperature_2m, city
FROM weather_data wd
INNER JOIN location l ON l.location_id = wd.location_id
WHERE DATE(time) BETWEEN '2002-12-08' AND '2003-12-08' AND HOUR(time) = "01"
"""
# Old SQL Query
# SELECT
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


# Execute the query and load the result into a Pandas DataFrame
with engine.connect() as conn:
    df = pd.read_sql_query(query, conn)
    
print(df)