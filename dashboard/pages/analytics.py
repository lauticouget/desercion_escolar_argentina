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

d_var = {'CODUSU': 'Código para distinguir VIVIENDAS, permite aparearlas con Hogares y Personas. Además permite hacer el seguimiento a través de los trimestres.',
 'NRO_HOGAR': 'Código para distinguir Hogares, permite aparearlos con Personas.',
 'COMPONENTE': 'Número de componente: número de orden que se asigna a las personas que conforman cada hogar de la vivienda.',
 'ANO4': 'Año de relevamiento (4 dígitos)',
 'TRIMESTRE': 'Ventana de observación',
 'REGION': 'REGION',
 'MAS_500': 'MAS_500',
 'AGLOMERADO': 'Código de aglomerado',
 'PONDERA': 'Ponderación',
 'CH03': 'Relación de parentesco',
 'CH04': 'Sexo',
 'CH06': '¿Cuántos años cumplidos tiene?',
 'CH07': '¿Actualmente está...',
 'CH08': '¿Tiene algún tipo de cobertura médica por la que paga o le descuentan?',
 'CH09': '¿Sabe leer y escribir?',
 'CH10': '¿Asiste o asistió a algún establecimiento educativo? (colegio, escuela, universidad)',
 'CH11': 'Ese establecimiento es…',
 'CH15': '¿Dónde nació?',
 'CH16': 'Dónde vivía hace 5 años?',
 'ESTADO': 'Condición de actividad',
 'PP02E': 'Durante esos 30 días, no buscó trabajo porque…',
 'PP02H': 'En los últimos 12 meses ¿buscó trabajo en algún momento?',
 'servicio_domestico': 'Si la persona brinda servicio doméstico en otro hogar',
 'NIVEL_ED': 'Nivel educativo',
 'IV1': 'Tipo de vivienda',
 'IV2': 'Cantidad de ambientes',
 'IV3': 'Material de los pisos interiores',
 'IV4': 'Material de la cubierta exterior del techo',
 'IV5': '¿El techo tiene cielorraso/revestimiento interior?',
 'IV6': 'Tiene agua...',
 'IV7': 'El agua es de...',
 'IV9': 'El baño o letrina está...',
 'IV11': 'El desagüe del baño es...',
 'IV12_2': 'La vivienda está ubicada en zona inundable',
 'II1': 'Ambientes de uso exclusivo',
 'II2': 'Ambientes usados para dormir',
 'II3': 'Ambientes usados exclusivamente como lugares de trabajo',
 'II4_1': 'Tiene cuarto de cocina',
 'II4_2': 'Tiene lavadero',
 'II4_3': 'Tiene garage',
 'II8': 'Combustible utilizado para cocinar',
 'II9': 'Baño (tenencia y uso)',
 'V1': '¿Las personas del hogar viven de lo ganan en el trabajo?',
 'V2': '¿Las personas del hogar viven de alguna jubilación o pensión?',
 'V21': '¿Las personas del hogar viven de algún aguinaldo de una jubilación?',
 'V22': '¿Las personas del hogar viven de algún retroactivo de una jubilación?',
 'V3': '¿Las personas del hogar viven de una indemnización por despido?',
 'V5': '¿Las personas del hogar viven de algún subsidio o ayuda social?',
 'V6': '¿Las personas del hogar viven de mercaderías, ropa, alimentos otorgados por instituciones?',
 'V7': '¿Las personas del hogar viven de mercaderías, ropa, alimentos otorgados por personas?',
 'V8': '¿Las personas del hogar viven de algún alquiler?',
 'V11': '¿Las personas del hogar viven de una beca de estudio?',
 'V12': '¿Las personas del hogar viven de cuotas de alimento o ayuda en dinero brindadas por otras personas?',
 'V13': '¿Las personas del hogar viven de gastar ahorros?',
 'V14': '¿Las personas del hogar viven de prestamos de familiares/amigos?',
 'IX_TOT': 'Cantidad de personas del hogar',
 'IX_MEN10': 'Cantidad de menores de 10 años del hogar',
 'DECCFR': 'Decil de ingresos familiar',
 'CH06_jefx': 'Edad del jefx de hogar',
 'ESTADO_jefx': 'Estado ocupacional del jefx de hogar',
 'NIVEL_ED_jefx': 'Nivel educativo del jefx de hogar',
 'APORTES_JUBILATORIOS_jefx': 'Aportes jubilatorios del jefx de hogar',
 'PP04B1_jefx': 'Si el jefx de hogar realiza servicio doméstico en otros hogares',
 'ESTADO_conyuge': 'Estado laboral del cónyuge',
 'JEFA_MUJER': 'Jefa de hogar mujer',
 'HOGAR_MONOP': 'Hogar monoparental',
 'ratio_ocupados': 'Ratio de ocupados/miembros',
 'NBI_COBERTURA_PREVISIONAL': 'NBI_COBERTURA_PREVISIONAL',
 'NBI_DIFLABORAL': 'NBI_DIFLABORAL',
 'NBI_HACINAMIENTO': 'NBI_HACINAMIENTO',
 'NBI_SANITARIA': 'NBI_SANITARIA',
 'NBI_TENENCIA': 'NBI_TENENCIA',
 'NBI_TRABAJO_PRECARIO': 'NBI_TRABAJO_PRECARIO',
 'NBI_VIVIENDA': 'NBI_VIVIENDA',
 'NBI_ZONA_VULNERABLE': 'NBI_ZONA_VULNERABLE',
 'DESERTO': 'DESERTO'}


def get_key_or_value(dictionary, query):
    """
    Get the key if the query is a value in the dictionary,
    or get the value if the query is a key in the dictionary.
    
    Parameters:
    dictionary (dict): The dictionary to search.
    query (str): The key or value to search for.
    
    Returns:
    str: The key if the query is a value in the dictionary,
         or the value if the query is a key in the dictionary.
    """
    if query in dictionary.values():
        return next(key for key, value in dictionary.items() if value == query)
    elif query in dictionary.keys():
        return dictionary[query]
    else:
        return None

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
            options=[{'label': col, 'value': col} for col in d_var.values()],
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
    column = get_key_or_value(d_var, selected_variable)
    violin = make_violin_plot(df=data, col=column)
    return violin


@callback(
    Output('histplot', 'figure'),
    [Input('variable-dropdown', 'value')],
    prevent_initial_call=True
)
def draw_violin_plot(selected_variable):
    column = get_key_or_value(d_var, selected_variable)
    hist = make_hist(df=data, col=column)
    return hist