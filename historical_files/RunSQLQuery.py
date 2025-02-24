#%%
import sqlalchemy
import pandas as pd
from SQLQueryCode import get_weather_sql_df, ALLLOCATIONSHOURLYDATA, SINGLELOCATIONHOURLYDATA

get_weather_sql_df(ALLLOCATIONSHOURLYDATA)
get_weather_sql_df(SINGLELOCATIONHOURLYDATA)




