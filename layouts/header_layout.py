import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

header_layout = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row([
                    dbc.Col(html.I(className="fas fa-chart-line me-2", style={"fontSize": "24px", "color": "white"})),
                    dbc.Col(dbc.NavbarBrand("Mesonet Dashboard", className="ms-2")),
                ], align="center", className="g-0"),
                href="/providers",  # Default to providers page
                style={"textDecoration": "none"},
            ),
            dbc.Nav(
                [
                    dbc.NavItem(
                        dbc.NavLink(
                            html.Div([
                                html.I(className="fas fa-home me-1"),
                                "Home"
                            ], style={"display": "flex", "alignItems": "center"}),
                            href="/",
                            className="nav-link"
                        )
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            html.Div([
                                html.I(className="fas fa-info-circle me-1"),
                                "About"
                            ], style={"display": "flex", "alignItems": "center"}),
                            href="/about",
                            className="nav-link"
                        )
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            html.Div([
                                html.I(className="fas fa-broadcast-tower me-1"),
                                html.Span("Providers", style={"fontWeight": "bold"}),
                            ], style={"display": "flex", "alignItems": "center"}),
                            href="/providers",
                            className="nav-link active"
                        )
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            html.Div([
                                html.I(className="fas fa-layer-group me-1"),
                                html.Span("Category", style={"fontWeight": "bold"}),
                            ], style={"display": "flex", "alignItems": "center"}),
                            href="/category",
                            className="nav-link"
                        )
                    ),
                ],
                className="ms-auto me-4",
                navbar=True,
            ),
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.I(className="fas fa-moon", style={"color": "white"}),
                    ], className="p-2 rounded-circle bg-dark bg-opacity-25"),
                    width="auto",
                    className="me-2"
                ),
                dbc.Col(
                    html.Div([
                        html.I(className="fas fa-user", style={"color": "white"}),
                    ], className="p-2 rounded-circle bg-dark bg-opacity-25"),
                    width="auto"
                ),
            ], className="g-0"),
        ],
        fluid=True,
    ),
    color="primary",
    dark=True,
    className="mb-4 shadow-sm",
    style={
        "background": "linear-gradient(90deg, #1e3c72 0%, #2a5298 100%)",
        "borderBottom": "1px solid rgba(255,255,255,0.1)"
    },
)
