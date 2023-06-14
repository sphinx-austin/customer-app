from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import os 

def create_dash_application(flask_app):
    # Create a Dash application integrated with Flask
    dash_app = Dash(
        server=flask_app,
        name="Dashboard",
        url_base_pathname="/dash/",
        external_stylesheets=[
            {
                "href": (
                    "https://fonts.googleapis.com/css2?"
                    "family=Lato:wght@400;700&display=swap"
                ),
                "rel": "stylesheet",
            },
        ],
    )

    # Get the path of the current Python file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute file path
    file_path = os.path.join(current_dir, "custData.csv")

    try:
        data = (
            pd.read_csv(file_path)
            .query("type == 'conventional' and region == 'Albany'")
            .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
            .sort_values(by="Date")
        )
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")

    # Create the Dash layout
    dash_app.layout = html.Div(
        children=[
            html.H1(
                children="Customer Lifetime Value",
                className="header-title",
            ),
            html.P(
                children=(
                    "Analyze the behavior of customer lifetime value and the number"
                    " of customers between 2015 and 2018"
                ),
            ),
            dcc.Graph(
                figure={
                    "data": [
                        {
                            "x": data["Date"],
                            "y": data["AveragePrice"],
                            "type": "lines",
                        },
                    ],
                    "layout": {"title": "Customer Lifetime Value"},
                },
            ),
            dcc.Graph(
                figure={
                    "data": [
                        {
                            "x": data["Date"],
                            "y": data["Total Volume"],
                            "type": "lines",
                        },
                    ],
                    "layout": {"title": "Transactions Made"},
                },
            ),
        ]
    )

    return dash_app
