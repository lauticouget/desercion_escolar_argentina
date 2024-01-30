'''
Listas de columnas que se toman sin modificar (salvo posterior transformación de columnas categóricas a variables dummies) y funciones de filtrado.
'''

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

def seleccionar_features(df, 
                        lista_columnas: list, 
                        cols_id: list = None):
    """Selecciona una lista de columnas de la EPH.

    Args:
        df (pandas DataFrame): DataFrame de pandas
        lista_columnas (list): lista de columnas a seleccionar
        info_geo (bool, opcional): True selecciona las columnas de identificación. False por default.

    Returns:
        pandas DataFrame: un DataFrame con las columnas de lista_columnas
    """
    if cols_id is None:
        cols_id = []
    return df[cols_id + lista_columnas]

if __name__ == "__main__":
    import pyeph

    hogar = pyeph.get(data='eph', year=2022, periodo=2, base_type='hogar')

    hogar_filtrada = seleccionar_features(hogar, cols_hogar)
    hogar_filtrada_con_id = seleccionar_features(hogar, cols_hogar, cols_id_hogar)

    print(hogar_filtrada)
    print(hogar_filtrada_con_id)
