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
SELECT * FROM location;
"""
# Execute the query and load the result into a Pandas DataFrame
with engine.connect() as conn:
    df = pd.read_sql_query(query, conn)
print(df)