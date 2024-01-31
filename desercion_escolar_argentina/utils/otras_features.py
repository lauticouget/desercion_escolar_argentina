import pyeph
import pandas as pd
import numpy as np

def unir_presonas_hogares(df_individual: pd.DataFrame,
                          df_hogares: pd.DataFrame,
                          sobre: list = ['CODUSU', 'NRO_HOGAR']):
    """Une un dataframe de personas con uno de hogar por las columnas CODUSU y NRO_HOGAR.

    Args:
        df_individual (pd.DataFrame): _description_
        df_hogares (pd.DataFrame): _description_
        on (list, optional): _description_. Defaults to ['CODUSU', 'NRO_HOGAR'].

    Returns:
        df_unido: _description_
    """
    df_unido = pd.merge(df_individual,
                        df_hogares,
                        on=sobre,
                        how='left')
    
    return df_unido

def crear_feature_binaria(df: pd.DataFrame,
                          nombre_feature: str,
                          condicion: str):
    """Crea una feature categórica binaria según si se cumple una condición en las columnas del dataframe pasado como argumento.

    Args:
        df(pd.DataFrame): _description_
        nombre_feature (str): _description_
        condicion (str): _description_

    Returns:
        _type_: _description_
    """
    data = df.loc[:, nombre_feature] = np.where(condicion, 1, 0)
    return data