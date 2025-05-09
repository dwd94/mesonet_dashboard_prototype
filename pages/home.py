import dash
from dash import dcc, html, Output, Input, callback
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
import datetime
import os
import json
import plotly.express as px
from PIL import Image
from dash import (
    Dash,
    Input,
    Output,
    Patch,
    State,
    ctx,
    dcc,
    html,
    no_update,
    callback,
)

import dash_bootstrap_components as dbc  # new import for column layout

from figures import figures_main

dash.register_page(__name__, path="/home", name="Home")

# Load dummy data (when available)
try:
    # Check if dummy data directory exists
    dummy_data_path = os.path.join(os.path.dirname(__file__), '../data/dummy_data')
    
    # Try to load provider stats
    stats_path = os.path.join(dummy_data_path, 'provider_stats.json')
    if os.path.exists(stats_path):
        with open(stats_path, 'r') as f:
            provider_stats = json.load(f)
    else:
        provider_stats = None
        
    # Try to load provider data
    deldot_path = os.path.join(dummy_data_path, 'deldot_dummy.parquet')
    deldeos_path = os.path.join(dummy_data_path, 'deldeos_dummy.parquet')
    colorado_path = os.path.join(dummy_data_path, 'colorado_dummy.parquet')
    
    if os.path.exists(deldot_path) and os.path.exists(deldeos_path) and os.path.exists(colorado_path):
        deldot_data = pd.read_parquet(deldot_path)
        deldeos_data = pd.read_parquet(deldeos_path)
        colorado_data = pd.read_parquet(colorado_path)
        
        all_providers_data = pd.concat([deldot_data, deldeos_data, colorado_data])
        has_real_data = True
    else:
        has_real_data = False
except Exception as e:
    print(f"Error loading dummy data: {e}")
    has_real_data = False
    provider_stats = None

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
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Div(
                                                        [
                                                            html.Div(
                                                                "System Status",
                                                                style={
                                                                    "fontWeight": (
                                                                        "bold"
                                                                    )
                                                                },
                                                            ),
                                                            html.Br(),
                                                            html.Div(
                                                                dcc.Dropdown(
                                                                    id="provider-dropdown",
                                                                    options=[
                                                                        {
                                                                            "label": (
                                                                                "DelDOT"
                                                                            ),
                                                                            "value": (
                                                                                "deldot"
                                                                            ),
                                                                        },
                                                                        {
                                                                            "label": (
                                                                                "DelDEOS"
                                                                            ),
                                                                            "value": (
                                                                                "deldeos"
                                                                            ),
                                                                        },
                                                                        {
                                                                            "label": (
                                                                                "Colorado"
                                                                            ),
                                                                            "value": (
                                                                                "colorado"
                                                                            ),
                                                                        },
                                                                        {
                                                                            "label": (
                                                                                "All Providers"
                                                                            ),
                                                                            "value": (
                                                                                "all"
                                                                            ),
                                                                        },
                                                                    ],
                                                                    value="all",
                                                                    clearable=False,
                                                                    style={
                                                                        "margin-bottom": (
                                                                            "10px"
                                                                        )
                                                                    },
                                                                ),
                                                            ),
                                                        ]
                                                    ),
                                                    width=9,
                                                ),
                                                dbc.Col(
                                                    html.Div(
                                                        "Expected Rate",
                                                        style={
                                                            "textAlign": (
                                                                "right"
                                                            ),
                                                            "fontWeight": (
                                                                "italic"
                                                            ),
                                                            "display": "flex",
                                                            "alignItems": (
                                                                "flex-end"
                                                            ),
                                                            "height": "100%",
                                                        },
                                                    ),
                                                    width=3,
                                                ),
                                            ],
                                            style={"margin-bottom": "5px"},
                                        ),
                                        html.Div(
                                            f"Last update: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                                            style={
                                                "fontSize": "12px",
                                                "color": "gray",
                                                "margin-bottom": "10px",
                                            },
                                        ),
                                    ]
                                ),
                                html.Div(id="provider-status-container"),
                            ]
                        ),
                        style={
                            "padding": "20px",
                            "backgroundColor": "#f8f9fa",
                            "borderRadius": "5px",
                            "height": "calc(100vh - 80px)",  # Full height minus navbar
                            "overflowY": "auto",
                        },
                    ),
                    width=3,
                ),
                # Right Main Content Column
                dbc.Col(
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Station Status Map"),
                                                dbc.CardBody(
                                                    [
                                                        dcc.Graph(
                                                            id="map",
                                                            config={"displayModeBar": False},
                                                            style={"height": "40vh"},
                                                        )
                                                    ]
                                                ),
                                            ]
                                        ),
                                        width=12,
                                    ),
                                ]
                            ),
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Temperature Trend"),
                                                dbc.CardBody(
                                                    [
                                                        dcc.Graph(
                                                            id="temperature-chart",
                                                            config={"displayModeBar": False},
                                                            style={"height": "30vh"},
                                                        )
                                                    ]
                                                ),
                                            ]
                                        ),
                                        width=6,
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Data Ingest Rates"),
                                                dbc.CardBody(
                                                    [
                                                        dcc.Graph(
                                                            id="ingest-rate-chart",
                                                            config={"displayModeBar": False},
                                                            style={"height": "30vh"},
                                                        )
                                                    ]
                                                ),
                                            ]
                                        ),
                                        width=6,
                                    ),
                                ]
                            ),
                        ],
                        style={
                            "padding": "20px",
                            "height": "calc(100vh - 80px)",  # Full height minus navbar
                            "overflowY": "auto",
                        },
                    ),
                    width=9,
                ),
            ],
            className="g-0",  # Remove gutters
        )
    ]
)

@callback(
    Output("provider-status-container", "children"),
    Input("provider-dropdown", "value"),
)
def update_provider_status(provider):
    if provider_stats and provider in provider_stats:
        stats = provider_stats[provider]
        
        # Access provider specific data
        total_stations = stats['total_stations']
        active_stations = stats['active_stations']
        avg_temp = stats['avg_temperature']
        avg_humidity = stats['avg_humidity']
        avg_wind = stats['avg_wind_speed']
        readings_per_hour = stats['readings_per_hour']
        
        # Calculate percentage for progress bar
        active_pct = int((active_stations / total_stations) * 100) if total_stations else 0
        latest_readings = readings_per_hour[max(readings_per_hour.keys())] if readings_per_hour else 0
        expected_readings = total_stations  # Simplified assumption
        
        # Determine status color based on percentage
        if active_pct >= 80:
            status_color = "success"
        elif active_pct >= 50:
            status_color = "warning"
        else:
            status_color = "danger"
            
        # Create sparkline data
        hours = list(readings_per_hour.keys())
        values = list(readings_per_hour.values())
    else:
        # Fallback data if provider stats not available
        if provider == "all":
            provider_title = "All Providers"
            active_pct = 85
            status_color = "success"
            latest_readings = 450
            expected_readings = 500
            total_stations = 150
            active_stations = 127
            
            # For the all providers case, create combined average values
            if has_real_data:
                avg_temp = all_providers_data['temperature'].mean()
                avg_humidity = all_providers_data['humidity'].mean()
                avg_wind = all_providers_data['wind_speed'].mean()
            else:
                avg_temp = 22.3
                avg_humidity = 58.7
                avg_wind = 9.2
        else:
            provider_title = provider.capitalize()
            active_pct = 40 if provider == "deldot" else (75 if provider == "deldeos" else 90)
            status_color = "warning" if active_pct < 80 else "success"
            latest_readings = 120 if provider == "deldot" else (180 if provider == "deldeos" else 150)
            expected_readings = 300
            total_stations = 50 if provider == "deldot" else (60 if provider == "deldeos" else 40)
            active_stations = int(total_stations * active_pct / 100)
            
            # Use placeholder values
            avg_temp = 21.5
            avg_humidity = 65.2
            avg_wind = 8.4
        
        # Random sparkline data
        import random
        hours = list(range(24))
        values = [random.randint(50, 200) for _ in range(24)]
    
    # Format provider title
    if provider == "deldot":
        provider_title = "DelDOT"
    elif provider == "deldeos":
        provider_title = "DelDEOS"
    elif provider == "colorado":
        provider_title = provider.capitalize()
    elif provider == "all":
        provider_title = "All Providers"
    else:
        provider_title = provider.capitalize()
        
    # Create sparkline figure
    sparkline_fig = {
        "data": [
            {
                "x": hours,
                "y": values,
                "type": "line",
                "mode": "lines",
                "line": {"width": 1, "color": "#007bff"},
            }
        ],
        "layout": {
            "margin": {"l": 0, "r": 0, "t": 0, "b": 0},
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "height": 30,
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
        },
    }
    
    return html.Div(
        [
            html.Div(provider_title),
            dbc.Row(
                [
                    dbc.Col(  # progress bar
                        dbc.Progress(
                            value=active_pct,
                            color=status_color,
                            striped=True,
                            animated=True,
                            label=f"{active_pct}%",
                        ),
                        width=6,
                    ),
                    dbc.Col(  # sparkline
                        dcc.Graph(
                            figure=sparkline_fig,
                            config={"displayModeBar": False},
                            style={"height": "30px"},
                        ),
                        width=3,
                    ),
                    dbc.Col(  # current rate text
                        html.Div(
                            f"{latest_readings} rec/hr",
                            style={
                                "textAlign": "right",
                                "fontSize": "12px",
                            },
                        ),
                        width=3,
                    ),
                ],
                style={"margin-bottom": "15px"},
            ),
            html.Hr(style={"margin": "10px 0"}),
            
            # Station Stats 
            html.Div("Station Stats", style={"fontWeight": "bold", "marginBottom": "10px"}),
            
            # Create a 2x2 grid of stats
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div("Total Stations", style={"fontSize": "12px", "color": "gray"}),
                            html.Div(f"{total_stations}", style={"fontSize": "16px", "fontWeight": "bold"}),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            html.Div("Active Stations", style={"fontSize": "12px", "color": "gray"}),
                            html.Div(f"{active_stations}", style={"fontSize": "16px", "fontWeight": "bold"}),
                        ],
                        width=6,
                    ),
                ],
                style={"marginBottom": "10px"},
            ),
            
            # More detailed stats from provider_stats if available
            html.Div("Avg. Measurements", style={"fontWeight": "bold", "marginTop": "15px", "marginBottom": "10px"}),
            
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div("Temperature", style={"fontSize": "12px", "color": "gray"}),
                            html.Div(
                                f"{avg_temp:.1f}°C", 
                                style={"fontSize": "16px", "fontWeight": "bold"}
                            ),
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        [
                            html.Div("Humidity", style={"fontSize": "12px", "color": "gray"}),
                            html.Div(
                                f"{avg_humidity:.1f}%", 
                                style={"fontSize": "16px", "fontWeight": "bold"}
                            ),
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        [
                            html.Div("Wind", style={"fontSize": "12px", "color": "gray"}),
                            html.Div(
                                f"{avg_wind:.1f} m/s", 
                                style={"fontSize": "16px", "fontWeight": "bold"}
                            ),
                        ],
                        width=4,
                    ),
                ],
            ),
        ]
    )

@callback(
    Output("map", "figure"),
    Input("provider-dropdown", "value"),
)
def update_map(provider):
    # Use real data if available
    if has_real_data:
        # Filter data for the selected provider
        if provider == "deldot":
            df = deldot_data
        elif provider == "deldeos":
            df = deldeos_data
        elif provider == "colorado":
            df = colorado_data
        elif provider == "all":
            df = all_providers_data
        else:
            df = all_providers_data
        
        # Get the latest reading for each station
        latest_data = df.sort_values('timestamp').groupby('station_id').last().reset_index()
        
        # Create the map with the stations
        fig = px.scatter_mapbox(
            latest_data,
            lat=latest_data['latitude'] if 'latitude' in latest_data.columns else [39.0 + i*0.05 for i in range(len(latest_data))],
            lon=latest_data['longitude'] if 'longitude' in latest_data.columns else [-75.5 + i*0.05 for i in range(len(latest_data))],
            color='provider' if 'provider' in latest_data.columns and provider == 'all' else 'status',
            color_discrete_map={'active': 'green', 'maintenance': 'orange', 'offline': 'red',
                               'deldot': 'blue', 'deldeos': 'green', 'colorado': 'red'},
            hover_name='station_id',
            hover_data=['temperature', 'humidity', 'wind_speed', 'provider'],
            size_max=15,
            zoom=6,
        )
        
        # Update map layout
        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            legend_title_text='Station Status' if provider != 'all' else 'Provider',
        )
        
        return fig
   
@callback(
    Output("temperature-chart", "figure"),
    Input("provider-dropdown", "value"),
)
def update_temperature_chart(provider):
    # Use real data if available
    if has_real_data:
        # Filter data for the selected provider
        if provider == "deldot":
            df = deldot_data
        elif provider == "deldeos":
            df = deldeos_data
        elif provider == "colorado":
            df = colorado_data
        elif provider == "all":
            df = all_providers_data
        else:
            df = all_providers_data
        
        # Group data by timestamp and calculate average temperature
        temp_trend = df.groupby(pd.Grouper(key='timestamp', freq='1H')).agg({
            'temperature': 'mean',
            'station_id': 'count'
        }).reset_index()
        
        # Create temperature trend figure
        fig = go.Figure()
        
        # Add temperature line
        fig.add_trace(
            go.Scatter(
                x=temp_trend['timestamp'],
                y=temp_trend['temperature'],
                mode='lines',
                name='Avg Temperature',
                line=dict(color='#FF9500', width=2),
            )
        )
        
        # Add reading count bars
        fig.add_trace(
            go.Bar(
                x=temp_trend['timestamp'],
                y=temp_trend['station_id'],
                name='Number of Readings',
                marker_color='#007BFF',
                opacity=0.3,
                yaxis='y2',
            )
        )
        
        # Configure layout with dual y-axes
        fig.update_layout(
            xaxis=dict(title=''),
            yaxis=dict(
                title='Temperature (°C)',
                titlefont=dict(color='#FF9500'),
                tickfont=dict(color='#FF9500'),
            ),
            yaxis2=dict(
                title='# of Readings',
                titlefont=dict(color='#007BFF'),
                tickfont=dict(color='#007BFF'),
                overlaying='y',
                side='right',
            ),
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
        )
        
        return fig
    else:
        # Create dummy temperature chart
        dates = pd.date_range(start=datetime.datetime.now() - datetime.timedelta(days=7), periods=168, freq='1H')
        
        # Generate temperature data with day/night pattern
        import numpy as np
        base_temp = 20 + np.random.normal(0, 1, 168)  # Base temperature around 20°C
        hour_of_day = np.array([d.hour for d in dates])
        day_effect = 5 * np.sin(np.pi * (hour_of_day - 6) / 12)  # Peak at noon (hour 12)
        temperatures = base_temp + day_effect
        
        # Random number of readings
        readings = np.random.randint(30, 60, 168)
        
        # Create figure with dual axes
        fig = go.Figure()
        
        # Add temperature line
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=temperatures,
                mode='lines',
                name='Avg Temperature',
                line=dict(color='#FF9500', width=2),
            )
        )
        
        # Add reading count bars
        fig.add_trace(
            go.Bar(
                x=dates,
                y=readings,
                name='Number of Readings',
                marker_color='#007BFF',
                opacity=0.3,
                yaxis='y2',
            )
        )
        
        # Configure layout with dual y-axes
        fig.update_layout(
            xaxis=dict(title=''),
            yaxis=dict(
                title='Temperature (°C)',
                titlefont=dict(color='#FF9500'),
                tickfont=dict(color='#FF9500'),
            ),
            yaxis2=dict(
                title='# of Readings',
                titlefont=dict(color='#007BFF'),
                tickfont=dict(color='#007BFF'),
                overlaying='y',
                side='right',
            ),
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
        )
        
        return fig
   
@callback(
    Output("ingest-rate-chart", "figure"),
    Input("provider-dropdown", "value"),
)
def update_ingest_rate_chart(provider):
    # Use real data if available
    if provider_stats and provider in provider_stats:
        readings_per_hour = provider_stats[provider]['readings_per_hour']
        hours = list(readings_per_hour.keys())
        values = list(readings_per_hour.values())
        
        # Create figure
        fig = go.Figure()
        
        # Add line trace for ingest rate
        fig.add_trace(
            go.Scatter(
                x=hours,
                y=values,
                mode='lines+markers',
                name='Readings per Hour',
                line=dict(color='#17a2b8', width=2),
                fill='tozeroy',
                fillcolor='rgba(23, 162, 184, 0.1)',
            )
        )
        
        # Add a target/expected line
        expected_rate = sum(values) / len(values) * 1.2  # 20% above average as target
        fig.add_trace(
            go.Scatter(
                x=[min(hours), max(hours)],
                y=[expected_rate, expected_rate],
                mode='lines',
                name='Expected Rate',
                line=dict(color='#dc3545', width=2, dash='dash'),
            )
        )
        
        # Configure layout
        fig.update_layout(
            xaxis=dict(
                title='Hour of Day',
                tickmode='array',
                tickvals=list(range(0, 24, 4)),
                ticktext=[f"{h:02d}:00" for h in range(0, 24, 4)],
            ),
            yaxis=dict(
                title='Readings / Hour',
            ),
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
        )
        
        return fig
    else:
        # Create appropriate ingest rate chart based on provider
        hours = list(range(24))
        
        # Create a pattern of ingest rates with higher during day, lower at night
        base_rate = 100
        if provider == "deldot":
            base_rate = 120
        elif provider == "deldeos":
            base_rate = 150
        elif provider == "colorado":
            base_rate = 100
        elif provider == "all":
            base_rate = 370  # Combined rate for all providers
            
        # Generate data with day/night pattern
        import numpy as np
        hour_effect = np.sin(np.pi * (np.array(hours) - 6) / 12)  # Peak at noon
        values = base_rate + 50 * hour_effect + np.random.normal(0, 10, 24)
        values = np.maximum(values, 0)  # Ensure no negative values
        
        # If we have actual data for all providers, use it
        if has_real_data and provider == "all":
            # Try to calculate real readings per hour
            try:
                last_day = all_providers_data[all_providers_data['timestamp'] >= (datetime.datetime.now() - datetime.timedelta(days=1))]
                real_readings = last_day.groupby(last_day['timestamp'].dt.hour).size()
                if not real_readings.empty:
                    hours = list(real_readings.index)
                    values = list(real_readings.values)
            except Exception as e:
                print(f"Error calculating real readings: {e}")
        
        # Create figure
        fig = go.Figure()
        
        # Add line trace for ingest rate
        fig.add_trace(
            go.Scatter(
                x=hours,
                y=values,
                mode='lines+markers',
                name='Readings per Hour',
                line=dict(color='#17a2b8', width=2),
                fill='tozeroy',
                fillcolor='rgba(23, 162, 184, 0.1)',
            )
        )
        
        # Add a target/expected line
        target_rate = base_rate * 1.2  # 20% above base rate
        fig.add_trace(
            go.Scatter(
                x=[0, 23],
                y=[target_rate, target_rate],
                mode='lines',
                name='Expected Rate',
                line=dict(color='#dc3545', width=2, dash='dash'),
            )
        )
        
        # Configure layout
        fig.update_layout(
            xaxis=dict(
                title='Hour of Day',
                tickmode='array',
                tickvals=list(range(0, 24, 4)),
                ticktext=[f"{h:02d}:00" for h in range(0, 24, 4)],
            ),
            yaxis=dict(
                title='Readings / Hour',
            ),
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
        )
        
        return fig
   