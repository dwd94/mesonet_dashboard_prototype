import dash
from dash import dcc, html, Output, Input
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
import datetime
import os

from PIL import Image
from dash import Dash, Input, Output, Patch, State, ctx, dcc, html, no_update, callback

import json
import dash_bootstrap_components as dbc  # new import for column layout

from figures import figures_main

dash.register_page(__name__, path="/", name="Home")
#data = DataLoader(data_dir="./data")


# Updated layout with two columns: a left sidebar and a right main content area
layout = html.Div(
    [
        dbc.Row(
            [
                # Left Sidebar Column
                dbc.Col(
                    html.Div(
                        dcc.Loading(
                            children=[
                                html.Div([
                                    dbc.Row([
                                        dbc.Col(
                                            html.Div([
                                                html.Div("System Status", style={"fontWeight": "bold"}),
                                                html.Div(
                                                    dcc.Dropdown(
                                                        id="provider-dropdown",
                                                        options=[
                                                            {"label": "Provider 1", "value": "provider_1"},
                                                            {"label": "Provider 2", "value": "provider_2"},
                                                        ],
                                                        value="provider_1",
                                                        clearable=False,
                                                        style={"margin-bottom": "10px"}
                                                    ),
                                                ),
                                            ]),
                                            width=9
                                        ),
                                        dbc.Col(html.Div("Expected Rate", style={"textAlign": "right", "fontWeight": "italic"}), width=3),
                                    ], style={"margin-bottom": "5px"}),
                                    html.Div(f"Last update: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                                             style={"fontSize": "12px", "color": "gray", "margin-bottom": "10px"})
                                ]),
                                html.Div([
                                    html.Div("Provider 1"),
                                    dbc.Row([
                                        dbc.Col(dbc.Progress(value=40, striped=True, animated=True, label="40%"), width=9),
                                        dbc.Col(html.Div("120 rec/hr", style={"textAlign": "right"}), width=3),
                                    ], style={"margin-bottom": "10px"}),
                                    html.Div("Provider 2"),
                                    dbc.Row([
                                        dbc.Col(dbc.Progress(value=70, striped=True, animated=True, label="70%"), width=9),
                                        dbc.Col(html.Div("220 rec/hr", style={"textAlign": "right"}), width=3),
                                    ], style={"margin-bottom": "10px"}),
                                    html.Div("Provider 3"),
                                    dbc.Row([
                                        dbc.Col(dbc.Progress(value=20, striped=True, animated=True, label="20%"), width=9),
                                        dbc.Col(html.Div("80 rec/hr", style={"textAlign": "right"}), width=3),
                                    ], style={"margin-bottom": "10px"}),
                                    html.Div("Provider 4"),
                                    dbc.Row([
                                        dbc.Col(dbc.Progress(value=100, striped=True, animated=True, label="100%"), width=9),
                                        dbc.Col(html.Div("300 rec/hr", style={"textAlign": "right"}), width=3),
                                    ], style={"margin-bottom": "10px"}),
                                ])
                            ],
                            style={"height": "100vh", "overflow-y": "auto", "padding": "10px"},
                        ),
                        style={
                            "padding": "15px",
                            "margin": "10px",
                            "background-color": "white",
                            "border-radius": "5px",
                            "box-shadow": "0 0 5px rgba(0,0,0,0.1)",
                        },
                    ),
                    lg=4,
                    className="ml-3 mt-0",
                ),
                # Right Main Content Column
                dbc.Col(
                    html.Div(
                        [
                            dcc.Loading(
                                id="loading-spinner-map",
                                delay_show=100,
                                type="default",
                                children=[
                                    dcc.Dropdown(
                                        id="provider-dropdown",
                                        options=[
                                            {"label": "Provider 1", "value": "provider_1"},
                                            {"label": "Provider 2", "value": "provider_2"},
                                        ],
                                        value="provider_1",
                                        style={"display": "none"}
                                    ),
                                    dcc.Graph(
                                        id="map",
                                        #style={"height": "40vh"},
                                        config={
                                            "displaylogo": False,
                                            "scrollZoom": True,
                                        },
                                    ),
                                ],
                            ),
                        ],
                        style={
                            "overflow-y": "scroll",
                            "height": "auto",
                            #"box-shadow": "-4px -4px 10px 6px rgba(0, 0, 0, 0.1)",
                            # "border-top-left-radius": "10px",
                            # "border-top-right-radius": "10px",
                        },
                    ),
                    className="mr-3",
                ),
            ]
        ),
    ]
)


# Callback to update map based on selected column
@callback(
    Output("map", "figure"),
    Input("provider-dropdown", "value"),
)
def map(provider):
    """
    Map.
    """
    return figures_main.map()