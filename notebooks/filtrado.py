import pyeph
import pandas as pd

#Para revision y poder ejecutar y ver resulatados son provisorias las lineasif __name__ == '__main__':  y los print

if __name__ == '__main__':  

    # Obtener bases de datos
    tipo_base = ["hogar", "individual"]
    anios = [2021, 2022, 2023]
    periodos = [2, 3, 4]

    df_hogar_completo = pd.DataFrame()
    df_individual_completo = pd.DataFrame()

    for tipo in tipo_base:
        base_datos_tipo = []  # Lista temporal para almacenar la base de datos por tipo
        for anio in anios:
            if anio != 2023:
                for periodo in periodos: 
                    bd = pyeph.get(data= "eph", year= anio, period= periodo, base_type= tipo)
                    base_datos_tipo.append(bd)  # Agrega el DataFrame a la lista temporal
            elif anio==2023:
                try:
                    bd = pyeph.get(data= "eph", year= anio, period= 2, base_type= tipo)
                    base_datos_tipo.append(bd)
                except:
                    pass
        # Concatenar los DataFrames y agregar al DataFrame completo correspondiente
        if tipo == "hogar":
            df_hogar_completo = pd.concat([df_hogar_completo] + base_datos_tipo, ignore_index=True)
        elif tipo == "individual":
            df_individual_completo = pd.concat([df_individual_completo] + base_datos_tipo, ignore_index=True)
    print( f'Bases de datos originales')
    print( df_hogar_completo.head(5))
    print( df_hogar_completo.shape)
    print( df_individual_completo.head(5))
    print( df_individual_completo.shape)


    # Realizar un "join" basado en las columnas CODUSU, "ANO4", NRO_HOGAR, "TRIMESTRE" y "PONDERA" usando "left"
    df_individual_completo = df_individual_completo.reset_index(drop=True)
    df_hogar_completo = df_hogar_completo.reset_index(drop=True)
    df_final = df_individual_completo.set_index(["CODUSU", "ANO4", "NRO_HOGAR", "TRIMESTRE", "PONDERA"])\
        .join(df_hogar_completo.set_index(["CODUSU", "ANO4", "NRO_HOGAR", "TRIMESTRE", "PONDERA"]), how="left", lsuffix="_ind", rsuffix="_hogar")\
            .reset_index()
    print( f'Bases de datos unida')
    print( df_final.head(5))
    print( df_final.shape)


    # Filtrar por edad y por nivel educativo
    condicion_edad = df_final['CH06'] >= 14
    condicion_nivel = ~df_final['NIVEL_ED'].isin([4, 5, 6, 7, 9])
    df_filtrado_edad_nivel = df_final[condicion_edad & condicion_nivel]
    print( f'Bases de datos filtrada por edad y nivel educativo')
    print( df_filtrado_edad_nivel.head(5))
    print( df_filtrado_edad_nivel.shape)


    # Crear una nueva columna que combine CODUSU y COMPONENTE
    df_filtrado_edad_nivel = df_filtrado_edad_nivel.copy()
    df_filtrado_edad_nivel['CODUSU_COMPONENTE'] = df_filtrado_edad_nivel['CODUSU'] + '_' + df_filtrado_edad_nivel['COMPONENTE'].astype(str)
    print( df_filtrado_edad_nivel.head(5))


    #Funcion filtrar por condición de asistencia
    def filtrar_y_concatenar(df, condiciones_trimestre1, condiciones_trimestre2):
        
        df_resultado = pd.DataFrame()

        df_trimestre1 = df[condiciones_trimestre1]   
        df_trimestre2 = df[condiciones_trimestre2]

        # Realizar el merge por la columna 'CODUSU_COMPONENTE'
        df_merge = pd.merge(df_trimestre1, df_trimestre2, on='CODUSU_COMPONENTE')

        # Dividir el DataFrame en dos partes
        df_parte1 = df_merge.iloc[:, :261]
        df_parte2 = df_merge.iloc[:, 262:]

        # Asignar los nombres originales de las columnas
        df_parte1.columns = df.columns[:261]
        df_parte2.columns = df.columns[:261]

        # Concatenar y reindexar
        df_resultado = pd.concat([df_parte1, df_parte2], ignore_index=True)

        return df_resultado


    # Usar la función "filtrar_y_concatenar" para obtener la base de datos filtrada final
    df_filtrado = pd.DataFrame()

    condiciones_a_considerar = [
        (2021, 2, 2021, 3),
        (2021, 3, 2021, 4),
        (2021, 4, 2022, 2),
        (2022, 2, 2022, 3),
        (2022, 3, 2022, 4)
    ]

    for condiciones in condiciones_a_considerar:

        anio1, trim1, anio2, trim2 = condiciones
        condiciones_trimestre1 = (df_filtrado_edad_nivel['ANO4'] == anio1) & (df_filtrado_edad_nivel['TRIMESTRE'] == trim1) & (df_filtrado_edad_nivel['CH10'] == 1)
        condiciones_trimestre2 = (df_filtrado_edad_nivel['ANO4'] == anio2) & (df_filtrado_edad_nivel['TRIMESTRE'] == trim2) & (df_filtrado_edad_nivel['CH10'] != 1)
        
        df_filtrado = pd.concat([df_filtrado, filtrar_y_concatenar(df_filtrado_edad_nivel, condiciones_trimestre1, condiciones_trimestre2)], ignore_index=True)

    print( f'Bases de datos filtrada por asistencia')  
    print( df_filtrado.head(5))
    print( df_filtrado.shape)