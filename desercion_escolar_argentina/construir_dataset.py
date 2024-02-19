from utils import descarga as d
from utils import preprocesado as pr
from utils import limpieza as l

import pandas as pd
import numpy as np
import pyeph


def obtener_datos(anios: list[int], trimestres: list[int]):
    bases_individuos = [d.obtener_eph(
        'individual', anio, trimestre) for anio in anios for trimestre in trimestres]
    bases_hogar = [d.obtener_eph('hogar', anio, trimestre)
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
    _jefxs = pd.merge(jefxs, hogares[l.cols_id_hogar], how='outer')
    hogares_jefxs = pd.DataFrame(_jefxs.groupby(l.cols_id_hogar)[[
        'CH04', 'CH06', 'ESTADO', 'NIVEL_ED', 'PP02E', 'CAT_OCUP', 'PP07I', 'PP07H', 'PP04B1']].sum()).reset_index()
    # hogares no monoparentales según género y ocupación del cónyuge
    _conyuges = pd.merge(conyuges, hogares[l.cols_id_hogar], how='outer')
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
                                           como='left',
                                           sufijos=('', '_conyuge'))
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
                    how='left')
    cond = (data.CH10 == 1) & (data.CH10_fin == 2 )
    estudiantes = pr.crear_feature_binaria(data, 'DESERTO', cond)
    estudiantes.drop(['CH10_fin'], axis=1, inplace=True)
    return estudiantes


def construir_dataset(anios: list[str], trimestres: list[str]):
    data, data_individuos, data_hogares = obtener_datos(anios, trimestres)
    # estudiantes de edad >=14
    cond_estudiante = 'CH10 == 1'
    cond_edad = 'CH06 >= 14'
    cond = cond_estudiante + '&' + cond_edad
    estudiantes = [l.filtrar_por_columnas(base, cond) for base in data]
    # ingenieria de atributos
    data = []
    for base, individuos, hogares in zip(estudiantes, data_individuos, data_hogares):
        print('Generando dataframes auxiliares de jefxs y cónyuges.')
        jefxs, conyuges = generar_dataframes_auxiliares(individuos, hogares)
        _base = unir_jefxs_conyuges(base, jefxs, conyuges)
        print('Generando variable JEFX_TRABAJA.')
        _base = generar_jefe_trabaja(_base)
        print('Generando variable CONYUGE_TRABAJA.')
        _base = generar_conyuge_trabaja(_base)
        print('Generando variable JEFA_MUJER.')
        _base = generar_jefa_mujer(_base)
        print('Generando variable HOGAR_MONOP.')
        _base = generar_hogar_monop(_base)
        print('Generando variable ratio_ocupado.')
        _base = generar_ratio_ocupados_miembros(_base, individuos, hogares)
        print('Generando variables NBI.')
        print('NBI_SUBSISTENCIA.')
        _base = generar_nbi_subsistencia(_base)
        print('NBI_COBERTURA_PREVISIONAL.')
        _base = generar_nbi_cobertura_previsional(_base)
        print('NBI_DIFLABORAL.')
        _base = generar_nbi_dificultad_laboral(_base)
        print('NBI_HACINAMIENTO.')
        _base = generar_nbi_hacinamiento(_base)
        print('NBI_SANITARIA.')
        _base = generar_nbi_sanitaria(_base)
        print('NBI_TENENCIA.')
        _base = generar_nbi_tenencia(_base)
        print('NBI_TRABAJO_PRECARIO.')
        _base = generar_nbi_trabajo_precario(_base)
        print('NBI_VIVIENDA_PRECARIA.')
        _base = generar_nbi_vivienda_precaria(_base)
        print('NBI_ZONA_VULNERABLE.')
        _base = generar_nbi_zona_vulnerable(_base)
        data.append(_base)
    
    estudiantes = []
    for base, base_p1 in zip(data[:-1], data_individuos[1:]):
        _base = generar_deserto(base, base_p1)
        estudiantes.append(_base[_base.TRIMESTRE != 4])
    return estudiantes


if __name__ == '__main__':
    datos = construir_dataset(anios=[2021, 2022], trimestres=[2, 3, 4])
    names = ['data212', 'data213', 'data214', 'data222', 'data223', 'data224']
    for df, name in zip(datos, names):
        path = '~/desercion_escolar_argentina/data/preprocessed/' + name + '.csv'
        df.to_csv(path)
    
    data = pd.concat(datos)
    data_path = '~/desercion_escolar_argentina/data/preprocessed/preprocessed.csv'
    data.to_csv(data_path)
