import pandas as pd

def filtrar_edad_nivel_ed(lista_base_datos: list)->list:
    
    """Filtra una lista de bases de datos según las condiciones especificadas: CH06 
    y NIVEL_ED.
    
    Parámetros:
        lista_base_datos (list): Lista de base de datos de inividuos a ser filtradas. 

    Retorna:                
        list: Una lista que contiene las bases de datos originales filtradas con 
        las siguientes columnas: CODUSU, ANO4, TRIMESTRE, NRO_HOGAR, COMPONENTE, 
        CH06, CH10, NIVEL_ED.
    """        

    columnas_requeridas = ['CODUSU', 'ANO4', 'TRIMESTRE', 'NRO_HOGAR', 'COMPONENTE', 'CH06', 'CH10','NIVEL_ED']
    
    lista_bd_filtrada = []

    for bd in lista_base_datos:

        condicion_edad = bd['CH06'] >= 14
        condicion_nivel_ed = bd['NIVEL_ED'] <= 3

        bd_filtrada = bd[columnas_requeridas][condicion_edad & condicion_nivel_ed]

        lista_bd_filtrada.append(bd_filtrada)

    return lista_bd_filtrada

