import pandas as pd
import numpy as np

def unir_personas_hogares(df_individual: pd.DataFrame,
                          df_hogares: pd.DataFrame,
                          sobre: list[str] | None = None,
                          como: str = 'inner') -> pd.DataFrame:
    """Une un dataframe de personas con uno de hogar por las columnas CODUSU y NRO_HOGAR.

    Args:
        df_individual (pd.DataFrame): DataFrame correspondiente a base de individuos.
        df_hogares (pd.DataFrame): DataFrame correspondiente a base de hogares.
        on (list, optional): Lista de columnas para unir. Defaults to ['CODUSU', 'NRO_HOGAR'].

    Returns:
        pd.DataFrame: el dataframe unido por las columnas seleccionadas
    """
    if sobre is None:
        sobre = ['CODUSU', 'NRO_HOGAR', 'ANO4', 'TRIMESTRE', 'REGION','MAS_500', 'AGLOMERADO', 'PONDERA']
    df_unido = pd.merge(df_individual,
                        df_hogares,
                        on=sobre,
                        how=como,
                        suffixes=('', '_r'))
    
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
    data.drop(data.filter(regex='_r$').columns, axis=1, inplace=True)
    return data

def eliminar_individuos_duplicados(base_datos:pd.DataFrame, lista_bases_comparar:list)->pd.DataFrame:
    """Elimina los individuos duplicados entre la base de datos y las bases de datos de la lista.
    
    Parámetros:
        base_datos (pd.DataFrame): Base de datos principal que se va a comparar y modificar.
        lista_bases_comparar (list): Lista de bases de datos que se van a usar para eliminar duplicados.

    Retorna:
        pd.DataFrame: Base de datos resultante después de eliminar duplicados.
    """
    base_depurada = base_datos.copy()

    for otras_bd in lista_bases_comparar:
        base_depurada = base_depurada.merge(otras_bd[['CODUSU', 'NRO_HOGAR', 'COMPONENTE']],
                                                how='left', indicator=True).\
                                query('_merge == "left_only"').drop(columns=['_merge'])

    return base_depurada

def variable_objetivo(bd_inicio: pd.DataFrame, bd_fin: pd.DataFrame, columnas_requeridas: list) -> pd.DataFrame:
    
    """Función que genera la columna target en las bases de datos filtradas,
    con los siguientes valores: no asiste (2), no desertó (1), deserto (0) en cada base de datos.

    Parámetros:
        bd_inicio (pd.DataFrame): DataFrame correspondiente al periodo de inicio.
        bd_fin (pd.DataFrame): DataFrame correspondiente al periodo de fin.
        columnas_requeridas (list): Lista de columnas requeridas en los DataFrames
        ['CODUSU', 'ANO4', 'TRIMESTRE', 'NRO_HOGAR', 'COMPONENTE', 'CH06', 'CH10', 'NIVEL_ED']

    Retorno:
        pd.DataFrame: Retorna un DataFrame con la columna target adjudicada.
    """

    bd_target = pd.merge(left=bd_inicio[columnas_requeridas],
                     right=bd_fin[columnas_requeridas],
                     how='inner',
                     on=['CODUSU', 'NRO_HOGAR', 'COMPONENTE'],
                     suffixes=('_in', '_fin'))

    bd_target['target'] = 2  # asignación inicial

    cond_asistencia = (bd_target['CH10_in'] == 1)  # asiste a la escuela
    cond_desercion = (bd_target['CH10_fin'] == 2)  # asistió a la escuela, pero ya no lo hace
    cond_no_desercion = (bd_target['CH10_fin'] == 1)  # asistió a la escuela, y todavía lo hace

    bd_target.loc[cond_asistencia, 'target'] = 1  # condicion inicial verdadera
    bd_target.loc[cond_asistencia & cond_desercion, 'target'] = 0
    bd_target.loc[cond_asistencia & cond_no_desercion, 'target'] = 1

    return bd_target