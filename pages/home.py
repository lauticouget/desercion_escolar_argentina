import os
import dash
from dash import Dash, dcc, html, callback, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import json

from desercion_escolar_argentina.utils import file_handler as fh

repo_path =fh.get_repo_path()
train_path = os.path.join(repo_path, 'data/preprocessed/', 'preprocessed_train.csv')
data = pd.read_csv(train_path)
with open(os.path.join(repo_path, 'regiones_argentina.geojson')) as file:
    regiones = json.load(file)
group = pd.DataFrame(data.groupby('REGION').count()['ESTADO']).reset_index()

presentacion = """
En Argentina, la educación es un derecho consagrado por la Constitución Nacional y regulado por la Ley Nº 26.206 de Educación Nacional. La escolaridad obligatoria abarca 14 años consecutivos, desde sala de 4 y preescolar en el Nivel Inicial, pasando por el Nivel Primario (con duración de 6 o 7 años según la jurisdicción), hasta el Nivel Secundario (con duración de 6 o 5 años, según la duración del nivel primario de la jurisdicción).\n
Este proyecto utiliza un modelo de machine learning para predecir deserción escolar de un trimestre a otro usando la base de datos de la EPH."""

dash.register_page(__name__, path='/')

layout = html.Div(
    [
        dbc.Row([html.Div(children=presentacion, id="texto-principal")]),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            dbc.Button(
                                "Predecir",
                                color="secondary",
                                className="me-1",
                                id="predict-button",
                            ),
                            dcc.Graph(figure={}, id="choropleth-map"),
                        ]
                    ),
                    width=4,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Div(
                                [dcc.Graph(id="chart-{}".format(i))], className="row"
                            )
                            for i in range(1, 6)
                        ]
                    ),
                    width=4,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Div(
                                [dcc.Graph(id="chart-{}".format(i))], className="row"
                            )
                            for i in range(1, 6)
                        ]
                    ),
                    width=4,
                ),
            ]
        ),
    ]
)

# Callback to update choropleth map
@callback(
    Output('choropleth-map', 'figure'),
    [Input('predict-button', 'n_clicks')]
)
def update_choropleth(n_clicks):
    if n_clicks is None:
        fig = px.choropleth(group, geojson=regiones, locations='REGION', color='ESTADO',
                    color_continuous_scale="Viridis",
                    range_color=(0, 12),
                    scope='south america',
                    labels={'unemp':'unemployment rate'}
                    )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig
    else:
        fig = px.choropleth(group, geojson=regiones, locations='REGION', color='ESTADO',
                            color_continuous_scale="Viridis",
                            range_color=(0, 12),
                            scope='south america',
                            labels={'unemp':'unemployment rate'}
                            )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig

# Callback to update charts
@callback(
    [Output('chart-{}'.format(i), 'figure') for i in range(1, 11)],
    [Input('predict-button', 'n_clicks')]
)
def update_charts(n_clicks):
    if n_clicks is None:
        # Initial data for charts
        charts = []
        for i in range(1, 11):
            charts.append(px.bar(x=['A', 'B', 'C', 'D', 'E'], y=[i]*5, title='Chart {}'.format(i)))
        return charts
    else:
        # Run prediction and update charts
        # Replace this with your actual prediction code
        charts = []
        for i in range(1, 11):
            charts.append(px.bar(x=['A', 'B', 'C', 'D', 'E'], y=[i+1]*5, title='Chart {} (Updated)'.format(i)))
        return charts
