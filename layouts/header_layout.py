import dash
from dash import html
import dash_bootstrap_components as dbc

header_layout = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.NavbarBrand("Mesonet Prototype", className="ms-3"),
                href="/",  # Link to home
                style={"textDecoration": "none"},  # Remove underline
            ),
            dbc.Nav(
                [
                    dbc.NavItem(
                        dbc.NavLink("Home", href="/", className="nav-link")
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            "About", href="/about", className="nav-link"
                        )
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            html.Span("Providers", style={"fontWeight": "bold"}),
                            href="/providers",
                            className="nav-link"
                        )
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            html.Span("Category", style={"fontWeight": "bold"}),
                            href="/category",
                            className="nav-link"
                        )
                    ),
                ],
                className="ms-auto",
                navbar=True,
            ),
        ],
        fluid=True,
    ),
    color="primary",
    dark=True,
)
