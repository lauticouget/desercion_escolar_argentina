import dash
from dash import Dash, dcc, html, callback, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, path='/')

layout = html.Div([
            html.Div([
                html.H4("Prediction"),
                html.Button("Predict", id="predict-button"),
                dcc.Graph(id='choropleth-map')
            ], className="col-md-3"),
            html.Div([
                html.Div([
                    dcc.Graph(id='chart-{}'.format(i))
                ], className="row") for i in range(1, 11)
            ], className="col-md-9")
        ], className="container-fluid")

# Callback to update choropleth map
@callback(
    Output('choropleth-map', 'figure'),
    [Input('predict-button', 'n_clicks')]
)
def update_choropleth(n_clicks):
    if n_clicks is None:
        return px.choropleth(data, locations='Province', locationmode='country names', color='Dropout Rate', scope='south america', title='Dropout Rate in Argentina')
    else:
        # Run prediction and update map
        # Replace this with your actual prediction code
        predicted_data = {
            'Province': ['Buenos Aires', 'Cordoba', 'Santa Fe', 'Mendoza', 'Tucuman'],
            'Predicted Dropout Rate': [8, 7, 9, 6, 8]
        }
        return px.choropleth(predicted_data, locations='Province', locationmode='country names', color='Predicted Dropout Rate', scope='south america', title='Predicted Dropout Rate in Argentina')

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