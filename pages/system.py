import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Generate example data
def generate_metrics():
    return {
        "cpu_usage": np.random.randint(60, 85),
        "memory_usage": np.random.randint(65, 90),
        "storage_usage": np.random.randint(50, 75),
        "network_in": np.random.randint(40, 120),  # Mbps
        "network_out": np.random.randint(20, 80),  # Mbps
        "active_users": np.random.randint(15, 45),
        "active_processes": np.random.randint(50, 150),
        "system_temp": np.random.randint(65, 80),  # °F
        "uptime": "12 days, 5 hours, 32 minutes",
        "last_restart": (datetime.now() - timedelta(days=12, hours=5, minutes=32)).strftime("%Y-%m-%d %H:%M")
    }

# Generate time series data for system performance
def generate_time_series():
    base = datetime.now()
    dates = [base - timedelta(minutes=i*10) for i in range(24)]
    dates.reverse()
    
    cpu_trend = [np.random.randint(60, 85) for _ in range(24)]
    memory_trend = [np.random.randint(65, 90) for _ in range(24)]
    network_trend = [np.random.randint(40, 120) for _ in range(24)]
    
    return pd.DataFrame({
        'timestamp': dates,
        'cpu_usage': cpu_trend,
        'memory_usage': memory_trend,
        'network_usage': network_trend
    })

# Generate example server status data
def generate_server_status():
    servers = ["App Server 1", "App Server 2", "Database Server", "Cache Server", "File Server"]
    statuses = ["Operational", "Operational", "Operational", "Operational", "Operational"]
    
    # Make one server have an issue randomly
    if np.random.random() < 0.2:  # 20% chance of an issue
        random_idx = np.random.randint(0, len(servers))
        statuses[random_idx] = np.random.choice(["Warning", "Critical"])
    
    return pd.DataFrame({
        'server': servers,
        'status': statuses,
        'load': [np.random.randint(20, 90) for _ in range(len(servers))]
    })

# Get metrics
metrics = generate_metrics()
time_series_data = generate_time_series()
server_status = generate_server_status()

# Create performance chart
def create_performance_chart(df):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['cpu_usage'],
        name='CPU Usage (%)',
        line=dict(color='#0D6EFD', width=2),
        hovertemplate='%{y}%<extra>CPU</extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['memory_usage'],
        name='Memory Usage (%)',
        line=dict(color='#DC3545', width=2),
        hovertemplate='%{y}%<extra>Memory</extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['network_usage'],
        name='Network (Mbps)',
        line=dict(color='#198754', width=2),
        hovertemplate='%{y} Mbps<extra>Network</extra>'
    ))
    
    fig.update_layout(
        title='System Performance (Last 4 Hours)',
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='white',
        plot_bgcolor='rgba(0,0,0,0.02)',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            title='Time',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
        ),
        yaxis=dict(
            title='Utilization',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
        )
    )
    
    return fig

# Create server status table
server_table = dbc.Table([
    html.Thead(
        html.Tr([html.Th("Server"), html.Th("Status"), html.Th("Load")])
    ),
    html.Tbody([
        html.Tr([
            html.Td(row['server']),
            html.Td([
                html.Span(
                    row['status'],
                    style={
                        "color": "white",
                        "backgroundColor": "#198754" if row['status'] == "Operational" else
                                          "#FFC107" if row['status'] == "Warning" else "#DC3545",
                        "padding": "2px 8px",
                        "borderRadius": "12px",
                        "fontSize": "0.8rem",
                        "fontWeight": "bold"
                    }
                )
            ]),
            html.Td([
                dbc.Progress(
                    value=row['load'],
                    color="success" if row['load'] < 70 else "warning" if row['load'] < 90 else "danger",
                    style={"height": "10px", "width": "120px"}
                )
            ])
        ]) for _, row in server_status.iterrows()
    ])
], bordered=False, hover=True, responsive=True, size="sm", className="mt-3")

# Layout
layout = html.Div([
    # Title
    html.H4("System Health & Performance", className="mb-4"),
    
    # Main content container
    dbc.Row([
        # Left panel with metrics cards
        dbc.Col([
            # Resource metrics cards
            dbc.Row([
                # CPU Usage card
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("CPU Usage", className="card-subtitle text-muted"),
                            html.H3(f"{metrics['cpu_usage']}%", className="my-2"),
                            dbc.Progress(
                                value=metrics['cpu_usage'],
                                color="success" if metrics['cpu_usage'] < 70 else "warning" if metrics['cpu_usage'] < 90 else "danger",
                                className="mb-2"
                            )
                        ])
                    ], className="shadow-sm"),
                    width=4
                ),
                
                # Memory Usage card
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Memory Usage", className="card-subtitle text-muted"),
                            html.H3(f"{metrics['memory_usage']}%", className="my-2"),
                            dbc.Progress(
                                value=metrics['memory_usage'],
                                color="success" if metrics['memory_usage'] < 70 else "warning" if metrics['memory_usage'] < 90 else "danger",
                                className="mb-2"
                            )
                        ])
                    ], className="shadow-sm"),
                    width=4
                ),
                
                # Storage Usage card
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Storage", className="card-subtitle text-muted"),
                            html.H3(f"{metrics['storage_usage']}%", className="my-2"),
                            dbc.Progress(
                                value=metrics['storage_usage'],
                                color="success" if metrics['storage_usage'] < 70 else "warning" if metrics['storage_usage'] < 90 else "danger",
                                className="mb-2"
                            )
                        ])
                    ], className="shadow-sm"),
                    width=4
                ),
            ], className="mb-3"),
            
            # Network metrics cards
            dbc.Row([
                # Network In card
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Network In", className="card-subtitle text-muted"),
                            html.H3([
                                f"{metrics['network_in']}",
                                html.Span(" Mbps", style={"fontSize": "1rem", "color": "#6c757d"})
                            ], className="my-2"),
                            html.Div(className="mb-1"),
                            html.Div(html.I(className="fas fa-arrow-down text-success"), style={"textAlign": "right"})
                        ])
                    ], className="shadow-sm"),
                    width=4
                ),
                
                # Network Out card
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Network Out", className="card-subtitle text-muted"),
                            html.H3([
                                f"{metrics['network_out']}",
                                html.Span(" Mbps", style={"fontSize": "1rem", "color": "#6c757d"})
                            ], className="my-2"),
                            html.Div(className="mb-1"),
                            html.Div(html.I(className="fas fa-arrow-up text-primary"), style={"textAlign": "right"})
                        ])
                    ], className="shadow-sm"),
                    width=4
                ),
                
                # Temperature card
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("System Temp", className="card-subtitle text-muted"),
                            html.H3([
                                f"{metrics['system_temp']}",
                                html.Span(" °F", style={"fontSize": "1rem", "color": "#6c757d"})
                            ], className="my-2"),
                            html.Div(
                                html.I(className="fas fa-thermometer-half text-warning"),
                                style={"textAlign": "right"}
                            )
                        ])
                    ], className="shadow-sm"),
                    width=4
                ),
            ], className="mb-3"),
            
            # Performance chart
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(
                        figure=create_performance_chart(time_series_data),
                        config={'displayModeBar': False},
                    )
                ])
            ], className="shadow-sm mb-3"),
        ], width=8),
        
        # Right panel with system info
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("System Information", className="fw-bold"),
                dbc.CardBody([
                    html.Div([
                        html.Div("Uptime:", className="text-muted"),
                        html.Div(metrics['uptime'], className="fw-bold mb-2")
                    ]),
                    html.Div([
                        html.Div("Last Restart:", className="text-muted"),
                        html.Div(metrics['last_restart'], className="fw-bold mb-2")
                    ]),
                    html.Div([
                        html.Div("Active Users:", className="text-muted"),
                        html.Div(metrics['active_users'], className="fw-bold mb-2")
                    ]),
                    html.Div([
                        html.Div("Active Processes:", className="text-muted"),
                        html.Div(metrics['active_processes'], className="fw-bold mb-2")
                    ]),
                ])
            ], className="shadow-sm mb-3"),
            
            dbc.Card([
                dbc.CardHeader("Server Status", className="fw-bold"),
                dbc.CardBody([
                    server_table
                ])
            ], className="shadow-sm mb-3"),
            
            dbc.Card([
                dbc.CardHeader("Quick Actions", className="fw-bold"),
                dbc.CardBody([
                    dbc.Button("Refresh System Data", color="primary", className="me-2 mb-2"),
                    dbc.Button("System Diagnostics", outline=True, color="secondary", className="me-2 mb-2"),
                    dbc.Button("View Logs", outline=True, color="secondary", className="me-2 mb-2"),
                    dbc.Button("Maintenance Mode", outline=True, color="warning", className="me-2")
                ])
            ], className="shadow-sm")
        ], width=4)
    ])
], style={"padding": "20px"}) 