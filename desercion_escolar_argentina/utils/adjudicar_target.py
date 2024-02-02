import pandas as pd

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
