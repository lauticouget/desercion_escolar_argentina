import pandas as pd
import numpy as np

def unir_personas_hogares(df_individual: pd.DataFrame,
                          df_hogares: pd.DataFrame,
                          sobre: list[str] | None = None,
                          como: str = 'inner',
                          sufijos: tuple[str, str] = ('', '_r')) -> pd.DataFrame:
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
                        suffixes=sufijos)
    return df_unido

def crear_feature_binaria(data: pd.DataFrame,
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
    data.loc[:, nombre_feature] = np.where(condicion, 1.0, 0.0)
    return data
