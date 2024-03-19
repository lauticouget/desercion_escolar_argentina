import dash
from dash import Dash, html
import plotly.express as px
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

app.layout = html.Div([
    dbc.NavbarSimple([
        html.Div(
            dbc.NavLink(f"{page['name']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ],
        brand="School Dropout Prediction",
        brand_href="#",
        color="primary",
        dark=True,
        sticky="top"
    ),
    dash.page_container
])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
