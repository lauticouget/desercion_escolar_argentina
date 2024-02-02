import pyeph


def obtener_lista_base_datos(tipo: str, anios: list, periodos: list) ->list:
    """Obtiene una lista de bases de datos para un tipo específico, años y periodos dados.

    Parámetros:
        tipo (str): Tipo de base de datos ("hogar" o "individual").
        anios (list): Lista de años para los cuales se desea obtener las bases de datos.
        periodos (list): Lista de periodos o tambien llamados trimestres para los cuales 
        se desea obtener las bases de datos (1, 2, 3, 4).

    Retorna:
        list: Una lista que contiene las bases de datos correspondientes al tipo, años y 
        periodos especificados.
    """
    lista_base_datos = []

    for anio in anios:
        if anio == anio:
            try:
                for periodo in periodos:
                     bd = pyeph.get(data="eph", year=anio, period=periodo, base_type=tipo)
                     lista_base_datos.append(bd)

            except Exception as e:
                print(f"Error obteniendo base de datos para {tipo}, año {anio}, periodo: {e}")

    return lista_base_datos

