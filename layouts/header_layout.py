import dash
from dash import html
import dash_bootstrap_components as dbc

header_layout = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.NavbarBrand("Mesonet Protoype", className="ms-3"),
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
