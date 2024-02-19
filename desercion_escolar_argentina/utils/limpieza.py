import pandas as pd

cols_id_hogar = [
    'CODUSU', 'NRO_HOGAR', 'REALIZADA', 'ANO4', 'TRIMESTRE', 'REGION', 'MAS_500', 'AGLOMERADO', 'PONDERA'
]

cols_hogar = [
    'IV1', 'IV2', 'IV3', 'IV4', 'IV5', 'IV6', 'IV7', 'IV8', 'IV9', 'IV10', 'IV11', 'IV12_1', 'IV12_2', 'IV12_3', 'II1', 'II2', 'II3', 'II4_1', 'II4_2', 'II4_3', 'II7', 'II8', 'II9', 'V1', 'V2', 'V21', 'V22', 'V3', 'V5', 'V6', 'V7', 'V8', 'V11', 'V12', 'V13', 'V14', 'IX_TOT', 'IX_MEN10', 'IX_MAYEQ10', 'ITF', 'DECCFR'
]

cols_id_individual = [
    'CODUSU', 'NRO_HOGAR', 'COMPONENTE', 'H15', 'ANO4', 'TRIMESTRE',  'REGION', 'MAS_500', 'AGLOMERADO', 'PONDERA'
]

cols_individual = [
    'CH03', 'CH04', 'CH06', 'CH07', 'CH08', 'CH09', 'CH10', 'CH11', 'CH15', 'CH16', 'ESTADO', 'CAT_OCUP', 'CAT_INAC', 'PP02E', 'PP02H', 'PP07I', 'PP07H', 'PP04B1', 'DECINDR', 'T_VI', 'NIVEL_ED', 'V2_M'
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
        lista_columnas = data.columns
    data_filtrada = data.query(filtro)[lista_columnas]
    return data_filtrada


def remover_duplicados(lista_df: list[pd.DataFrame]):
    if len(lista_df) < 2:
        raise ValueError("La lista debe tener al menos dos DataFrames.")

    result_df = lista_df[0]

    # iterar sobre los siguientes dataframes
    for df in lista_df[1:]:
        # unir los dataframes
        result_df = pd.merge(result_df, df[['CODUSU', 'NRO_HOGAR', 'COMPONENTE']], 
                             on=['CODUSU', 'NRO_HOGAR', 'COMPONENTE'], 
                             how='left', indicator=True)

        # Filtrar filas a izquierda
        result_df = result_df[result_df['_merge'] == 'left_only']

        # droppear columna _merge
        result_df = result_df.drop('_merge', axis=1)

    return result_df

