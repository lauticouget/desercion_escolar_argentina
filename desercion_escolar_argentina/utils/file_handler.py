import os
import requests
from io import BytesIO
import zipfile

import pyeph
import pandas as pd

URL_BASE_INDEC = 'https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/'

def eph_desde_indec(tipo: str, anio: int, periodo: int, url_base=URL_BASE_INDEC) -> pd.DataFrame:
    url = f'{url_base}' + 'EPH_usu_' + f'{periodo}' + '_Trim_' + f'{anio}' + '_txt.zip'
    response = requests.get(url, timeout=100)
    if response.status_code != 200:
        print("No se encuentra el archivo")
        return None
    with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
        # Get the list of file names in the zip file
        file_names = zip_file.namelist()
        file_name = [name for name in file_names if f'{tipo}' in name][0]
        with zip_file.open(file_name) as file:
            df = pd.read_csv(file, sep=';', header=0)
    return df

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
    except pyeph.errors.NonExistentDBError:
        try: 
            data = eph_desde_indec(tipo, anio, periodo)
            return data
        except zipfile.BadZipFile:
            print('No existe la base solicitada.')
            return None

def get_repo_path():
    file_path = os.path.dirname(__file__)
    utils_path = os.path.dirname(file_path)
    repo_path = os.path.dirname(utils_path)
    return repo_path