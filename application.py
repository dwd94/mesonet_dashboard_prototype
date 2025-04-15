from dash import Dash, html, dcc, Patch, no_update
import plotly.express as px
import dash
import pandas as pd
import json
import time
from datetime import date
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from flask import Flask
import numpy as np
from dotenv import load_dotenv
import logging
import sys
import os

# serve production ready server
from waitress import serve
from layouts.header_layout import header_layout

# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
load_dotenv()

DASH_PROD = os.getenv("DASH_PROD")


def create_app():
    """
    Create the Flask app.
    """
    server = Flask(__name__)

    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        force=True,
    )

    log = logging.getLogger(__name__)
    log.info("Creating app")

    FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"

    # create the Dash app
    application = Dash(
        __name__,
        server=server,
        # prevent_initial_callbacks="initial_duplicate",
        # suppress_callback_exceptions=True,
        use_pages=True,
        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            dbc.icons.BOOTSTRAP,
            FONT_AWESOME,
        ],
    )

    application.layout = dbc.Container(
        fluid=True,
        id="root",  # most outer container
        children=[
            header_layout,
            dash.page_container,
        ],
        style={"padding": 0, "overflow-x": "hidden"},
    )

    # return the Dash app
    return application


if __name__ == "__main__":

    application = create_app()

    if DASH_PROD == "True":
        print("app is running with production server")
        serve(application.server, host="0.0.0.0", port=10000)
    else:
        print("app is running with development server")
        application.run(host="0.0.0.0", debug=True, port=10000)
