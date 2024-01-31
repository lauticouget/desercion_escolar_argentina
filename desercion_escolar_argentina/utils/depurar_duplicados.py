import pandas as pd

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
