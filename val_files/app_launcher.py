from shiny import App, ui, render
import pandas as pd
from plotnine import ggplot, aes, geom_bar, geom_col, labs, theme_minimal, position_dodge,  geom_point, scale_fill_brewer, scale_fill_gradient, geom_tile, geom_line, facet_wrap, scale_x_continuous, theme, element_text
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
from modelfunction import predict_weather_for_locations
from app import app_ui, server


app = App(app_ui, server)