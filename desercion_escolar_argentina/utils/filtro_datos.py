import pandas as pd

def filtrar_edad_nivel_ed(base_datos: pd.DataFrame) -> pd.DataFrame:
    
    """Filtra una base de datos según las condiciones especificadas: CH06 y NIVEL_ED.

    Parámetros:
        base_datos (pd.DataFrame): DataFrame de individuos a ser filtrado.
    
    Retorna:
        pd.DataFrame: Un DataFrame resultante después de aplicar los filtros con las 
        siguientes columnas: CODUSU, ANO4, TRIMESTRE, NRO_HOGAR, COMPONENTE, CH06, CH10, NIVEL_ED.
    """

    columnas_requeridas = ['CODUSU', 'ANO4', 'TRIMESTRE', 'NRO_HOGAR', 'COMPONENTE', 'CH06', 'CH10', 'NIVEL_ED']

    # Condiciones de filtro
    condicion_edad = base_datos['CH06'] >= 14
    condicion_nivel_ed = base_datos['NIVEL_ED'] <= 3

    # Aplicar los filtros y seleccionar las columnas requeridas
    base_filtrada = base_datos[condicion_edad & condicion_nivel_ed][columnas_requeridas]

    return base_filtrada
