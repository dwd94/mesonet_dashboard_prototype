import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

# dcc.Location(id="url", refresh=False),
header_layout = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row([
                    dcc.Location(id="url", refresh=False),
                    dbc.Col(html.I(className="fas fa-chart-line me-2", style={"fontSize": "24px", "color": "white"})),
                    dbc.Col(dbc.NavbarBrand("Mesonet Dashboard", className="ms-2")),
                ], align="center", className="g-0"),
                href="/",  # Default to providers page
                style={"textDecoration": "none"},
            ),
            dbc.Nav(
                [
                    dbc.NavItem(
                        dbc.NavLink(
                            html.Div([
                                html.I(className="fas fa-broadcast-tower me-1"),
                                html.Span("Providers", style={"fontWeight": "bold"}),
                            ], style={"display": "flex", "alignItems": "center"}),
                            id="nav-providers",
                            href="/",
                            className="nav-link"
                        )
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            html.Div([
                                html.I(className="fas fa-layer-group me-1"),
                                html.Span("Category", style={"fontWeight": "bold"}),
                            ], style={"display": "flex", "alignItems": "center"}),
                            id="nav-category",
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

@callback(
    Output("nav-providers", "className"),
    Output("nav-category", "className"),
    Input("url", "pathname")
)
def highlight_active_link(pathname):
    providers_active = "nav-link active" if pathname == "/" else "nav-link"
    category_active = "nav-link active" if pathname == "/category" else "nav-link"
    return providers_active, category_active