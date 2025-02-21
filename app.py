import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load weather data
weather_data = pd.read_csv("current_weather_data.csv")

# Initialize Dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True  # Allows callbacks for dynamically generated components

# Unique locations for dropdown
unique_locations = weather_data["location_id"].unique()

# Layout of the dashboard with Tabs
app.layout = html.Div([
    html.H1("Weather Dashboard", style={'textAlign': 'center'}),

    dcc.Tabs(id="tabs", value="tab1", children=[
        dcc.Tab(label="Current Weather", value="tab1"),
        dcc.Tab(label="Historical Data", value="tab2"),
        dcc.Tab(label="Prediction Model", value="tab3")
    ]),

    html.Div(id="tab-content")
])

# Callback to update tab content
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def update_tab(selected_tab):
    if selected_tab == "tab1":
        return html.Div([
            # Temperature Line Graph
            dcc.Graph(id='temperature-line', 
                      figure=px.line(weather_data, x="location_id", 
                                     y=["temperature_2m", "apparent_temperature"],
                                     title="Current Temperature vs. Feels-Like Temperature",
                                     labels={"value": "Temperature (°C)", "variable": "Temperature Type", "location_id": "Location ID"},
                                     markers=True)),

            # Temperature Scatter Plot
            dcc.Graph(id='temperature-scatter',
                      figure=px.scatter(weather_data, x="location_id", y="temperature_2m",
                                        color="temperature_2m",
                                        size=[10]*len(weather_data),
                                        title="Current Temperature Scatter Plot",
                                        labels={"temperature_2m": "Temperature (°C)", "location_id": "Location ID"},
                                        color_continuous_scale="Oranges")),

            # Humidity Bar Chart
            dcc.Graph(id='humidity-bar',
                      figure=px.bar(weather_data, x="location_id", y="relative_humidity_2m",
                                    color="relative_humidity_2m",
                                    title="Humidity Levels",
                                    labels={"relative_humidity_2m": "Humidity (%)", "location_id": "Location ID"},
                                    color_continuous_scale="Blues")),

            # Dropdown + Wind Rose Graph
            html.Div([
                html.Label("Select Location:", style={'display': 'flex', 'justify-self': 'self-end'}),
                dcc.Dropdown(
                    id="location-dropdown",
                    options=[{"label": loc, "value": loc} for loc in unique_locations],
                    value=unique_locations[0],  
                    clearable=False,
                    className="custom-dropdown"
                )
            ], id="location-dropdown-container"),

            dcc.Graph(id='wind-rose'),

            # Cloud Cover Bar Chart
            dcc.Graph(id='cloud-cover-bar',
                      figure=px.bar(weather_data, x="location_id", y="cloud_cover",
                                    color="cloud_cover",
                                    title="Cloud Cover Percentage",
                                    labels={"cloud_cover": "Cloud Cover (%)", "location_id": "Location ID"},
                                    color_continuous_scale="gray")),

            # Pressure Bar Chart
            dcc.Graph(id='pressure-bar',
                      figure=px.bar(weather_data, x="location_id", y="pressure_msl",
                                    color="pressure_msl",
                                    title="Pressure Levels",
                                    labels={"pressure_msl": "Pressure (hPa)", "location_id": "Location ID"},
                                    color_continuous_scale="Purples"))
        ])
    
    elif selected_tab == "tab2":
        return html.Div([
            html.H3("Tab 2 content will go here"),
        ])

    elif selected_tab == "tab3":
        return html.Div([
            html.H3("Tab 3 content will go here"),
        ])

    return html.Div("No content available.")

# Callback to update Wind Rose chart based on location selection
@app.callback(
    Output("wind-rose", "figure"),
    Input("location-dropdown", "value")
)
def update_wind_rose(selected_location):
    filtered_data = weather_data[weather_data["location_id"] == selected_location]

    fig = px.bar_polar(filtered_data, 
                       r="wind_speed_10m",  
                       theta="wind_direction_10m",  
                       color="wind_speed_10m",  
                       title=f"Wind Speed & Direction for {selected_location}",
                       labels={"wind_speed_10m": "Wind Speed (km/h)", "wind_direction_10m": "Wind Direction (°)"},
                       color_continuous_scale="Greens")

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
