from utils import descarga as d
from utils import preprocesado as pr
from utils import limpieza as l

import pandas as pd
import pyeph

def obtener_datos(anios: int | list[int], 
                  trimestres: int | list[int]):
    bases_individuos = [d.obtener_eph('individual', anio, trimestre)
                        for anio in anios for trimestre in trimestres]

    data_individuos = [l.seleccionar_features(base,
                                            l.cols_individual,
                                            l.cols_id_individual)
                    for base in bases_individuos]
    bases_hogar = [d.obtener_eph('hogar', anio, trimestre)
                for anio in anios for trimestre in trimestres]

    data_hogares = [l.seleccionar_features(base,
                                        l.cols_hogar,
                                        l.cols_id_hogar)
                    for base in bases_hogar]
    data = [pr.unir_personas_hogares(individuos, hogares)
            for individuos, hogares in zip(data_individuos, data_hogares)]
    return data

def generar_dataframes_auxiliares(data: list[pd.DataFrame]):
    jefxs_masks = [base.CH03 == 1 for base in data]
    conyuges_masks = [base.CH03 == 2 for base in data]
    jefxs = [base[mascara] for base, mascara in zip(data, jefxs_masks)]
    conyuges = [base[mascara] for base, mascara in zip(data, conyuges_masks)]
    # hogares por estado de ocupación del jefx
    hogares_jefxs = [pd.DataFrame(base.groupby(l.cols_id_hogar)[[
                              'ESTADO', 'CH04']].sum()).reset_index()
                              for base in jefxs]
    # hogares no monoparentales según género y ocupación del cónyuge
    hogares_no_mono = [pd.DataFrame(base.groupby(l.cols_id_hogar)
                                    [['ESTADO', 'CH04']].sum()).reset_index() 
                       for base in conyuges]
    return hogares_jefxs, hogares_no_mono

def generar_jefe_trabaja(estudiantes,
                         hogares_jefxs):
    estudiantes = [pr.unir_personas_hogares(db_estudiantes, db_jefxs) 
                   for db_estudiantes, db_jefxs 
                   in zip(estudiantes, hogares_jefxs)]
    jefe_trabaja_conds = [base.ESTADO_r == 1 for base in estudiantes]
    estudiantes = [pr.crear_feature_binaria(base, 'JEFE_TRABAJA', cond) 
                   for base, cond in zip(estudiantes, jefe_trabaja_conds)]
    return estudiantes

def generar_jefa_mujer(estudiantes,
                       hogares_jefxs):
    estudiantes = [pr.unir_personas_hogares(db_estudiantes, db_jefxs) 
                   for db_estudiantes, db_jefxs 
                   in zip(estudiantes, hogares_jefxs)]
    jefa_mujer_conds = [base.CH04_r == 2 for base in estudiantes]
    estudiantes = [pr.crear_feature_binaria(base, 'JEFA_MUJER', cond) 
                   for base, cond in zip(estudiantes, jefa_mujer_conds)]
    return estudiantes

def generar_hogar_monop(estudiantes,
                        hogares_no_mono):
    estudiantes = [pr.unir_personas_hogares(db_estudiantes,
                                            db_no_mono,
                                            como='left')
                   for db_estudiantes, db_no_mono
                   in zip(estudiantes, hogares_no_mono)]
    conds_hogar_monop = [base.ESTADO_r.isna() for base in estudiantes]
    estudiantes = [pr.crear_feature_binaria(base, 'HOGAR_MONOP', cond) 
                   for base, cond in zip(estudiantes, conds_hogar_monop)]
    return estudiantes

def generar_conyuge_trabaja(estudiantes,
                            hogares_no_mono):
    estudiantes = [pr.unir_personas_hogares(db_estudiantes,
                                            db_no_mono,
                                            como='left')
                   for db_estudiantes, db_no_mono
                   in zip(estudiantes, hogares_no_mono)]
    conds_conyuge_trabaja = [base.ESTADO_r == 1 for base in estudiantes]
    estudiantes = [pr.crear_feature_binaria(base, 'CONYUGE_TRABAJA', cond) 
                   for base, cond in zip(estudiantes, conds_conyuge_trabaja)]
    return estudiantes

def construir_dataset(anios, trimestres):
    data = obtener_datos(anios, trimestres)
    # estudiantes de edad >=14
    cond_estudiante = 'CH10 == 1'
    cond_edad = 'CH06 >= 14'
    cond = cond_estudiante + '&' + cond_edad
    estudiantes = [l.filtrar_por_columnas(base, cond) for base in data]
    # ingenieria de atributos
    hogares_jefxs, hogares_no_mono = generar_dataframes_auxiliares(data)
    estudiantes = generar_jefe_trabaja(estudiantes, hogares_jefxs)
    estudiantes = generar_jefa_mujer(estudiantes, hogares_jefxs)
    estudiantes = generar_hogar_monop(estudiantes, hogares_no_mono)
    estudiantes = generar_conyuge_trabaja(estudiantes, hogares_no_mono)

    return estudiantes

if __name__ == '__main__':
    data = construir_dataset(anios=[2021, 2022], trimestres=[2, 3, 4])
    names = ['data212', 'data213', 'data214', 'data222', 'data223', 'data224']
    for df, name in zip(data, names):
        path = '~/desercion_escolar_argentina/data/preprocessed/' + name + '.csv'
        df.to_csv(path)