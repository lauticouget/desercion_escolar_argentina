import pandas as pd

def variable_objetivo(lista: list, periodos_requeridos: list, columnas_requeridas:list) -> list:
    
    """Funcion que genera la columna target en las bases de datos filtradas,
    con los siguientes valores no asiste: 2, no desertó: 1, deserto:0 en cada base de datos.
   
    Parámetros:
        lista (list): recibe una lista de bases de datos filtrada.
        periodos_requeridos (list): Lista de tuplas indicando los dos periodos inicial y final por año y periodo:
        [((2021, 2), (2021, 3)), ((2021, 3), (2021, 4)), ((2021, 2), (2021, 3)), ((2021, 3), (2021, 4))]
        columnas_requeridas (list): Lista de años para los cuales se desea obtener las bases de datos:
        ['CODUSU', 'ANO4', 'TRIMESTRE', 'NRO_HOGAR', 'COMPONENTE', 'CH06', 'CH10', 'NIVEL_ED']

    Retorno:
        list: Retorna una lista de base de datos con el target adjudicado
    """    
    
    bases_datos_target = []

    for periodo_inicio, periodo_fin in periodos_requeridos:
        
        bd_inicio = None #comprobar si existen las bd
        bd_fin = None

        for bd in lista:
            if (bd['ANO4'].iloc[0] == periodo_inicio[0] and bd['TRIMESTRE'].iloc[0] == periodo_inicio[1]):
                bd_inicio = bd.copy()  
            elif (bd['ANO4'].iloc[0] == periodo_fin[0] and bd['TRIMESTRE'].iloc[0] == periodo_fin[1]):
                bd_fin = bd.copy() 

        if bd_inicio is not None and bd_fin is not None: #comprobar si existen las bd
            _data = pd.merge(left=bd_inicio[columnas_requeridas],
                            right=bd_fin[columnas_requeridas],
                            how='inner',
                            on=['CODUSU', 'NRO_HOGAR', 'COMPONENTE'],
                            suffixes=('_in', '_fin'))

            _data['target'] = 2 #asignacion inicial

            cond_asistencia = (_data['CH10_in'] == 1)  # asiste a la escuela
            cond_desercion = (_data['CH10_fin'] == 2)  # asistió a la escuela, pero ya no lo hace
            cond_no_desercion = (_data['CH10_fin'] == 1)  # asistió a la escuela, y todavía lo hace

            _data.loc[cond_asistencia , 'target'] = 1 #condicion incial verdadera
            _data.loc[cond_asistencia & cond_desercion, 'target'] = 0  
            _data.loc[cond_asistencia & cond_no_desercion, 'target'] = 1

            bases_datos_target.append(_data)

    return bases_datos_target