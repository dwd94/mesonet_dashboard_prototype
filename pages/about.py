import dash
from dash import html

# Register the page
dash.register_page(__name__, path="/about", name="About")

layout = html.Div(
    [
        html.H3("About This App"),
        html.P("This app is a prototype for the mesonet system."),
    ]
)
