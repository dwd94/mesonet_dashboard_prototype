import dash
from dash import dcc, html, Output, Input, callback
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
import datetime
import os
import json
import plotly.express as px
import numpy as np
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
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/providers", name="Providers")

# Load provider data from Excel
excel_path = os.path.join(os.path.dirname(__file__), '../data/dummy_data/Mesonet Vendor Info.xlsx')

# Print available sheet names
xl = pd.ExcelFile(excel_path)
print("Available sheets:", xl.sheet_names)

# Try to find the correct sheet name
sheet_name = 'Sheet 1'  # Use the specific dashboard metadata sheet
if sheet_name not in xl.sheet_names:
    sheet_name = next((s for s in xl.sheet_names if 'vendor' in s.lower()), None)
    if sheet_name is None:
        sheet_name = xl.sheet_names[0]  # Use the first sheet if no matching sheet found
print(f"Using sheet: {sheet_name}")

vendor_df = pd.read_excel(excel_path, sheet_name=sheet_name)
print("Available columns:", vendor_df.columns.tolist())

# exit()
# Convert provider data to list of dictionaries
providers = []
for _, row in vendor_df.iterrows():
    try:
        # provider = {
        #     "name": str(row.get('Vendor Name', row.get('Provider Name', 'Unknown'))),
        #     "color": str(row.get('Color', '#1f77b4')),  # Default color if not specified
        #     "lat": float(row.get('Latitude', 0)),
        #     "lon": float(row.get('Longitude', 0)),
        #     "frequency": float(row.get('Frequency', 24)),  # Default frequency if not specified
        #     "status": str(row.get('Status', 'Active'))  # Default status if not specified
        # }
        # print(row)
        provider = {
            "name": str(row.get('Unnamed: 1', 'Unknown')),                  # Vendor/Provider Name
            "color": str(row.get('Color', '#1f77b4')),                      # Default color (not present in your columns, fallback assumed)
            "lat": float(row.get('Unnamed: 5', 0)),                         # Latitude
            "lon": float(row.get('Unnamed: 6', 0)),                         # Longitude
            "frequency": float(row.get('Unnamed: 4', 0)),                  # Frequency (not mapped in your columns, fallback assumed)
            "status": str(row.get('Status', 'Active')),                    # Status (not mapped in your columns, fallback assumed)
            "station_count": int(row.get('Total Station Count', 0))                 # Total Station Count
        }
        providers.append(provider)
    except Exception as e:
        # print(f"Error processing row: {row}")
        # print(f"Error: {e}")
        pass

print(f"Loaded {len(providers)} providers")

def create_provider_mini_graph(provider_name):
    # Create dummy data for the mini graph
    dates = pd.date_range(end=datetime.datetime.now(), periods=24, freq='h')
    values = [20 + 5 * np.sin(i/3) for i in range(24)]
    df = pd.DataFrame({'timestamp': dates, 'value': values})
    
    provider_color = next((p["color"] for p in providers if p["name"] == provider_name), '#1f77b4')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['value'],
        mode='lines',
        line=dict(width=2, color=provider_color),
        showlegend=False
    ))
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=30,  # Reduced height
        width=100,  # Added width
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False)
    )
    
    return fig

def create_provider_card(provider):
    # Calculate progress percentage (using station count as an example)
    max_stations = max(p['station_count'] for p in providers)
    progress = (provider['station_count'] / max_stations) * 100 if max_stations > 0 else 10
    if progress == 0.0:
        progress = 5
    station_count = provider['station_count']
    if station_count >= 100:
        marker_color = 'green'
        traffic_light = "🟢"
    elif station_count >= 50:
        marker_color = 'yellow'
        traffic_light = "🟡"
    else:
        marker_color = 'pink'
        traffic_light = "🔴"
    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                # Provider Name and Traffic Signal
                dbc.Col(html.H6(provider["name"], style={"marginBottom": "5px"}), width=10),
                dbc.Col(html.Div(traffic_light, style={"fontSize": "1.2rem", "textAlign": "right"}), width=2),
            ]),
            dbc.Row([
                # Progress Bar with percentage text
                dbc.Col([
                    html.Div([
                        dbc.Progress(
                            value=progress,
                            color=marker_color,
                            style={"height": "10px", "marginBottom": "5px", "width": "100%"}
                        ),
                        html.Span(
                            f"{progress:.1f}%", 
                            style={"fontSize": "0.8rem", "display": "block", "textAlign": "right"}
                        ),
                    ]),
                    # Line Graph in same column
                    html.Div([
                        dcc.Graph(
                            figure=create_provider_mini_graph(provider["name"]),
                            config={"displayModeBar": False},
                            style={"height": "30px", "width": "100%", "marginTop": "5px"}
                        ),
                        html.Div(
                            f"{provider['frequency']:.1f}/h",
                            style={"textAlign": "right", "fontSize": "0.8rem", "marginTop": "2px"}
                        )
                    ])
                ], width=12),
            ]),
        ]),
        style={"marginBottom": "10px", "padding": "10px"}
    )

# Layout
layout = html.Div([
    # Left sidebar toggle button
    html.Div([
        dbc.Button(
            html.I(className="fas fa-chevron-left", id="sidebar-icon"),
            id="sidebar-toggle",
            color="primary",
            size="sm",
            style={
                "position": "fixed", 
                "top": "95px", 
                "left": "10px", 
                "zIndex": "1000",
                "borderRadius": "0 4px 4px 0",
                "paddingLeft": "8px",
                "paddingRight": "8px",
                "boxShadow": "2px 2px 4px rgba(0, 0, 0, 0.2)"
            },
        ),
    ]),
    
    # Right legend toggle button
    html.Div([
        dbc.Button(
            html.I(className="fas fa-chevron-right", id="legend-icon"),
            id="legend-toggle",
            color="primary",
            size="sm",
            style={
                "position": "fixed", 
                "top": "95px", 
                "right": "10px", 
                "zIndex": "1000",
                "borderRadius": "4px 0 0 4px",
                "paddingLeft": "8px",
                "paddingRight": "8px",
                "boxShadow": "2px 2px 4px rgba(0, 0, 0, 0.2)"
            },
        ),
    ]),
    
    dbc.Row([
        # Left Sidebar (Providers list)
        dbc.Col([
            html.Div([
                html.Div([
                    html.H4("Providers", style={"marginBottom": "20px"}),
                    html.Div([
                        create_provider_card(provider) for provider in providers
                    ])
                ], style={
                    "padding": "20px",
                    "backgroundColor": "#f8f9fa",
                    "borderRadius": "5px",
                    "height": "calc(100vh - 80px)",
                    "overflowY": "auto"
                })
            ], id="sidebar-content")
        ], id="sidebar-column", width=4, style={"transition": "all 0.3s ease-in-out"}),
        
        # Main Content (Map)
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Provider Locations"),
                dbc.CardBody([
                    dcc.Graph(
                        id="provider-map",
                        config={"displayModeBar": False},
                        style={"height": "calc(100vh - 120px)"}
                    )
                ])
            ])
        ], id="map-column", width=8, style={"transition": "all 0.3s ease-in-out"})
    ])
])

# Add sidebar toggle callback
@callback(
    [Output("sidebar-column", "width"),
     Output("sidebar-column", "style"),
     Output("map-column", "width"),
     Output("sidebar-icon", "className")],
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar-column", "width"),
     State("sidebar-column", "style")]
)
def toggle_sidebar(n_clicks, current_width, current_style):
    if n_clicks is None:
        # Initial load - sidebar is visible
        return 4, {"transition": "all 0.3s ease-in-out"}, 8, "fas fa-chevron-left"
    
    if current_width == 4:
        # Collapse sidebar
        style = current_style or {}
        style.update({"display": "none", "transition": "all 0.3s ease-in-out"})
        return 0, style, 12, "fas fa-chevron-right"
    else:
        # Expand sidebar
        style = current_style or {}
        style.update({"display": "block", "transition": "all 0.3s ease-in-out"})
        return 4, style, 8, "fas fa-chevron-left"

# Add legend toggle callback
@callback(
    Output("provider-map", "figure"),
    [Input("provider-map", "id"),
     Input("legend-toggle", "n_clicks")],
    [State("provider-map", "figure")]
)
def update_map(_, n_clicks, current_figure):
    # Get the trigger
    triggered_id = ctx.triggered_id if ctx.triggered else None
    
    fig = go.Figure()
    show_legend = True
    
    # If the legend toggle was clicked, toggle the legend visibility
    if triggered_id == "legend-toggle" and current_figure:
        # Toggle the legend visibility
        show_legend = not current_figure.get('layout', {}).get('showlegend', True)
        
        # If we have the existing figure, just update the legend visibility
        if current_figure:
            fig = go.Figure(current_figure)
            fig.update_layout(showlegend=show_legend)
            return fig
    
    # Calculate center of all provider locations
    lats = [p["lat"] for p in providers]
    lons = [p["lon"] for p in providers]
    center_lat = sum(lats) / len(lats) if lats else 39.0
    center_lon = sum(lons) / len(lons) if lons else -95.0
    
    # Add map background
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox=dict(
            center=dict(lat=center_lat, lon=center_lon),
            zoom=5  # Increased zoom level
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=show_legend,  # Control legend visibility
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="rgba(0, 0, 0, 0.2)",
            borderwidth=1
        )
    )
    
    # Add provider markers
    for provider in providers:
        station_count = provider['station_count']
        if station_count >= 100:
            marker_color = 'green'
        elif station_count >= 50:
            marker_color = 'yellow'
        else:
            marker_color = 'pink'
            
        fig.add_trace(go.Scattermapbox(
            lat=[provider["lat"]],
            lon=[provider["lon"]],
            mode='markers+text',
            marker=go.scattermapbox.Marker(
                size=35,
                color=marker_color,
                opacity=0.8,
                # symbol='marker'  # This creates a pin-like marker
            ),
            text=[f"{station_count}"],
            textposition="middle center",
            textfont=dict(
                size=12,
                color='black'
            ),
            name=provider["name"],
            showlegend=True,
            hovertext=[f"{provider['name']}<br>Status: {provider['status']}<br>Expected Record Counts/HR: {provider['frequency']}/h<br>Stations: {station_count}"],
            hoverinfo='text'
        ))
    
    return fig

# Update legend toggle icon
@callback(
    Output("legend-icon", "className"),
    [Input("provider-map", "figure")]
)
def update_legend_icon(figure):
    # Check if the legend is visible
    if figure and figure.get('layout', {}).get('showlegend', True):
        return "fas fa-chevron-right"
    else:
        return "fas fa-chevron-left" 