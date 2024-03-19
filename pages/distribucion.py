import dash
from dash import html, dcc, Output, Input
import pandas as pd
import plotly.express as px

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Definir el diseño de la aplicación
columnas_categoricas = ['NRO_HOGAR', 'COMPONENTE', 'REGION', 'CH03', 'CH07', 'CH10', 'CH15', 'CH16',
                        'ESTADO', 'CAT_INAC', 'PP02E', 'PP02E_jefx', 'H15', 'CH09', 'CH11', 'PP02H',
                        'PP07I', 'PP07H', 'PP04B1', 'REALIZADA', 'IV5', 'IV8', 'IV12_1', 'IV12_2',
                        'IV12_3', 'II3', 'II4_1', 'II4_2', 'II4_3', 'V1', 'V2', 'V21', 'V22', 'V3',
                        'V5', 'V6', 'V7', 'V8', 'V11', 'V12', 'V13', 'V14', 'REALIZADA_jefx',
                        'CH04_jefx', 'PP07I_jefx', 'PP07H_jefx', 'PP04B1_jefx', 'REALIZADA_conyuge',
                        'CH04_conyuge', 'JEFE_TRABAJA', 'CONYUGE_TRABAJA', 'JEFA_MUJER', 'HOGAR_MONOP',
                        'NBI_SUBSISTENCIA', 'NBI_COBERTURA_PREVISIONAL', 'NBI_DIFLABORAL', 'NBI_HACINAMIENTO',
                        'NBI_SANITARIA', 'NBI_TENENCIA', 'NBI_TRABAJO_PRECARIO', 'NBI_VIVIENDA',
                        'NBI_ZONA_VULNERABLE', 'DESERTO', 'MAS_500', 'CH04', 'II8', 'IV6', 'IV7', 'IV9',
                        'IV10', 'IV11', 'CH08', 'TRIMESTRE', 'CAT_OCUP', 'DECINDR', 'NIVEL_ED', 'IV1',
                        'IV3', 'IV4', 'II7', 'DECCFR', 'ESTADO_jefx', 'NIVEL_ED_jefx', 'CAT_OCUP_jefx',
                        'ANO4', 'II9', 'ESTADO_conyuge']

columnas_numericas = ['AGLOMERADO', 'PONDERA', 'CH06', 'T_VI', 'V2_M', 'IV2', 'II1', 'II2', 'IX_TOT',
                      'IX_MEN10', 'IX_MAYEQ10', 'ITF', 'CH06_jefx', 'ratio_ocupados']

app.layout = html.Div([
    dcc.Dropdown(
        id='variable-dropdown',
        options=[{'label': col, 'value': col}
                 for col in (columnas_categoricas + columnas_numericas)],
        value='NRO_HOGAR'
    ),
    dcc.Graph(id='distribution-plot')
])

# Definir la función de actualización del gráfico


@app.callback(
    Output('distribution-plot', 'figure'),
    [Input('variable-dropdown', 'value')]
)
def update_plot(selected_variable):
    filtered_df = df_data_explore[df_data_explore[selected_variable] != -999]

    if selected_variable in columnas_categoricas:
        fig = px.histogram(filtered_df, x=selected_variable, histfunc='count')
    elif selected_variable in columnas_numericas:
        fig = px.histogram(filtered_df, x=selected_variable)
    else:
        fig = None

    if fig:
        fig.update_layout(title='Distribución de {}'.format(selected_variable))

    return fig


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
