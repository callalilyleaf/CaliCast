from shiny import App, ui, render, reactive
import pandas as pd
from plotnine import ggplot, aes, geom_bar, geom_col, labs, theme_minimal, position_dodge,  geom_point, scale_fill_brewer, scale_fill_gradient, geom_tile, geom_line, facet_wrap, scale_x_continuous, scale_x_datetime, theme, element_text, geom_boxplot
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
# Ivan: I don't have this file so I will comment it out
# from modelfunction import predict_weather_for_locations
from historical_files.SQLQueryCode import get_weather_sql_df, ALLLOCATIONSHOURLYDATA, SINGLELOCATIONHOURLYDATA

# To-dos: 
# 1. Find the way to load current df, all & single location dfs
# 2. Put the ggplots for each of the historical category (display all)  
# (Stretches: )
# 3. Have buttons/ drop down list for user to choose which category to deplay and for multiple locations or the trends of a single one
# 4. Have various buttons that get data from different time frame: 1 week, 1 month, 3 months, 6 months, customerized


# Load weather data dfs
current_weather_data = pd.read_csv("val_files\current_weather_data.csv")
historical_weather_data_all = get_weather_sql_df(ALLLOCATIONSHOURLYDATA)
historical_weather_data_single = get_weather_sql_df(SINGLELOCATIONHOURLYDATA)

# Mapping location_id to city names
location_map = {
    0: "San Diego", 1: "Lemoore", 2: "Ramona", 3: "Palm Springs",
    4: "Los Angeles", 5: "Fresno", 6: "San Francisco", 7: "Sacramento",
    8: "Truckee", 9: "Chico", 10: "Mount Shasta", 11: "Crescent City"
}

# Current weather data df set up
current_weather_data["city"] = current_weather_data["location_id"].map(location_map)

# Historical weather data df set up
historical_weather_data_all["city"] = historical_weather_data_all["location_id"].map(location_map)
historical_weather_data_single["city"] = historical_weather_data_single["location_id"].map(location_map)


# Define UI with Tabs
app_ui = ui.page_fluid(
    ui.h1("Weather Dashboard"),
    
    ui.navset_tab(
        ui.nav_panel("Current Weather", 
            ui.h2("Data retrieved at: ", ui.output_text("cur_retrieved_time"),"\n"),
            ui.h3("Temperature vs Feels-Like"),
            ui.output_plot("cur_temp_bar_chart"),
            ui.h3("Humidity"),
            ui.output_plot("cur_humidity_bar_chart"),
            ui.h3("Cloud Cover"),
            ui.output_plot("cur_cloud_coverage_heatmap"),
            ui.h3("Cloud Cover vs. Humidity"),
            ui.output_plot("cur_cloud_humidity_scatter"),
            ui.h3("Wind Speed"),
            ui.input_select("selected_city", "Select City:", choices=list(current_weather_data["city"].unique())),
            ui.output_plot("cur_wind_polar_plot"),
         

        ),
        ui.nav_panel("Historical Data", ui.h2("Data retrieved at: ", ui.output_text("retrieved_time"),"\n"), 
                     # Historical Data: city, weather_code, temperature, apparent_temperature, wind_speed, cloud_cover, surface_pressure
            ui.h3("Select Dataset"),
            ui.input_action_button("btn_all", "Use All Locations Data"), # choose all/ single locations data
            ui.input_action_button("btn_single", "Use Single Location Data"),
            
            ui.h3("Temperature Trends"),
            ui.output_plot("his_temp_line_chart"),
            ui.h3("Temperature vs Feels-Like"),
            ui.output_plot("his_temp_bar_chart"),
            ui.h3("Humidity"),
            ui.output_plot("his_humidity_bar_chart"),
            ui.h3("Cloud Cover"),
            ui.output_plot("his_cloud_coverage_heatmap"),
            ui.h3("Humidity v.s. Cloud Cover"),
            ui.output_plot("his_humidity_vs_cloud_cover_chart"),
            ui.h3("Weather Condition Frequency"),
            ui.output_plot("his_weather_code_frequency"),
            ui.h3("Wind Speed"),
            ui.output_plot("his_wind_speed_chart"),        
        ), 
        
        ui.nav_panel("Prediction Model",
                    ui.h2("Weather Prediction Model"),
                    ui.output_plot("create_prediction_plots")
                    
                     )  

    )
)

# Convert data to long format for bar grouping by city
weather_long = current_weather_data.melt(
    id_vars=["city"], 
    value_vars=["temperature_2m", "apparent_temperature"], 
    var_name="Temperature Type", value_name="Temperature"
)

#

# Server logic
def server(input, output, session):
    
    @reactive.calc # dynamical df loading according to user selection with buttons
    def df():
        if input.btn_all():
            return historical_weather_data_all
        elif input.btn_single():
            return historical_weather_data_single
        return historical_weather_data_all #  Default dataset: all locations


    @output
    @render.text
    def cur_retrieved_time():
        file_path = "current_weather_data.csv"
        modified_time = os.path.getmtime(file_path)  # Get last modified time
        return datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d %H:%M:%S")

    # Temperature Bar Chart (Cities on X-axis)
    @output
    @render.plot
    def cur_temp_bar_chart():
        return (
            ggplot(current_weather_data, aes(x="city", y="Temperature", fill="Temperature Type")) +
            geom_bar(stat="identity", position=position_dodge()) +
            scale_fill_brewer(type="qual", palette="Paired") +
            theme_minimal() +
            labs(title="Temperature vs Feels-Like by City",
                 x="City", y="Temperature (°C)") +
            theme(axis_text_x = element_text(angle=45, hjust=1))
        )

     # Humidity Bar Chart
    @output
    @render.plot
    def cur_humidity_bar_chart():
        return (
            ggplot(current_weather_data, aes(x="city", y="relative_humidity_2m", fill="city")) +  
            geom_col(show_legend=False) +  
            scale_fill_brewer(type="seq", palette="Greys") +  
            # scale_fill_brewer(type="qual", palette="Paired") +
            theme_minimal() +
            labs(title="Humidity by City", x="City", y="Humidity (%)") +
            theme(axis_text_x = element_text(angle=45, hjust=1))

        )
    
    # cloud coverage
    @output
    @render.plot
    def cur_cloud_coverage_heatmap():
        return (
            ggplot(current_weather_data, aes(x="city", y="cloud_cover", fill="cloud_cover")) +  
            geom_col(show_legend=True) +  
            scale_fill_gradient(low="lightblue", high="darkblue") +  # Adjust colors to your preference
            labs(title="Cloud Coverage by City", x="City", y="") +
            theme_minimal() +
            theme(axis_text_x = element_text(angle=45, hjust=1))

        )

    # Scatter Plot for Cloud Cover vs. Humidity
    @output
    @render.plot
    def cur_cloud_humidity_scatter():
       
        return (
            ggplot(current_weather_data, aes(x="relative_humidity_2m", y="cloud_cover", color="city")) +
            geom_point(size=3) +
            labs(title="Cloud Cover vs. Humidity by City",
                 x="Humidity (%)", y="Cloud Cover (%)") +
            theme_minimal()
        )

    # Wind Rose Chart (Filtered by City)
    @output
    @render.plot
    def cur_wind_polar_plot():
        # Filter data for selected city
        
        # To be edified: make the column name the same as the historical dfs
        df = current_weather_data[current_weather_data["city"] == input.selected_city()]
        
        if df.empty:
            return plt.figure()  # Return empty figure if no data
        
        # Convert wind direction to radians
        wind_direction_rad = np.radians(df["wind_direction_10m"])
        wind_speed = df["wind_speed_10m"]

        # Create polar plot
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.set_title(f"Wind Speed & Direction for {input.selected_city()}\n \n")
        
        ax.scatter(wind_direction_rad, wind_speed, c="blue", alpha=0.7, edgecolors="black")
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        
        
        return fig
    
    ### These are the functions for the historical Charts
    # Bar Chart for temperature trends
    @output
    @render.plot
    def his_temp_line_chart():
        return(
            ggplot(df, aes(x="observation_date", y="temperature", color="city")) +  
            geom_line(size=1) +  
            labs(title="Temperature Trends Over Time", x="Date", y="Temperature (°C)") +  
            theme_minimal() +  
            facet_wrap('~city', scales="free_x") +  # Separate plots per city
            scale_x_datetime(date_breaks="1 month", date_labels="%b %Y")
        )
    
    # Temperature Bar Chart for comparing different cities at the same time(Cities on X-axis)
    @output
    @render.plot
    def his_temp_bar_chart():
        df_choice = df() # get the df according to user tab choice
        return (
            ggplot(df_choice, aes(x="city", y="Temperature", fill="Temperature Type")) +
            geom_bar(stat="identity", position=position_dodge()) +
            scale_fill_brewer(type="qual", palette="Paired") +
            theme_minimal() +
            labs(title="Temperature vs Feels-Like by City",
                 x="City", y="Temperature (°C)") +
            theme(axis_text_x = element_text(angle=45, hjust=1))
        )

    # Humidity Bar Chart
    @output
    @render.plot
    def his_humidity_bar_chart():
        df_choice = df()
        return (
            ggplot(df_choice, aes(x="city", y="humidity", fill="city")) +  
            geom_col(show_legend=False) +  
            scale_fill_brewer(type="seq", palette="Greys") +  
            # scale_fill_brewer(type="qual", palette="Paired") +
            theme_minimal() +
            labs(title="Humidity by City", x="City", y="Humidity (%)") +
            theme(axis_text_x = element_text(angle=45, hjust=1))
        )
        
    # Humidity vs cloud cover Chart
    @output
    @render.plot
    def his_humidity_vs_cloud_cover_chart():
        return(
            ggplot(df, aes(x="humidity", y="cloud_cover", color="city")) +  
            geom_point(size=3, alpha=0.7) +  
            labs(title="Humidity vs. Cloud Cover", x="Humidity (%)", y="Cloud Cover (%)") +  
            theme_minimal()
        )
    
    # Weather Code Frequency (Bar Chart)
    @output
    @render.plot
    def his_weather_code_frequency():
        return (ggplot(df, aes(x="weather_code", fill="city")) +  
                geom_bar(position="dodge") +  
                labs(title="Weather Code Frequency", x="Weather Code", y="Count") +  
                theme_minimal()
                )
    
    @output
    @render.plot
    def his_cloud_coverage_heatmap():
        df_choice = df()
        return (
            ggplot(df_choice, aes(x="city", y="cloud_cover", fill="cloud_cover")) +  
            geom_col(show_legend=True) +  
            scale_fill_gradient(low="lightblue", high="darkblue") +  # Adjust colors to your preference
            labs(title="Cloud Coverage by City", x="City", y="") +
            theme_minimal() +
            theme(axis_text_x = element_text(angle=45, hjust=1))

        )
        
    @output
    @render.plot
    def his_wind_speed_chart():
        return (ggplot(df, aes(x="city", y="wind_speed", fill="city")) +  
                geom_boxplot() +  
                labs(title="Wind Speed Distribution by City", x="City", y="Wind Speed (m/s)") +  
                theme_minimal() +  
                theme(axis_text_x=element_text(angle=45, hjust=1))
                )
        
    # # Temperature trends Chart
    # @output
    # @render.plot
    # def his_temp_trend_plots():
    #     df_choice = df()
    #     return(
    #     ggplot(df_choice, aes(x = "city", y = "temperature", group = "city", color = "city")) +
    #     geom_line(size = 1) +
    #     geom_point(size = 2) +
    #     theme_minimal() +
    #     labs(title = "Temperature Trends Across Locations",
    #          x = "Location",
    #          y = "Temperature (°C)") +
    #     theme(axis_text_x = element_text(angle = 45, hjust = 1))
    #     )
    
    

    ### These are the functions for the predictions
    # Ivan: I don't have predict_weather_for_locations file so I comment it out for now
    
    # @output
    # @render.plot
    # def create_prediction_plots():
    

    #     location_ids = [0,1,2,3,4,5,6,7,8,9,10,11]
    #     df = predict_weather_for_locations(location_ids)

    #     # Debugging: Print df to see its contents
    #     print("DEBUG: DataFrame returned by predict_weather_for_locations:")
    #     print(df)

    #     # Check if df is None
    #     if df is None:
    #         print("ERROR: predict_weather_for_locations() returned None!")
    #         return plt.figure()  # Return an empty plot instead of crashing

    #     # Check if df is actually a DataFrame
    #     if not isinstance(df, pd.DataFrame):
    #         print(f"ERROR: Expected DataFrame but got {type(df)} instead!")
    #         return plt.figure()

    #     # Check if DataFrame is empty
    #     if df.empty:
    #         print("ERROR: DataFrame is empty!")
    #         return plt.figure()

    #     # If df exists and has columns, print them
    #     print("Columns in df:", df.columns)

    #     return (
    #         ggplot(df, aes(x="hour_ahead", y="predicted_temperature", color="city")) +
    #         geom_line(size=1.5) +
    #         labs(title="",
    #              x="Hours Ahead", 
    #              y="Temperature C",
    #              color = "City") +
    #         theme_minimal() +
    #         facet_wrap('~city', ncol=4) +
    #         scale_x_continuous(breaks=range(1, 12, 2))
    #     )
    
    # @output
    # @render.data_frame
    # def display_prediction_table():
    #     location_ids = [0,1,2,3,4,5,6,7,8,9,10,11]
        
    #     df = predict_weather_for_locations(location_ids)
    #     # print(df.head(20))
        
    #     return df.head()







# Run the app
app = App(app_ui, server)
