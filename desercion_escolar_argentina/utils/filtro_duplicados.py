import pandas as pd

def eliminar_individuos_duplicados(lista_dataframes):
    """Elimina los individuos duplicados entre las bases de datos de la lista.
    
    Parámetros:
        list: Lista de bases de datos que se van a comparar y modificar.

    Retorna:
        list: Lista de bases de datos resultantes después de eliminar duplicados.
    """
    bases_de_datos = lista_dataframes.copy()

    for i, bd in enumerate(bases_de_datos):
        for j, otras_bd in enumerate(bases_de_datos):
            if i != j:  # Evita comparar la bd consigo misma
                bases_de_datos[i] = bd.merge(otras_bd[['CODUSU', 'NRO_HOGAR', 'COMPONENTE']],
                                             how='left', indicator=True).\
                                     query('_merge == "left_only"').drop(columns=['_merge']) # Hace merge con otra bd y luego la descarta

    return bases_de_datos