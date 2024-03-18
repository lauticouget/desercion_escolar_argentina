import os

import pandas as pd
import numpy as np
import typer
import pyeph

from desercion_escolar_argentina.utils import file_handler as fh
from desercion_escolar_argentina.utils import preprocesado as pr
from desercion_escolar_argentina.utils import limpieza as l


app = typer.Typer()

def obtener_datos(anios: list[int], trimestres: list[int]):
    bases_individuos = [fh.obtener_eph(
        'individual', anio, trimestre) for anio in anios for trimestre in trimestres]
    bases_hogar = [fh.obtener_eph('hogar', anio, trimestre)
                   for anio in anios for trimestre in trimestres]

    data_individuos = [l.seleccionar_features(
        base, l.cols_individual, l.cols_id_individual) for base in bases_individuos]
    data_hogares = [l.seleccionar_features(
        base, l.cols_hogar, l.cols_id_hogar) for base in bases_hogar]

    data = [pr.unir_personas_hogares(
        individuos, hogares) for individuos, hogares in zip(data_individuos, data_hogares)]

    return data, data_individuos, data_hogares


def generar_dataframes_auxiliares(data: pd.DataFrame, hogares: pd.DataFrame):
    jefxs = data[data.CH03 == 1]
    conyuges = data[data.CH03 == 2]
    # hogares por estado de ocupación del jefx
    _jefxs = pd.merge(jefxs, hogares[l.cols_id_hogar], how='left')
    hogares_jefxs = pd.DataFrame(_jefxs.groupby(l.cols_id_hogar)[[
        'CH04', 'CH06', 'ESTADO', 'NIVEL_ED', 'PP02E', 'CAT_OCUP', 'PP07I', 'PP07H', 'PP04B1']].sum()).reset_index()
    # hogares no monoparentales según género y ocupación del cónyuge
    _conyuges = pd.merge(conyuges, hogares[l.cols_id_hogar], how='left')
    hogares_conyuges = pd.DataFrame(_conyuges.groupby(l.cols_id_hogar)[[
        'CH04', 'ESTADO']].sum()).reset_index()
    return hogares_jefxs, hogares_conyuges


def unir_jefxs_conyuges(data: pd.DataFrame,
                        hogares_jefxs: pd.DataFrame,
                        hogares_conyuges: pd.DataFrame):
    _data = pr.unir_personas_hogares(data,
                                     hogares_jefxs,
                                     sufijos=('', '_jefx'))
    estudiantes = pr.unir_personas_hogares(_data,
                                           hogares_conyuges,
                                           como='outer',
                                           sufijos=('', '_conyuge'))
    estudiantes.fillna(0)
    return estudiantes


def generar_jefe_trabaja(data: pd.DataFrame):
    cond = data.ESTADO_jefx == 1
    estudiantes = pr.crear_feature_binaria(data, 'JEFE_TRABAJA', cond)
    return estudiantes


def generar_jefa_mujer(data: pd.DataFrame):
    cond = data.CH04_jefx == 2
    estudiantes = pr.crear_feature_binaria(data, 'JEFA_MUJER', cond)
    return estudiantes


def generar_hogar_monop(data: pd.DataFrame):
    cond = data.ESTADO_conyuge.isna()
    estudiantes = pr.crear_feature_binaria(data, 'HOGAR_MONOP', cond)
    return estudiantes


def generar_conyuge_trabaja(data: pd.DataFrame):
    cond = data.ESTADO_conyuge == 1
    estudiantes = pr.crear_feature_binaria(data, 'CONYUGE_TRABAJA', cond)
    return estudiantes


def generar_nbi_vivienda_precaria(data: pd.DataFrame):
    cond = (data["IV3"] > 2) | ((data["IV4"] > 4) & (data["IV5"] == 2))
    estudiantes = pr.crear_feature_binaria(data, 'NBI_VIVIENDA', cond)
    return estudiantes


def generar_nbi_hacinamiento(data: pd.DataFrame):
    cond = data.IX_TOT / data.IV2 >= 3
    estudiantes = pr.crear_feature_binaria(data, 'NBI_HACINAMIENTO', cond)
    return estudiantes


def generar_nbi_tenencia(data: pd.DataFrame):
    cond = data['II7'].isin([3, 7])
    estudiantes = pr.crear_feature_binaria(data, 'NBI_TENENCIA', cond)
    return estudiantes


def generar_nbi_sanitaria(data: pd.DataFrame):
    cond = (data['IV8'] == 2) | (data['IV10'] > 1)
    estudiantes = pr.crear_feature_binaria(data, 'NBI_SANITARIA', cond)
    return estudiantes


def generar_nbi_zona_vulnerable(data: pd.DataFrame):
    cond = (data['IV12_1'] == 1) | (data['IV12_3'] == 1)
    estudiantes = pr.crear_feature_binaria(data, 'NBI_ZONA_VULNERABLE', cond)
    return estudiantes


def generar_nbi_dificultad_laboral(data: pd.DataFrame):
    cond_hombre = ((data.CH06_jefx.between(16, 64)) & (data.CH04_jefx == 1)) & (
        (data.ESTADO_jefx == 2) | (data.PP02E_jefx.isin([3, 5])))
    cond_mujer = ((data.CH06_jefx.between(16, 59)) & (data.CH04_jefx == 2)) & (
        (data.ESTADO_jefx == 2) | (data.PP02E_jefx.isin([3, 5])))
    data.loc[:, 'NBI_DIFLABORAL'] = np.nan
    data.loc[cond_hombre, 'NBI_DIFLABORAL'] = 1
    data.loc[cond_mujer, 'NBI_DIFLABORAL'] = 1
    data.loc[:, 'NBI_DIFLABORAL'].fillna(0, inplace=True)
    return data


def generar_nbi_trabajo_precario(data: pd.DataFrame):
    cond = ((data.CAT_OCUP == 2) & (data.NIVEL_ED.isin([1, 2, 3, 7]))) | (
        (data.PP07I == 2) | (data.PP07H == 2)) | (
        (data.PP04B1 == 1) & ((data.PP07I == 2) | (data.PP07H == 2)))
    estudiantes = pr.crear_feature_binaria(data, 'NBI_TRABAJO_PRECARIO', cond)
    return estudiantes


def generar_ratio_ocupados_miembros(data: pd.DataFrame, 
                                    individuos: pd.DataFrame,
                                    hogares: pd.DataFrame):
    ocupados_por_hogar = individuos[individuos.ESTADO == 1].groupby(['CODUSU', 'NRO_HOGAR'])['ESTADO'].sum().reset_index()
    ocupados_por_hogar.rename({'ESTADO': 'nro_ocupados'}, axis=1, inplace=True)
    ocupados = pd.merge(hogares, ocupados_por_hogar)
    ocupados.loc[:, 'ratio_ocupados'] = ocupados.nro_ocupados / ocupados.IX_TOT
    cols = l.cols_id_hogar + ['ratio_ocupados']
    estudiantes = pd.merge(data, ocupados[cols], how='left')
    estudiantes.ratio_ocupados.fillna(0, inplace=True)
    return estudiantes


def generar_nbi_subsistencia(data: pd.DataFrame):
    cond = data.NIVEL_ED_jefx.isin([1, 2, 3, 7]) & data.ratio_ocupados >= 4
    estudiantes = pr.crear_feature_binaria(data, 'NBI_SUBSISTENCIA', cond)
    return estudiantes


def generar_nbi_cobertura_previsional(data: pd.DataFrame):
    cond = ((data.CH06 >= 65) & (data.CH04 == 1) & (data.V2_M == 0)) | (
        (data.CH06 >= 60) & (data.CH04 == 2) & (data.V2_M == 0))
    estudiantes = pr.crear_feature_binaria(
        data, 'NBI_COBERTURA_PREVISIONAL', cond)
    return estudiantes

def generar_deserto(data_t: pd.DataFrame,
                    individuos_tp1: pd.DataFrame)->pd.DataFrame:
    cols_tp1 = ['CODUSU', 'NRO_HOGAR', 'COMPONENTE'] + ['CH10']
    data = pd.merge(data_t, individuos_tp1[cols_tp1], 
                    on=['CODUSU', 'NRO_HOGAR', 'COMPONENTE'],
                    suffixes=('', '_fin'),
                    how='inner')
    cond = (data.CH10 == 1) & (data.CH10_fin == 2 )
    estudiantes = pr.crear_feature_binaria(data, 'DESERTO', cond)
    estudiantes.drop(['CH10_fin'], axis=1, inplace=True)
    return estudiantes


def data_constructor(anios: list[int], trimestres: list[int]):
    data, data_individuos, data_hogares = obtener_datos(anios, trimestres)
    # estudiantes de edad >=14
    cond_estudiante = 'CH10 == 1'
    cond_edad = 'CH06 >= 14'
    cond = cond_estudiante + '&' + cond_edad
    estudiantes = [l.filtrar_por_columnas(base, cond) for base in data]
    # ingenieria de atributos
    data = []
    for base, individuos, hogares in zip(estudiantes, data_individuos, data_hogares):
        jefxs, conyuges = generar_dataframes_auxiliares(individuos, hogares)
        _base = unir_jefxs_conyuges(base, jefxs, conyuges)
        _base = generar_jefe_trabaja(_base)
        _base = generar_conyuge_trabaja(_base)
        _base = generar_jefa_mujer(_base)
        _base = generar_hogar_monop(_base)
        _base = generar_ratio_ocupados_miembros(_base, individuos, hogares)
        _base = generar_nbi_subsistencia(_base)
        _base = generar_nbi_cobertura_previsional(_base)
        _base = generar_nbi_dificultad_laboral(_base)
        _base = generar_nbi_hacinamiento(_base)
        _base = generar_nbi_sanitaria(_base)
        _base = generar_nbi_tenencia(_base)
        _base = generar_nbi_trabajo_precario(_base)
        _base = generar_nbi_vivienda_precaria(_base)
        _base = generar_nbi_zona_vulnerable(_base)
        data.append(_base)
    return data, data_individuos

def construir_dataset(data: list[pd.DataFrame], 
                      data_individuos: list[pd.DataFrame],
                      ultimo_trimestre: int):
    estudiantes = []
    for base, base_p1 in zip(data[:-1], data_individuos[1:]):
        _base = generar_deserto(base, base_p1)
        estudiantes.append(_base[_base.TRIMESTRE != ultimo_trimestre])
    return estudiantes


def homogeneizar_binarias(df, columns):
    replace_dict = {col: {2: 0, 'S': 1, 'N': 0, 'NO': 0} for col in columns}
    data = df.replace(replace_dict)
    data[columns].astype('float64', copy=False)
    return data


def aglomerados_a_distancia(df, aglomerado='AGLOMERADO'):
    data_x_y = {
        'eph_codagl': [13, 29, 31, 25, 34, 7, 26, 15, 4, 91, 18, 23, 30, 12, 20, 93, 8, 14, 6, 5, 3, 9, 22, 36, 38, 38, 10, 19, 2, 32, 17, 33, 27],
        'eph_aglome': ['Gran Córdoba', 'Gran Tucumán - Tafi Viejo', 'Ushuaia - Rio Grande', 'La Rioja', 'Mar del Plata - Batán', 'Posadas', 'San Luis - El Chorrillo', 'Formosa', 'Gran Rosario', 'Rawson - Trelew', 'Santiago del Estero - La Banda', 'Salta', 'Santa Rosa - Toay', 'Corrientes', 'Rio Gallegos', 'Viedma - Carmen de Patagones', 'Gran Resistencia', 'Concordia', 'Gran Paraná', 'Gran Santa Fe', 'Bahia Blanca - Cerri', 'Comodoro Rivadavia - Rada Tilly', 'Gran Catamarca', 'Rio Cuarto', 'San Nicolas - Villa Constitiución', 'San Nicolas - Villa Constitiución', 'Gran Mendoza', 'Jujuy - Palpalá', 'Gran La Plata', 'CABA', 'Neuquén - Plottier', 'Partidos del GBA', 'Gran San Juan'],
        'x': [3.668196e+06, 3.575528e+06, 3.368650e+06, 3.433735e+06, 4.238702e+06, 4.500828e+06, 3.470658e+06, 4.290676e+06, 3.989413e+06, 3.561793e+06, 3.671129e+06, 3.558820e+06, 3.652175e+06, 4.215852e+06, 3.274586e+06, 3.754150e+06, 4.194276e+06, 4.258864e+06, 4.023207e+06, 4.008905e+06, 3.824880e+06, 3.382300e+06, 3.520630e+06, 3.656809e+06, 4.035477e+06, 4.029783e+06, 3.231898e+06, 3.560475e+06, 4.234043e+06, 4.193488e+06, 3.310530e+06, 4.180647e+06, 3.260047e+06],
        'y': [6.533650e+06, 7.036009e+06, 3.980855e+06, 6.726538e+06, 5.760505e+06, 6.922012e+06, 6.318389e+06, 7.090830e+06, 6.346344e+06, 5.211965e+06, 6.926946e+06, 7.258796e+06, 5.947417e+06, 6.941437e+06, 4.274342e+06, 5.478764e+06, 6.944114e+06, 6.501289e+06, 6.473109e+06, 6.487715e+06, 5.709612e+06, 4.921987e+06, 6.858955e+06, 6.336869e+06, 6.293741e+06, 6.307894e+06, 6.360832e+06, 7.329096e+06, 6.103368e+06, 6.144082e+06, 5.686581e+06, 6.148549e+06, 6.509854e+06]
    }
    df_x_y = pd.DataFrame(data_x_y)
    df_aglomerado = df.copy()
    df_aglomerado['x_temp'] = None
    df_aglomerado['y_temp'] = None
    df_aglomerado['DISTANCIA'] = None

    # Coordenadas de la capital
    capital_x = 4.193488e+06
    capital_y = 6.144082e+06
    for index, row in df_aglomerado.iterrows():
        eph_codagl = row[aglomerado]
        matching_row = df_x_y[df_x_y['eph_codagl'] == eph_codagl]
        if not matching_row.empty:
            x_temp = matching_row['x'].values[0]
            y_temp = matching_row['y'].values[0]
            distancia = np.sqrt((x_temp - capital_x)**2 + (y_temp - capital_y)**2)
            df_aglomerado.at[index, 'DISTANCIA'] = distancia

    # Eliminar columnas temporales 'x_temp' e 'y_temp'
    df_aglomerado['AGLOMERADO'] = df_aglomerado['DISTANCIA']
    df_aglomerado.drop(columns=['x_temp', 'y_temp', 'DISTANCIA'], inplace=True)
    return df_aglomerado

def save_data(data: pd.DataFrame, data_dir: str, filename: str) -> None:
    repo_path = fh.get_repo_path()
    pr_path = os.path.join(repo_path, data_dir)
    data_path = os.path.join(pr_path, filename)
    data.to_csv(data_path, index=False)
    return None

def preprocesar_data(data: pd.DataFrame, train_test: bool = True) -> pd.DataFrame:
    if len(data) > 1:
        datos = pd.concat(data)
    if len(data) == 1:
        datos = data[0]
    drop_cols = [
        'IV8', 'IX_MAYEQ10', 'CAT_OCUP', 'CAT_INAC', 'CAT_OCUP_jefx', 'JEFE_TRABAJA', 'T_VI', 'V2_M', 'CH04_conyuge', 'CH04_jefx', 'NBI_SUBSISTENCIA', 'IV10', 'II7', 'IV12_1', 'IV12_3', 'PP07I', 
        'PP07H', 'PP02E_jefx', 'REALIZADA_jefx', 'REALIZADA_conyuge',
        'H15', 'ITF', 'REALIZADA'
    ]
    if train_test is True:
        columnas_binarias = [
            'CH11', 'PP02H', 'PP04B1', 'IV5', 'IV12_2', 'II3', 'II4_1', 'II4_2', 'II4_3', 'V1', 'V2', 'V21', 'V22', 'V3', 'V5', 'V6', 'V7', 'V8', 'V11', 'V12', 'V13', 'V14', 'PP07I_jefx', 'PP07H_jefx', 'PP04B1_jefx', 'CONYUGE_TRABAJA', 'JEFA_MUJER', 'HOGAR_MONOP', 'NBI_COBERTURA_PREVISIONAL', 'NBI_DIFLABORAL', 'NBI_HACINAMIENTO', 'NBI_SANITARIA', 'NBI_TENENCIA', 'NBI_TRABAJO_PRECARIO', 'NBI_VIVIENDA', 'NBI_ZONA_VULNERABLE', 'DESERTO', 'MAS_500', 'CH04'
        ]
    if train_test is False:
        columnas_binarias = [
            'CH11', 'PP02H', 'PP04B1', 'IV5', 'IV12_2', 'II3', 'II4_1', 'II4_2', 'II4_3', 'V1', 'V2', 'V21', 'V22', 'V3', 'V5', 'V6', 'V7', 'V8', 'V11', 'V12', 'V13', 'V14', 'PP07I_jefx', 'PP07H_jefx', 'PP04B1_jefx', 'CONYUGE_TRABAJA', 'JEFA_MUJER', 'HOGAR_MONOP', 'NBI_COBERTURA_PREVISIONAL', 'NBI_DIFLABORAL', 'NBI_HACINAMIENTO', 'NBI_SANITARIA', 'NBI_TENENCIA', 'NBI_TRABAJO_PRECARIO', 'NBI_VIVIENDA', 'NBI_ZONA_VULNERABLE', 'MAS_500', 'CH04'
        ]
    data = datos[datos['H15'] == 1]
    data.drop(drop_cols, axis=1, inplace=True)
    data = homogeneizar_binarias(data, columnas_binarias)
    # PP04B1 --> renombre a servicio_domestico + reemplazo de valores
    data.loc[:, 'PP04B1'].replace({2: 0, np.nan: 0}, inplace=True)
    data.rename({'PP04B1': 'servicio_domestico'}, 
                axis=1, inplace=True)
    # PP07H_jefx renombre a apotes_jubilatorios_jefx
    data.rename({'PP07H_jefx': 'APORTES_JUBILATORIOS_jefx'}, 
                axis=1, inplace=True)
    # variables conyuge --> lleno NaN con ceros pues corresponden a HOGAR_MONOP==1
    cvars = data.columns.str.endswith('_conyuge')
    data[data.columns[cvars]] = data.loc[:, cvars].fillna(0)
    data = aglomerados_a_distancia(data)
    return data

def datos_train(anios: list[int],
                trimestres: list[int],
                data_dir: str,
                filename: str,
                save_df: bool = True) -> pd.DataFrame:
    datos, datos_individuos = data_constructor(anios=anios, trimestres=trimestres)
    data = construir_dataset(datos, datos_individuos, trimestres[-1])
    estudiantes = preprocesar_data(data)
    if save_df is True:
        save_data(estudiantes, data_dir=data_dir, filename=filename)
        return None
    if save_df is False:
        return estudiantes

def remover_duplicados(df_list):
    if len(df_list) < 2:
        raise ValueError("df_list debe ser una lista de al menos dos elementos.")
    result_df = df_list[0]
    for df in df_list[1:]:
        result_df = pd.merge(result_df, df[['CODUSU', 'NRO_HOGAR', 'COMPONENTE']], 
                             on=['CODUSU', 'NRO_HOGAR', 'COMPONENTE'], 
                             how='left', indicator=True)
        result_df = result_df[result_df['_merge'] == 'left_only']
        result_df = result_df.drop('_merge', axis=1)

    return result_df

def datos_test(anios: list[int], 
               trimestres: list[int],
               data_dir: str, 
               filename: str,
               train_dataset: str | pd.DataFrame = "preprocessed_train.csv",
               save_df: bool = True) -> pd.DataFrame:
    datos, datos_individuos = data_constructor(anios=anios, trimestres=trimestres)
    data = construir_dataset(datos, datos_individuos, trimestres[-1])
    estudiantes = preprocesar_data(data)
    train_data_path = os.path.join(fh.get_repo_path(), data_dir, train_dataset)
    train_data = pd.read_csv(train_data_path)[['CODUSU', 'NRO_HOGAR', 'COMPONENTE']]
    estudiantes = remover_duplicados([estudiantes, train_data])
    if save_df is True:
        save_data(estudiantes, data_dir=data_dir, filename=filename)
        return None
    if save_df is False:
        return estudiantes

def datos_predict(anios: list[int], 
                  trimestres: list[int],
                  data_dir: str, 
                  filename: str,
                  train_dataset: str | pd.DataFrame = "preprocessed_train.csv",
                  test_dataset: str | pd.DataFrame = "preprocessed_test.csv",
                  save_df: bool = True) -> pd.DataFrame:
    datos, datos_individuos = data_constructor(anios=anios, trimestres=trimestres)
    estudiantes = preprocesar_data(datos, train_test=False)
    train_data_path = os.path.join(fh.get_repo_path(), data_dir, train_dataset)
    test_data_path = os.path.join(fh.get_repo_path(), data_dir, test_dataset)
    train_data = pd.read_csv(train_data_path)[['CODUSU', 'NRO_HOGAR', 'COMPONENTE']]
    test_data = pd.read_csv(test_data_path)[['CODUSU', 'NRO_HOGAR', 'COMPONENTE']]
    estudiantes = remover_duplicados([estudiantes, train_data])
    estudiantes = remover_duplicados([estudiantes, test_data])
    if save_df is True:
        save_data(estudiantes, data_dir=data_dir, filename=filename)
        return None
    if save_df is False:
        return estudiantes


@app.command()
def train(
    anios: str = typer.Option(..., help="List of years"),
    trimestres: str = typer.Option(..., help="List of trimesters"),
    data_dir: str = typer.Option("data/preprocessed/", help="Data directory"),
    filename: str = typer.Option("preprocessed_train.csv", help="Filename"),
    save_df: bool = typer.Option(True, help="Whether to save the DataFrame")
):
    """
    Ejecuta la función datos_train.
    """
    typer.echo("Generando dataset de entrenamiento.")
    anos = list(map(int, anios.split(',')))
    trims = list(map(int, trimestres.split(',')))
    df = datos_train(anos, trims, data_dir, filename, save_df)
    typer.echo("Dataset de entrenamiento generado exitosamente.")

@app.command()
def test(
    anios: str = typer.Option(..., help="List of years"),
    trimestres: str = typer.Option(..., help="List of trimesters"),
    data_dir: str = typer.Option("data/preprocessed/", help="Data directory"),
    filename: str = typer.Option("preprocessed_test.csv", help="Filename"),
    train_dataset: str = typer.Option("preprocessed_train.csv", help="Train dataset filename"),
    save_df: bool = typer.Option(True, help="Whether to save the DataFrame")
):
    """
    Ejecuta la función datos_test.
    """
    typer.echo("Generando dataset de testeo.")
    anos = list(map(int, anios.split(',')))
    trims = list(map(int, trimestres.split(',')))
    df = datos_test(anos, trims, data_dir, filename, train_dataset, save_df)
    typer.echo("Dataset de testeo generado exitosamente.")

@app.command()
def predict(
    anios: str = typer.Option(..., help="List of years"),
    trimestres: str = typer.Option(..., help="List of trimesters"),
    data_dir: str = typer.Option("data/preprocessed/", help="Data directory"),
    filename: str = typer.Option("preprocessed_predict.csv", help="Filename"),
    train_dataset: str= typer.Option("preprocessed_train.csv", help="Train dataset filename"),
    test_dataset: str= typer.Option("preprocessed_test.csv", help="Test dataset filename"),
    save_df: bool = typer.Option(True, help="Whether to save the DataFrame")
):
    """
    Ejecuta la función datos_predict.
    """
    typer.echo("Generando dataset de predicción.")
    anos = list(map(int, anios.split(',')))
    trims = list(map(int, trimestres.split(',')))
    df = datos_predict(anos, trims, data_dir, filename, train_dataset, test_dataset, save_df)
    typer.echo("Dataset de predicción generado exitosamente.")


if __name__ == '__main__':
    app()
