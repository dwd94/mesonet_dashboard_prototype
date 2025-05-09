import dash
from dash import dcc, html, Output, Input, callback
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
import os

# Register the page
dash.register_page(__name__, path="/category", name="Category Status")

# Dummy data for categories
categories = [
    {
        "name": "Ground Stations",
        "expected": 9830,
        "actual": 9720,
        "lat": 39.5,
        "lon": -98.35,
    },
    {
        "name": "Fixed Buoys",
        "expected": 75,
        "actual": 70,
        "lat": 29.5,
        "lon": -89.5,
    },
    {
        "name": "Drift Buoys",
        "expected": 95,
        "actual": 80,
        "lat": 36.5,
        "lon": -75.5,
    },
    {
        "name": "Balloons",
        "expected": 200,
        "actual": 200,
        "lat": 32.5,
        "lon": -100.0,
    },
    {
        "name": "ABO",
        "expected": 25,
        "actual": 25,
        "lat": 34.0,
        "lon": -118.0,
    },
    {
        "name": "Dropsondes",
        "expected": 36,
        "actual": 36,
        "lat": 40.0,
        "lon": -74.0,
    },
]

# Calculate percentages and color
for cat in categories:
    cat["percent"] = 100 * cat["actual"] / cat["expected"] if cat["expected"] else 0
    if cat["percent"] >= 98:
        cat["color"] = "#6cc26c"  # green
    elif cat["percent"] >= 90:
        cat["color"] = "#ffe135"  # yellow
    else:
        cat["color"] = "#e74c3c"  # red

# Dummy system stats
total_expected = sum(c["expected"] for c in categories)
total_actual = sum(c["actual"] for c in categories)
total_percent = 100 * total_actual / total_expected if total_expected else 0
latency = 4.3

# Traffic light component (vertical, all three lights)
def traffic_light_component(status):
    colors = {
        'red':   '#e74c3c',
        'yellow': '#ffe135',
        'green': '#6cc26c'
    }
    active = {
        'red':   0.3,
        'yellow': 0.3,
        'green': 0.3
    }
    if status == 'green':
        active['green'] = 1
    elif status == 'yellow':
        active['yellow'] = 1
    else:
        active['red'] = 1
    return html.Div([
        html.Div(style={
            "width": "32px", "height": "32px", "borderRadius": "50%", "backgroundColor": colors['red'],
            "opacity": active['red'], "margin": "0 auto 6px auto", "border": "2px solid #888"
        }),
        html.Div(style={
            "width": "32px", "height": "32px", "borderRadius": "50%", "backgroundColor": colors['yellow'],
            "opacity": active['yellow'], "margin": "0 auto 6px auto", "border": "2px solid #888"
        }),
        html.Div(style={
            "width": "32px", "height": "32px", "borderRadius": "50%", "backgroundColor": colors['green'],
            "opacity": active['green'], "margin": "0 auto", "border": "2px solid #888"
        })
    ], style={"display": "flex", "flexDirection": "column", "alignItems": "center", "marginBottom": "18px"})

# Determine traffic light status
if total_percent >= 98:
    traffic_status = 'green'
elif total_percent >= 90:
    traffic_status = 'yellow'
else:
    traffic_status = 'red'

# Sidebar table with progress bars under each row
sidebar = html.Div([
    # Full traffic light at the top
    traffic_light_component(traffic_status),
    dbc.Table([
        html.Thead(html.Tr([
            html.Th(""),
            html.Th("Expected Recs/Hrs"),
            html.Th("Records Last Hour"),
            html.Th("%", style={"width": "80px"})
        ])),
        html.Tbody([
            html.Tr([
                html.Td("Total System", style={"fontWeight": "bold"}),
                html.Td(f"{total_expected:,}", style={"fontWeight": "bold"}),
                html.Td(f"{total_actual:,}", style={"fontWeight": "bold"}),
                html.Td(
                    html.Div(
                        dbc.Progress(
                            value=total_percent,
                            color="success" if total_percent >= 98 else ("warning" if total_percent >= 90 else "danger"),
                            style={"height": "15px", "width": "100%"},
                            children=f"{total_percent:.2f}%"
                        ),
                        style={"display": "flex", "alignItems": "center", "height": "100%", "padding": "2px 0"}
                    )
                )
            ]),
            *[
                html.Tr([
                    html.Td(cat["name"]),
                    html.Td(f"{cat['expected']:,}"),
                    html.Td(f"{cat['actual']:,}"),
                    html.Td(
                        html.Div(
                            dbc.Progress(
                                value=cat["percent"],
                                color="success" if cat["percent"] >= 98 else ("warning" if cat["percent"] >= 90 else "danger"),
                                style={"height": "20px", "width": "100%", "backgroundColor": cat["color"]},
                                children=f"{cat['percent']:.2f}%"
                            ),
                            style={"display": "flex", "alignItems": "center", "height": "100%", "padding": "2px 0"}
                        )
                    )
                ]) for cat in categories
            ]
        ])
    ], bordered=False, hover=True, responsive=True, size="sm"),
], style={
    "flex": "1 1 350px",
    "backgroundColor": "#f8f9fa",
    "borderRadius": "5px",
    "padding": "30px 10px 10px 10px",
    "minWidth": "320px",
    "maxWidth": "420px",
    "height": "100%",
    "overflowY": "auto",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.04)"
})

# Map
map_fig = go.Figure()
map_fig.update_layout(
    mapbox_style="carto-positron",
    mapbox=dict(
        center=dict(lat=39.5, lon=-98.35),
        zoom=3.5
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    showlegend=False,
    autosize=True,
    height=None,
)
for cat in categories:
    map_fig.add_trace(go.Scattermapbox(
        lat=[cat["lat"]],
        lon=[cat["lon"]],
        mode="markers",
        marker=go.scattermapbox.Marker(
            size=25,
            color=cat["color"],
            opacity=0.9
        ),
        text=[cat["name"]],
        hovertext=[f"{cat['name']}<br>Expected: {cat['expected']}<br>Actual: {cat['actual']}<br>Percent: {cat['percent']:.2f}%"],
        hoverinfo="text"
    ))

map_div = html.Div([
    dcc.Graph(
        id="category-map",
        figure=map_fig,
        config={"displayModeBar": False},
        style={"height": "100%", "width": "100%"}
    )
], style={"flex": "2 1 700px", "display": "flex", "flexDirection": "column", "minWidth": "400px", "height": "100%", "marginLeft": "20px"})

# Right panel (system stats)
right_panel = html.Div([
    html.Div([
        html.H6("Ingested", style={"display": "inline-block", "marginRight": "10px"}),
        html.Span(f"{total_actual:,}", style={"fontWeight": "bold"}),
        html.H6("Exported", style={"display": "inline-block", "marginLeft": "30px", "marginRight": "10px"}),
        html.Span(f"{total_actual:,}", style={"fontWeight": "bold"}),
    ], style={"marginBottom": "10px"}),
    dbc.Progress(
        value=100,
        color="success",
        style={"height": "15px", "marginBottom": "10px"},
        children="100.00%"
    ),
    html.Div([
        html.Span("Latency:", style={"marginRight": "10px"}),
        html.Span(f"{latency} Seconds", style={"fontWeight": "bold"})
    ])
], style={"flex": "1 1 220px", "display": "flex", "flexDirection": "column", "padding": "10px", "minWidth": "180px", "height": "100%"})

# Layout
layout = html.Div([
    html.Div([
        sidebar,
        map_div,
        right_panel
    ], style={
        "display": "flex",
        "justifyContent": "flex-start",
        "alignItems": "stretch",
        "gap": "10px",
        "height": "calc(100vh - 20px)",
        "width": "100%"
    })
], style={"background": "#fff", "padding": "20px 0 0 0", "height": "100vh", "width": "100vw", "overflow": "hidden"}) 