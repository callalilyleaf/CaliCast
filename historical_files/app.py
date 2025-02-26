import faicons as fa
import plotly.express as px

# Load data and compute static values
from shared import app_dir, tips
from shinywidgets import render_plotly

from shiny import reactive, render, App
from shiny.express import input, ui

# Sample weather data with FontAwesome icons
LOCATIONS = [
    {"name": "Los Angeles", "icon": fa.icon_svg("sun"), "high": 75, "low": 60},
    {"name": "San Francisco", "icon": fa.icon_svg("sun"), "high": 65, "low": 50},
    {"name": "San Diego", "icon": fa.icon_svg("cloud-sun"), "high": 70, "low": 58},
    {"name": "Sacramento", "icon": fa.icon_svg("sun"), "high": 80, "low": 55},
    {"name": "Fresno", "icon": fa.icon_svg("fire"), "high": 85, "low": 60},
    {"name": "Oakland", "icon": fa.icon_svg("smog"), "high": 66, "low": 52},
    {"name": "San Jose", "icon": fa.icon_svg("cloud-rain"), "high": 72, "low": 54},
    {"name": "Long Beach", "icon": fa.icon_svg("water"), "high": 74, "low": 59},
    {"name": "Bakersfield", "icon": fa.icon_svg("fire"), "high": 90, "low": 62},
    {"name": "Anaheim", "icon": fa.icon_svg("sun"), "high": 78, "low": 60},
    {"name": "Santa Barbara", "icon": fa.icon_svg("sun"), "high": 73, "low": 57},
    {"name": "Palm Springs", "icon": fa.icon_svg("temperature-high"), "high": 95, "low": 70},
]    

# Reactive variable for selected location
selected_location = reactive.value(LOCATIONS[0]["name"])
    
bill_rng = (min(tips.total_bill), max(tips.total_bill))

# Add page title and sidebar    
ui.page_opts(
    title=ui.tags.div(
        {"class": "title-bar"},
        "CaliCast -- Weather in 12 California areas",
        ui.tags.div(
            {"class": "title-buttons"},
            ui.input_action_button("btn1", "Historical"),
            ui.input_action_button("btn2", "Current"),
            ui.input_action_button("btn3", "Future")
        )
    ),
    fillable=True
)

# Include CSS for styling
ui.include_css(app_dir / "styles.css")

with ui.sidebar(open="desktop"):
    @render.ui
    def weather_sidebar():
        # Sort the list: selected location appears first
        sorted_locations = sorted(
            LOCATIONS, key=lambda loc: loc["name"] != selected_location()
        )

        return [
            ui.tags.div(
                {"class": f"weather-bar {'selected' if loc['name'] == selected_location() else ''}",
                 "onclick": f"Shiny.setInputValue('selected_location', '{loc['name']}', {{priority: 'event'}})"},
                ui.tags.div(
                    {"class": "weather-icon"},
                    loc["icon"]  # Using FontAwesome icon
                ),
                ui.tags.span(loc["name"]),
                ui.tags.span(f"↑ {loc['high']}°F  ↓ {loc['low']}°F"),
            )
            for loc in sorted_locations
        ]

# Add main content
ICONS = {
    "user": fa.icon_svg("user", "regular"),
    "wallet": fa.icon_svg("wallet"),
    "currency-dollar": fa.icon_svg("dollar-sign"),
    "ellipsis": fa.icon_svg("ellipsis"),
}

with ui.layout_columns(fill=False):
    with ui.value_box(showcase=ICONS["user"]):
        "Total tippers"

        @render.express
        def total_tippers():
            tips_data().shape[0]

    with ui.value_box(showcase=ICONS["wallet"]):
        "Average tip"

        @render.express
        def average_tip():
            d = tips_data()
            if d.shape[0] > 0:
                perc = d.tip / d.total_bill
                f"{perc.mean():.1%}"

    with ui.value_box(showcase=ICONS["currency-dollar"]):
        "Average bill"

        @render.express
        def average_bill():
            d = tips_data()
            if d.shape[0] > 0:
                bill = d.total_bill.mean()
                f"${bill:.2f}"


with ui.layout_columns(col_widths=[6, 6, 12]):
    with ui.card(full_screen=True):
        ui.card_header("Tips data")

        @render.data_frame
        def table():
            return render.DataGrid(tips_data())

    with ui.card(full_screen=True):
        with ui.card_header(class_="d-flex justify-content-between align-items-center"):
            "Total bill vs tip"
            with ui.popover(title="Add a color variable", placement="top"):
                ICONS["ellipsis"]
                ui.input_radio_buttons(
                    "scatter_color",
                    None,
                    ["none", "sex", "smoker", "day", "time"],
                    inline=True,
                )

        @render_plotly
        def scatterplot():
            color = input.scatter_color()
            return px.scatter(
                tips_data(),
                x="total_bill",
                y="tip",
                color=None if color == "none" else color,
                trendline="lowess",
            )

    with ui.card(full_screen=True):
        with ui.card_header(class_="d-flex justify-content-between align-items-center"):
            "Tip percentages"
            with ui.popover(title="Add a color variable"):
                ICONS["ellipsis"]
                ui.input_radio_buttons(
                    "tip_perc_y",
                    "Split by:",
                    ["sex", "smoker", "day", "time"],
                    selected="day",
                    inline=True,
                )

        @render_plotly
        def tip_perc():
            from ridgeplot import ridgeplot

            dat = tips_data()
            dat["percent"] = dat.tip / dat.total_bill
            yvar = input.tip_perc_y()
            uvals = dat[yvar].unique()

            samples = [[dat.percent[dat[yvar] == val]] for val in uvals]

            plt = ridgeplot(
                samples=samples,
                labels=uvals,
                bandwidth=0.01,
                colorscale="viridis",
                colormode="row-index",
            )

            plt.update_layout(
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5
                )
            )

            return plt


ui.include_css(app_dir / "styles.css")

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------


@reactive.calc
def tips_data():
    bill = input.total_bill()
    idx1 = tips.total_bill.between(bill[0], bill[1])
    idx2 = tips.time.isin(input.time())
    return tips[idx1 & idx2]


@reactive.effect
@reactive.event(input.reset)
def _():
    ui.update_slider("total_bill", value=bill_rng)
    ui.update_checkbox_group("time", selected=["Lunch", "Dinner"])
