import os

import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pyeph

from desercion_escolar_argentina.utils import file_handler as fh

dash.register_page(__name__)

repo_path = fh.get_repo_path()

file_path = os.path.join(repo_path, 
                         'data/preprocessed/preprocessed_train.csv')
data = pd.read_csv(file_path).fillna(0)


def make_violin_plot(df, col='CH06', bivariate='DESERTO'):
    data_0 = df[col][df[bivariate] == 0]
    data_1 = df[col][df[bivariate] == 1]
    fig = go.Figure()
    fig.add_trace(go.Violin(x=df[bivariate][df[bivariate]],
                            y=data_0,
                            legendgroup='Desertó', scalegroup='0', name='Desertó',
                            width=0.3,
                            points=False,
                            side='negative',
                            pointpos=-1.5,
                            line_color='lightseagreen'))
    fig.add_trace(go.Violin(x=df[bivariate][df[bivariate]],
                            y=data_1,
                            legendgroup='No desertó', scalegroup='1', name='No desertó',
                            width=0.3,
                            points=False,
                            side='positive',
                            pointpos=1.5,
                            line_color='mediumpurple'
                            ))
    min_value = df[col].min()

    fig.update_layout(
        violingap=0, violinmode='overlay', xaxis_showticklabels=False,
        yaxis={'range': [min_value - 2, df[col].max() + 1]}
    )

    return fig


def make_hist(df, col='CH06', color_col='DESERTO'):
    fig = px.histogram(data_frame=df,
                       x=col,
                       color=color_col)
    return fig


layout = dbc.Container(
    [dbc.Row(
        [html.H2('Histograma y distribución bivariada de la variable seleccionada'),
         dcc.Dropdown(
            id='variable-dropdown',
            options=[{'label': col, 'value': col} for col in data.columns],
            placeholder="Seleccionar variable a mostrar",
        )]),
    dbc.Row(
        [dbc.Col(
            dcc.Graph(figure=make_hist(df=data), id='histplot'),
            width=6
        ),
        dbc.Col(
            dcc.Graph(figure=make_violin_plot(df=data), id='violin-plot'),
            width=6
        )]
    )], fluid=True
)

@callback(
    Output('violin-plot', 'figure'),
    [Input('variable-dropdown', 'value')],
    prevent_initial_call=True
)
def draw_violin_plot(selected_variable):
    violin = make_violin_plot(df=data, col=selected_variable)
    return violin


@callback(
    Output('histplot', 'figure'),
    [Input('variable-dropdown', 'value')],
    prevent_initial_call=True
)
def draw_violin_plot(selected_variable):
    hist = make_hist(df=data, col=selected_variable)
    rename_traces(hist)
    return hist