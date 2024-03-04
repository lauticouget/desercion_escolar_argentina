import pyeph
import pandas as pd
import os

def obtener_eph(tipo: str, anio: int, periodo: int) -> pd.DataFrame:
    
    """Obtiene una base de datos para un tipo específico, año y periodo dado.

    Parámetros:
        tipo (str): Tipo de base de datos ("hogar" o "individual").
        anio (int): Año para el cual se desea obtener la base de datos.
        periodo (int): Periodo o trimestre para el cual se desea obtener la base de datos (1, 2, 3, 4).

    Retorna:
        pd.DataFrame: Un DataFrame que contiene la base de datos correspondiente al tipo, año y periodo especificados.
    """
    try:
        data = pyeph.get(data="eph", year=anio, period=periodo, base_type=tipo)
        return data
    except ValueError as e:
        print(f"Error obteniendo base de datos para {tipo}, año {anio}, periodo {periodo}: {e}")
        return pd.DataFrame()

def get_repo_path():
    file_path = os.path.dirname(__file__)
    utils_path = os.path.dirname(file_path)
    repo_path = os.path.dirname(utils_path)
    return repo_path