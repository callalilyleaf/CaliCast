from shiny import App, render, ui
import pandas as pd

# Load the CSV data
def load_data():
    return pd.read_csv("current_weather_data.csv")

# UI Layout
app_ui = ui.page_fluid(
    ui.h1("Current Weather Dashboard"),
    ui.output_table("weather_table")
)

# Server Logic
def server(input, output, session):
    @output
    @render.table
    def weather_table():
        df = load_data()
        return df

# Create and run the app
app = App(app_ui, server)
