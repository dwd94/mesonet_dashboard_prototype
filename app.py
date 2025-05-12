import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

from mesonet_dash_prototype import pages

# Initialize the app with the Cosmo theme from Bootswatch
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.FLATLY],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

# Set the title of the page
app.title = 'Oklahoma Mesonet'

# Create the navbar
navbar = dbc.Navbar(
    dbc.Container([
        # Brand element with logo, vertically centered
        dbc.Row([
            dbc.Col(
                html.A(
                    html.Img(src="/assets/oklahoma-mesonet-logo.png", height="40px"),
                    href="/"
                ),
                width="auto",
                class_name="me-2 d-flex align-items-center"
            ),
            dbc.Col(
                html.A(
                    dbc.NavbarBrand("Oklahoma Mesonet", className="ms-2 fw-bold"),
                    href="/",
                    style={"textDecoration": "none"}
                ),
                width="auto"
            ),
        ], align="center", className="g-0"),
        
        # Navigation links - removed About link
        dbc.Nav([
            dbc.NavItem(dbc.NavLink("Dashboard", href="/", active="exact")),
            dbc.NavItem(dbc.NavLink("Category", href="/category", active="exact")),
            dbc.NavItem(dbc.NavLink("System", href="/system", active="exact")),
        ], className="ms-auto", navbar=True),
        
        # User profile with dropdown
        dbc.Row([
            dbc.Col(
                dbc.DropdownMenu(
                    [
                        dbc.DropdownMenuItem("Profile", href="#"),
                        dbc.DropdownMenuItem("Settings", href="#"),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("Logout", href="#"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label=html.Img(src="/assets/user-avatar.png", height="30px", className="rounded-circle"),
                    align_end=True,
                ),
                width="auto",
            ),
        ], align="center", className="g-0 ms-3"),
    ]),
    color="primary",
    dark=True,
    className="mb-2",
)

# Create the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

# Define the callback to render the correct page content
@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/category':
        return pages.category.layout
    elif pathname == '/system':
        return pages.system.layout
    elif pathname == '/' or pathname == '/providers':
        return pages.index.layout
    else:
        return pages.index.layout

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=10000) 