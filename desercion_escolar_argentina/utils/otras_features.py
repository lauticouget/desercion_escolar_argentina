import pyeph
import pandas as pd
import numpy as np

def unir_presonas_hogares(df_individual: pd.DataFrame,
                          df_hogares: pd.DataFrame,
                          sobre: list = ['CODUSU', 'NRO_HOGAR']) -> pd.DataFrame:
    """Une un dataframe de personas con uno de hogar por las columnas CODUSU y NRO_HOGAR.

    Args:
        df_individual (pd.DataFrame): DataFrame correspondiente a base de individuos.
        df_hogares (pd.DataFrame): DataFrame correspondiente a base de hogares.
        on (list, optional): Lista de columnas para unir. Defaults to ['CODUSU', 'NRO_HOGAR'].

    Returns:
        pd.DataFrame: el dataframe unido por las columnas seleccionadas
    """
    df_unido = pd.merge(df_individual,
                        df_hogares,
                        on=sobre,
                        how='left')
    
    return df_unido

def crear_feature_binaria(df: pd.DataFrame,
                          nombre_feature: str,
                          condicion: pd.Series) -> pd.DataFrame:
    """Crea una feature categórica binaria según si se cumple una condición en las columnas del dataframe pasado como argumento.

    Args:
        df(pd.DataFrame): DataFrame al cual agregar la variable
        nombre_feature (str): nombre de la variable
        condicion (pd.Series): máscara booleana

    Returns:
        pd.DataFrame: un DataFrame con la columna categórica de nombre 'nombre_feature'
    """
    data = df.copy()
    data.loc[:, nombre_feature] = np.where(condicion, 1, 0)
    return data

if __name__ == '__main__':
    # dataframe de estudiantes que desertaron en el tercer trimestre de 2021
    hogares21_2 = pyeph.get(data="eph", year=2021, period=2, base_type='hogar')
    individuos21_2 = pyeph.get(data="eph", year=2021, period=2, base_type='individual')

    hogares21_3 = pyeph.get(data="eph", year=2021, period=3, base_type='hogar')
    individuos21_3 = pyeph.get(data="eph", year=2021, period=3, base_type='individual')

    cols = ['CODUSU', 'NRO_HOGAR', 'COMPONENTE', 'CH06', 'CH10', 'NIVEL_ED']
    # uno los dataframes por CODUSU, NRO_HOGAR y COMPONENTE
    _data = pd.merge(left=individuos21_2[cols],
                      right=individuos21_3[cols],
                      how='inner',
                      on=['CODUSU', 'NRO_HOGAR', 'COMPONENTE'],
                      suffixes=('_t2', '_t3'))

    cond_edad = 'CH06_t2 >= 4' # inicio de la educación obligatoria
    cond_asistencia = 'CH10_t2 == 1' # asiste a la escuela
    cond_desercion = 'CH10_t3 == 2' # asistió a la escuela, pero ya no lo hace
    cond_nivel = 'NIVEL_ED_t3 <= 3' # educación secundaria incompleta

    desertados21_3 = _data.query(f'{cond_edad} & {cond_asistencia} & {cond_desercion} & {cond_nivel}')

    # variables categóricas: JEFE_TRABAJA, JEFA_MUJER, HOGAR_MONOP, CONYUGE_TRABAJA

    # dataframes de jefxs de hogares y cónyuges
    jefxs_mask = individuos21_2.CH03 == 1
    conyuge_mask = individuos21_2.CH03 == 2
    jefxs = individuos21_2[jefxs_mask].loc[:, ['CODUSU', 'NRO_HOGAR', 'COMPONENTE', 'ESTADO', 'CH04']]
    conyuges = individuos21_2[conyuge_mask].loc[:, ['CODUSU', 'NRO_HOGAR', 'COMPONENTE', 'ESTADO', 'CH04']]
    
    # hogares por estado de ocupación del jefx
    jefxs = pd.DataFrame(jefxs.groupby(['CODUSU', 'NRO_HOGAR'])['ESTADO', 'CH04'].sum()).reset_index()
    # hogares no monoparentales según género y ocupación del cónyuge
    hogar_no_mono = pd.DataFrame(conyuges.groupby(['CODUSU', 'NRO_HOGAR'])[['ESTADO', 'CH04']].sum()).reset_index()
    
    # variables JEFE_TRABAJA y JEFA_MUJER
    data = unir_presonas_hogares(desertados21_3, jefxs)
    jefe_trabaja_cond = data.ESTADO == 1
    jefe_trabaja = crear_feature_binaria(data, 'JEFE_TRABAJA', jefe_trabaja_cond)

    jefa_mujer_cond = data.CH04 == 2
    jefa_mujer = crear_feature_binaria(data, 'JEFA_MUJER', jefa_mujer_cond)

    print('Estado de ocupación del jefx de hogar de las personas que dejaron sus estudios entre el segundo y tercer trimestre de 2021.')
    print(jefe_trabaja.JEFE_TRABAJA.value_counts(normalize=True))

    print('Distribución de desertados según género del jefx de hogar.')
    print(jefa_mujer.JEFA_MUJER.value_counts(normalize=True))

    # HOGAR_MONOP
    data = unir_presonas_hogares(desertados21_3, hogar_no_mono)
    cond_hogar_monop = data[['ESTADO']].isna()
    hogar_monop = crear_feature_binaria(data, 'HOGAR_MONOP', cond_hogar_monop)

    print('Distribución de desertados según hogar monoparental o no.')
    print(hogar_monop.HOGAR_MONOP.value_counts(normalize=True))

    # variable CONYUGE_TRABAJA
    data = unir_presonas_hogares(desertados21_3, hogar_no_mono)
    cond_conyuge_trabaja = data.ESTADO == 1
    conyuge_trabaja = crear_feature_binaria(data, 'CONYUGE_TRABAJA', cond_conyuge_trabaja)

    print('Distribución de desertados según condición laboral del cónyuge de hogar.')
    print(conyuge_trabaja.CONYUGE_TRABAJA.value_counts(normalize=True))