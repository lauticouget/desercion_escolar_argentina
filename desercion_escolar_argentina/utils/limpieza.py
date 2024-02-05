import pandas as pd

cols_id_hogar = [
    'CODUSU', 'NRO_HOGAR', 'REALIZADA', 'ANO4', 'TRIMESTRE', 'REGION','MAS_500', 'AGLOMERADO', 'PONDERA'
]

cols_hogar = [
    'IV1', 'IV2', 'IV3', 'IV4', 'IV5', 'IV6', 'IV7', 'IV8', 'IV9', 'IV10','IV11', 'IV12_1', 'IV12_2', 'IV12_3', 'II1', 'II2', 'II3','II4_1', 'II4_2', 'II4_3', 'II7', 'II8', 'II9', 'V1', 'V2', 'V21', 'V22', 'V3', 'V5', 'V6', 'V7', 'V8', 'V11', 'V12', 'V13','V14', 'IX_TOT', 'IX_MEN10','IX_MAYEQ10', 'ITF', 'DECCFR'
]

cols_id_individual = [
    'CODUSU','NRO_HOGAR', 'COMPONENTE', 'H15', 'ANO4', 'TRIMESTRE',  'REGION','MAS_500', 'AGLOMERADO', 'PONDERA'
]

cols_individual = [
    'CH03', 'CH04', 'CH06', 'CH07', 'CH08', 'CH09', 'CH11', 'CH15', 'CH16', 'ESTADO', 'CAT_OCUP', 'CAT_INAC', 'PP02E', 'PP02H', 'DECINDR', 'T_VI'
]

def seleccionar_features(data, 
                         lista_columnas: list, 
                         cols_id: list = None):
    """Selecciona una lista de columnas de la EPH.

    Args:
        df (pandas DataFrame): DataFrame de pandas
        lista_columnas (list): lista de columnas a seleccionar
        cols_id (lista, opcional): lista de columnas identificatorias. None por default.

    Returns:
        pandas DataFrame: un DataFrame con las columnas de lista_columnas
    """
    if cols_id is None:
        cols_id = []
    return data[cols_id + lista_columnas]

def filtrar_por_columnas(data: pd.DataFrame, 
                         filtro: str, 
                         lista_columnas: list = None) -> pd.DataFrame:
    """Filtra una base de datos según los filtros pasados como argumento usando el método query de pandas. Devuelve la base filtrada con las columnas requeridas por lista_columnas.

    Args:
        data (pd.DataFrame): base de datos a filtrar.
        filtro (str): filtros por columnas.
        lista_columnas (list): lista de columnas que devuelve la función. Por default devuelve la base completa.

    Returns:
        pd.DataFrame: _description_
    """
    if lista_columnas is None:
        lista_columnas=data.columns
    data_filtrada = data.query(filtro)[lista_columnas]
    return data_filtrada

def eliminar_duplicados(base_datos:pd.DataFrame, lista_bases_comparar:list)->pd.DataFrame:
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