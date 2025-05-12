import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Generate sample data for providers
def generate_provider_data():
    providers = [
        {"name": "NOAA", "status": "high", "availability": 99.8, "records": 45280},
        {"name": "ASOS", "status": "high", "availability": 99.5, "records": 32150},
        {"name": "NWS", "status": "medium", "availability": 95.2, "records": 28970},
        {"name": "MADIS", "status": "high", "availability": 98.7, "records": 36420},
        {"name": "NSSL", "status": "high", "availability": 99.1, "records": 18640},
        {"name": "OK Mesonet", "status": "low", "availability": 86.3, "records": 15280},
        {"name": "USGS", "status": "medium", "availability": 94.8, "records": 8750},
        {"name": "FAA", "status": "high", "availability": 97.9, "records": 12340},
    ]
    
    # Sort by availability (highest first)
    providers.sort(key=lambda x: x["availability"], reverse=True)
    
    return providers

providers = generate_provider_data()

# Status colors
status_colors = {
    "high": "#6cc26c",  # green
    "medium": "#ffe135",  # yellow
    "low": "#ff9dbf"  # pink (instead of red)
}

# Create a bar chart for provider availability
def create_availability_chart(provider_data):
    df = pd.DataFrame(provider_data)
    
    fig = px.bar(
        df,
        x="name",
        y="availability",
        color="status",
        color_discrete_map=status_colors,
        text=df["availability"].apply(lambda x: f"{x:.1f}%"),
        labels={"name": "Provider", "availability": "Availability (%)"},
        height=380,
    )
    
    fig.update_layout(
        title="Provider Availability (%)",
        plot_bgcolor="rgba(0,0,0,0.02)",
        paper_bgcolor="white",
        margin=dict(l=40, r=20, t=60, b=80),
        yaxis=dict(
            range=[80, 100],
            gridcolor="rgba(0,0,0,0.1)",
        ),
        xaxis=dict(
            categoryorder="total descending",
            tickangle=-45,
        ),
        legend_title="Status",
    )
    
    fig.update_traces(
        textposition="outside",
        textfont=dict(size=12),
        marker_line_width=1,
        marker_line_color="white",
    )
    
    return fig

# Create a gauge chart showing overall system status
def create_gauge_chart():
    # Calculate average availability
    avg_availability = np.mean([p["availability"] for p in providers])
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_availability,
        title={"text": "Overall System Status"},
        gauge={
            "axis": {"range": [80, 100], "tickwidth": 1, "tickcolor": "darkblue"},
            "bar": {"color": "#6cc26c" if avg_availability >= 98 else 
                   "#ffe135" if avg_availability >= 90 else "#ff9dbf"},
            "steps": [
                {"range": [80, 90], "color": "rgba(255, 157, 191, 0.3)"},  # pink
                {"range": [90, 98], "color": "rgba(255, 225, 53, 0.3)"},  # yellow
                {"range": [98, 100], "color": "rgba(108, 194, 108, 0.3)"}  # green
            ],
            "threshold": {
                "line": {"color": "black", "width": 2},
                "thickness": 0.75,
                "value": 98
            }
        }
    ))
    
    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
    )
    
    return fig

# Create a table showing provider details
def create_provider_table(provider_data):
    return dbc.Table(
        [
            html.Thead(
                html.Tr([
                    html.Th("Provider"),
                    html.Th("Status"),
                    html.Th("Availability"),
                    html.Th("Records/Hour"),
                ])
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(
                                html.Div(
                                    [
                                        html.Span(
                                            p["name"],
                                            style={"fontWeight": "bold" if p["status"] == "high" else "normal"},
                                        )
                                    ]
                                )
                            ),
                            html.Td(
                                html.Span(
                                    p["status"].upper(),
                                    style={
                                        "color": "white",
                                        "backgroundColor": status_colors[p["status"]],
                                        "padding": "2px 8px",
                                        "borderRadius": "12px",
                                        "fontSize": "0.7rem",
                                        "fontWeight": "bold",
                                    },
                                )
                            ),
                            html.Td(f"{p['availability']:.1f}%"),
                            html.Td(f"{p['records']:,}"),
                        ]
                    )
                    for p in provider_data
                ]
            ),
        ],
        bordered=False,
        hover=True,
        responsive=True,
        striped=True,
        size="sm",
        className="mt-3",
    )

# Statistics calculation
total_records = sum(p["records"] for p in providers)
total_providers = len(providers)
healthy_providers = sum(1 for p in providers if p["status"] == "high")
warning_providers = sum(1 for p in providers if p["status"] == "medium")
critical_providers = sum(1 for p in providers if p["status"] == "low")

# Create layout
layout = html.Div(
    [
        # Title row
        dbc.Row(
            [
                dbc.Col(html.H4("Provider Dashboard", className="mb-4"), width={"size": 6, "order": 1}),
                dbc.Col(
                    dbc.Button(
                        [html.I(className="fas fa-sync-alt me-2"), "Refresh Data"],
                        color="primary",
                        className="float-end",
                    ),
                    width={"size": 6, "order": 2},
                    className="d-flex justify-content-end align-items-center",
                ),
            ],
            className="mb-4",
        ),
        
        # Stats cards row
        dbc.Row(
            [
                # Total Providers card
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("Total Providers", className="card-subtitle text-muted"),
                                html.H3(total_providers, className="mt-2 mb-3"),
                                html.Div(
                                    [
                                        html.Span("Active", className="text-success me-2 fw-bold"),
                                        html.Span(f"{healthy_providers} of {total_providers}")
                                    ],
                                    className="small"
                                )
                            ]
                        ),
                        className="shadow-sm h-100",
                    ),
                    md=3,
                    sm=6,
                ),
                
                # Provider Status card
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("Provider Status", className="card-subtitle text-muted"),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Span(
                                                    f"{healthy_providers}",
                                                    style={"fontSize": "1.5rem", "fontWeight": "bold", "color": status_colors["high"]},
                                                ),
                                                html.Span(" Healthy", className="text-muted ms-2"),
                                            ],
                                            className="mt-2 mb-1",
                                        ),
                                        html.Div(
                                            [
                                                html.Span(
                                                    f"{warning_providers}",
                                                    style={"fontSize": "1.5rem", "fontWeight": "bold", "color": status_colors["medium"]},
                                                ),
                                                html.Span(" Warning", className="text-muted ms-2"),
                                            ],
                                            className="mb-1",
                                        ),
                                        html.Div(
                                            [
                                                html.Span(
                                                    f"{critical_providers}",
                                                    style={"fontSize": "1.5rem", "fontWeight": "bold", "color": status_colors["low"]},
                                                ),
                                                html.Span(" Critical", className="text-muted ms-2"),
                                            ],
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        className="shadow-sm h-100",
                    ),
                    md=3,
                    sm=6,
                ),
                
                # Data Ingestion card
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("Data Ingestion", className="card-subtitle text-muted"),
                                html.H3(
                                    [
                                        f"{total_records:,}",
                                        html.Span(
                                            " records/hr",
                                            style={"fontSize": "1rem", "fontWeight": "normal", "color": "#6c757d"},
                                        ),
                                    ],
                                    className="mt-2 mb-2",
                                ),
                                dbc.Progress(
                                    value=95,
                                    color="success",
                                    style={"height": "8px"},
                                    className="mb-2"
                                ),
                                html.Div("95% of expected volume", className="small text-muted text-end"),
                            ]
                        ),
                        className="shadow-sm h-100",
                    ),
                    md=3,
                    sm=6,
                ),
                
                # Last Update card
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("Latest Update", className="card-subtitle text-muted"),
                                html.H3("2 mins ago", className="mt-2 mb-3"),
                                html.Div(
                                    [
                                        html.I(className="fas fa-check-circle text-success me-2"),
                                        html.Span("All systems operational", className="small"),
                                    ]
                                ),
                            ]
                        ),
                        className="shadow-sm h-100",
                    ),
                    md=3,
                    sm=6,
                ),
            ],
            className="mb-4 g-3",
        ),
        
        # Main content row
        dbc.Row(
            [
                # Left column - Provider Table
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Provider Details", className="fw-bold"),
                            dbc.CardBody(
                                [
                                    create_provider_table(providers),
                                ]
                            ),
                        ],
                        className="shadow-sm",
                    ),
                    md=5,
                    className="mb-4",
                ),
                
                # Right column - Charts
                dbc.Col(
                    [
                        # Gauge chart
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dcc.Graph(
                                            figure=create_gauge_chart(),
                                            config={"displayModeBar": False},
                                        )
                                    ],
                                    className="p-2",
                                )
                            ],
                            className="shadow-sm mb-4",
                        ),
                        
                        # Bar chart
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dcc.Graph(
                                            figure=create_availability_chart(providers),
                                            config={"displayModeBar": False},
                                        )
                                    ],
                                    className="p-2",
                                )
                            ],
                            className="shadow-sm",
                        ),
                    ],
                    md=7,
                ),
            ],
            className="g-3",
        ),
    ],
    style={"padding": "20px"},
) 