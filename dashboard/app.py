import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
server = app.server

app.layout = html.Div([
    dbc.NavbarSimple(
        [dbc.NavLink(f"{page['name']}", href=page["relative_path"])
        for page in dash.page_registry.values()
        ],
        brand="Deserción Escolar Argentina",
        brand_href="/home",
        color="primary",
        dark=True,
        sticky="top"
    ),
    dash.page_container
])


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
