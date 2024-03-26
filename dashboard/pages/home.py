import os
import pickle

import dash
from dash import dcc, html, callback, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import json
import pyeph

from desercion_escolar_argentina.utils import file_handler as fh

repo_path =fh.get_repo_path()
regiones_file = os.path.join(repo_path, 'Regiones.geojson')
model_file = os.path.join(repo_path, 'models/logistic_1932024.pkl')
with open(regiones_file) as regs:
    regiones = json.load(regs)
with open(model_file, 'rb') as file:  
    model = pickle.load(file)
pred_path = os.path.join(repo_path, 
                         'data/preprocessed/preprocessed_predict.csv')
data = pd.read_csv(pred_path)
id_cols = [
    'CODUSU', 'NRO_HOGAR', 'COMPONENTE', 'ANO4', 'TRIMESTRE', 'PONDERA',
    'DESERTO'
]

X = data.loc[:, ~data.columns.isin(id_cols)].dropna()

importantes = [
    'CH06', 'CH04', 'NIVEL_ED', 'II8',
    'IX_MEN10', 'CH07', 'V12', 'IV2', 'NIVEL_ED_jefx', 'ESTADO'
]

y_pred = model.predict(X)
X.loc[:, 'DESERTO'] = y_pred


presentacion = """
En Argentina, la educación es un derecho consagrado por la Constitución Nacional y regulado por la Ley Nº 26.206 de Educación Nacional. La escolaridad obligatoria abarca 14 años consecutivos, desde sala de 4 y preescolar en el Nivel Inicial, pasando por el Nivel Primario (con duración de 6 o 7 años según la jurisdicción), hasta el Nivel Secundario (con duración de 6 o 5 años, según la duración del nivel primario de la jurisdicción).\n
Este proyecto utiliza un modelo de machine learning para predecir deserción escolar de un trimestre a otro usando la base de datos de la EPH. Al apretar el botón \"Predecir\" aplicará el modelo predictivo a los datos del tercer trimestre de 2023."""

dash.register_page(__name__, path='/')

layout = dbc.Container([
    dbc.Row([dbc.Container(children=presentacion, id="texto-principal")]),
    dbc.Row([
        dbc.Col(html.Div([
                dbc.Button("Predecir", color="secondary", className="me-1", id='predict-button'),
                dcc.Graph(figure={}, id='choropleth-map'),
                dbc.Container(html.Img(src='assets/conf_matrix.png'))
            ], style={'position': 'sticky', 'top': 0}), width=4),
        dbc.Col(html.Div([
            dcc.Graph(figure={}, id='chart1'),
            dcc.Graph(figure={}, id='chart2'),
            dcc.Graph(figure={}, id='chart3'),
            dcc.Graph(figure={}, id='chart4'),
            dcc.Graph(figure={}, id='chart5')
        ]), width=4),
        dbc.Col([
            dcc.Graph(figure={}, id='chart6'),
            dcc.Graph(figure={}, id='chart7'),
            dcc.Graph(figure={}, id='chart8'),
            dcc.Graph(figure={}, id='chart9'),
            dcc.Graph(figure={}, id='chart10')
        ], width=4)
    ])
], fluid=True)

# Callback to update choropleth map
@callback( 
    Output('choropleth-map', 'figure'),
    [Input('predict-button', 'n_clicks')]
)
def update_choropleth(n_clicks):
    if n_clicks is None:
        group = pd.DataFrame(data.groupby('REGION').size()).reset_index()
        group.rename({'REGION': 'CodigoEPH', 0: 'personas'}, axis=1, inplace=True)
        fig = px.choropleth(group, geojson=regiones, locations='CodigoEPH', color='personas',
            color_continuous_scale="Viridis",
            range_color=(group.personas.min(), group.personas.max()),
            scope='south america',
            projection='mercator',
            featureidkey='properties.CodigoEPH'
            )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig
    group = pd.DataFrame(X[X.DESERTO == 1].groupby('REGION').size().reset_index())
    group.rename({'REGION': 'CodigoEPH', 0: 'desertores'}, axis=1, inplace=True)
    fig = px.choropleth(group, geojson=regiones, locations='CodigoEPH', color='desertores',
        color_continuous_scale="Viridis",
        range_color=(group.desertores.min(), group.desertores.max()),
        scope='south america',
        projection='mercator',
        featureidkey='properties.CodigoEPH'
        )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


@callback(
    [Output(f'chart{i}', 'figure') for i in range(1, 11)],
    [Input('predict-button', 'n_clicks')]
)
def update_charts(n_clicks):
    if n_clicks is None:
        charts = []
        for i in range(1, 11):
            charts.append(px.histogram(data_frame=X,
                                       x=importantes[i-1],
                                       color='CH04',
                                       labels={'CH04': 'Género'}))
        return charts
    charts = []
    for i in range(1, 11):
            charts.append(px.histogram(data_frame=X,
                                       x=importantes[i-1],
                                       color='DESERTO'))
    return charts
