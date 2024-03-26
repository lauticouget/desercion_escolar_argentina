import os

import dash
from dash import dcc, html, callback, Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

from desercion_escolar_argentina.utils import file_handler as fh

# Obtener la ruta del directorio base del proyecto
repo_path = fh.get_repo_path()

# Guardar el archivo en el directorio
file_path = os.path.join(repo_path, 
                         'data/preprocessed/preprocessed_eda.csv')

# Cargar el archivo CSV en un DataFrame
df = pd.read_csv(file_path)


# Definir la aplicación Dash
dash.register_page(__name__, path='/violin')

# Definir el diseño de la aplicación
layout = html.Div([
    dcc.Dropdown(
        id='variable-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns[1:20]],
        value=df.columns[1],
        placeholder="Selecciona una variable"
    ),
    dcc.Graph(id='violin-plot')
])

# Definir la función de actualización para el gráfico de violín


# @callback(
#     Output('violin-plot', 'figure'),
#     [Input('variable-dropdown', 'value')]
# )
# def update_violin_plot(selected_variable):
#     fig = go.Figure()

#     data_deserto_0 = df[selected_variable][(
#         df['DESERTO'] == 0) & (df[selected_variable] != -999)]
#     data_deserto_1 = df[selected_variable][(
#         df['DESERTO'] == 1) & (df[selected_variable] != -999)]

#     fig.add_trace(go.Violin(x=df['DESERTO'][df['DESERTO']],
#                             y=data_deserto_0,
#                             legendgroup='Desertó', scalegroup='0', name='Desertó',
#                             width=0.3,
#                             side='negative',
#                             pointpos=-1.5,
#                             line_color='lightseagreen'))

#     fig.add_trace(go.Violin(x=df['DESERTO'][df['DESERTO']],
#                             y=data_deserto_1,
#                             legendgroup='No desertó', scalegroup='1', name='No desertó',
#                             width=0.3,
#                             side='positive',
#                             pointpos=1.5,
#                             line_color='mediumpurple'
#                             ))

#     fig.update_traces(meanline_visible=True,
#                       points='all',
#                       jitter=0.05,
#                       scalemode='count')

#     min_value = df[selected_variable][df[selected_variable] != -999].min()

#     fig.update_layout(
#         title_text=f"Distribucion de {selected_variable} segun la deserción",
#         violingap=0, violinmode='overlay', xaxis_showticklabels=False,
#         yaxis=dict(range=[min_value - 1, df[selected_variable].max() + 1])
#     )

#     return fig

