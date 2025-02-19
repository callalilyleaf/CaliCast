from shiny import App, render, ui
import pandas as pd

# Load CSV data functions
def load_current_weather():
    return pd.read_csv("current_weather_data.csv")

def load_hourly_weather():
    return pd.read_csv("hourly_weather_data.csv")

# UI Layout with Tabs
app_ui = ui.page_fluid(
    ui.h1("Weather Dashboard"),
    ui.navset_tab(  
        ui.nav_panel("Current Weather", ui.output_table("current_weather_table")),
        ui.nav_panel("Hourly Weather", ui.output_table("hourly_weather_table"))

    )
)

# Server Logic
def server(input, output, session):
    @output
    @render.table
    def current_weather_table():
        return load_current_weather()

    @output
    @render.table
    def hourly_weather_table():
        return load_hourly_weather()

# Create and run the app
app = App(app_ui, server)
