import numpy as np
import pandas as pd
import pyeph 



# Se define el script que tome los datos de lista_base_datos: 

def generar_nbi(houses, individuals):
    

    """ Construcción de indicadores nbi en base al enfoque de probreza multidimensional
    
    Parámetros:
        lista_base_datos (list): Lista de base de datos de hogares e individuos
    Retorna:                
        list: Una lista que contiene las bases de datos originales agregando
        las siguientes columnas: 

    Columnas: 
        "IV1" : Tipo de vivienda
        "IV3" : Piso 
        "IV4" : Techo
        "IV5" : Cielorraso o revestimiento de techo
        "II7" : Tenencia insegura
        "IV12_3" : Vivienda en zona vulnerable
        "IV12_1" : Vievienda en proximidad a basural
        "IV10" : Condiciones sanitarias
        "IX_TOT" :  Miembros del hogar
        "IV2" : ambientes de la vivienda
        "PP02E" : Durante esos 30 días, no buscó trabajo
        "PP07I" : ¿Aporta por sí mismo a algún sistema jubilatorio?
        "PP07H" : ¿Por ese trabajo tiene descuento jubilatorio?
        "PP04B1" : Si presta servicio doméstico en hogares particulares
        "V2_M" : Monto por jubilación o pensión percibido en ese mes
        
        

    Definiciones de las nbi:

        # Dimensión vivienda.
        nbi_1: Precariedad de los materiales de la vivienda
        nbi_2 : Hacinamiento. Hogar con 3 o más personas por cuarto 
        nbi_3: Tenencia insegura. El hogar ocupa la vivienda sin permiso, o bien sólo es propietario de la vivienda (y no del terreno).

        # Dimensión habitat y servicios.
        nbi_4: Condiciones sanitarias. Hogares que no tuvieran ningún tipo de retrete con descarga de agua.
        nbi_5: vivienda en zona vulnerable.

        # Dimensión empleo y protección social. 
        nbi6: Dificultades de acceder a empleo remunerado.
        nbi7: Precariedad laboral.
        nbi: Cobertura previsional
        nbi: Capacidad de subsitencia

    """        

    lista_bd_nbi = []


    for bd_hogares, bd_individuos in zip(houses, individuals):    
        
            bd = pd.merge(bd_hogares, bd_individuos, on= ['CODUSU','NRO_HOGAR'], how='inner')
            
            bd['id'] = bd.groupby(['CODUSU', 'NRO_HOGAR']).ngroup()

        
            # Crear indicadores de NBI

            ## Dimensión vivienda


            bd["nbi_1"] = np.nan

            # nbi_1 = 0 si:

            bd.loc[bd["IV3"] <= 2, "nbi_1"] = 0 # piso = Mosaico/baldosa/madera/cerámica/alfombra/Cemento/ladrillo fijo
            bd.loc[(bd["IV4"] <= 3) & (bd["IV5"] == 1), "nbi_1"] = 0
            bd.loc[(bd["IV4"] == 4) & (bd["IV5"] == 1), "nbi_1"] = 0
            bd.loc[(bd["IV4"] == 5) & (bd["IV5"] == 1), "nbi_1"] = 0

            # nbi_1 = 1 si:

            bd.loc[bd["IV3"] == 3, "nbi_1"] = 1  # piso = ladrillo suelto/ tierra y/o 
            bd.loc[(bd["IV4"] == 4) & (bd["IV5"] == 2), "nbi_1"] = 1 # techo = techo de chapa de metal sin revestimiento
            bd.loc[(bd["IV4"] == 5) & (bd["IV5"] == 2), "nbi_1"] = 1 # techo = techo de chapa de fibra sin revestimiento
            bd.loc[bd["IV4"] == 6, "nbi_1"] = 1 # techo = techo de cartón
            bd.loc[bd["IV4"] == 7, "nbi_1"] = 1  # techo = techo de Caña/tabla/paja 



            bd["nbi_2"] = np.nan

            # Crear variable auxiliar miembros/ambientes

            bd["aux"] = bd["IX_TOT"] / bd["IV2"]


            #nbi_2 = 0 si:
            bd.loc[(bd['aux'] <= 3), 'nbi_2'] = 0

            #nbi_2 = 1 si:
            bd.loc[(bd['aux'] >= 3) & ~bd['aux'].isna(), 'nbi_2'] = 1

            # eliminor variable aux
            bd.drop('aux', axis=1, inplace=True)


            bd["nbi_3"] = np.nan

            #nbi_3 = 0 si:

            bd.loc[bd["II7"] == 1, "nbi_3"] = 0 # Propietario de la vivienda y el terreno
            bd.loc[bd["II7"] == 3, "nbi_3"] = 0  # Inquilino/arrendatario de la vivienda
            bd.loc[bd["II7"] == 4, "nbi_3"] = 0  # Ocupante por pago de impuestos/expensas
            bd.loc[bd["II7"] == 5, "nbi_3"] = 0  # Ocupante en relación de dependencia
            bd.loc[bd["II7"] == 6, "nbi_3"] = 0  # Ocupante gratuito/ con permiso
            bd.loc[bd["II7"] == 8, "nbi_3"] = 0  # Está en sucesión

            #nbi_3 = 1 si:

            bd.loc[bd["II7"] == 2, "nbi_3"] = 1  #  Propietario de la vivienda y no del terreno
            bd.loc[bd["II7"] == 7, "nbi_3"] = 1  #  ocupante de hecho (sin permiso)




            ### Total dimensión de la vivienda 

            # Individuo
            bd["nbi_viv"] = 0
            
            bd.loc[(bd["nbi_1"] == 1) | (bd["nbi_2"] == 1) | (bd["nbi_3"] == 1), "nbi_viv"] = 1 
            bd.loc[(bd["nbi_1"].isna() ) & (bd["nbi_2"].isna()) & (bd["nbi_3"].isna()), "nbi_viv"] = np.nan
                        

            ## Dimensión habitat y servicios


            bd["nbi_4"] = np.nan

            #nbi_4 = 0 si:

            bd.loc[bd["IV10"] == 1, "nbi_4"] = 0   # Inodoro con botón/ mochila/ cadena y arrastre de agua

            #nbi_4 = 1 si:

            bd.loc[bd["IV10"] == 2, "nbi_4"] = 1   # Inodoro sin botón/cadena y con arrastre de agua (a balde)
            bd.loc[bd["IV10"] == 3, "nbi_4"] = 1   # Letrina (sin arrastre de agua)




            bd["nbi_5"] = np.nan

            #nbi_5 = 0 si:

            bd.loc[bd["IV12_3"] == 2, "nbi_5"] = 0    # Vivienda no esta ubicada en villa de emergencia
            bd.loc[bd["IV12_1"] == 2, "nbi_5"] = 0   # Vivienda no esta ubicada en zona de basural

            # nbi_5 = 1 si:

            bd.loc[bd["IV12_3"] == 1, "nbi_5"] = 1    # Vivienda esta ubicada en zona vulnerable
            bd.loc[bd["IV12_1"] == 1, "nbi_5"] = 1   # Vivienda esta ubicada en zona de basural




            ### Total dimensión habitat y servicios

            # individuo
            bd["nbi_hab"] = 0
            
            bd.loc[(bd["nbi_4"] == 1) | (bd["nbi_5"] == 1) , "nbi_hab"] = 1 
            bd.loc[(bd["nbi_4"].isna() ) & (bd["nbi_5"].isna()) , "nbi_hab"] = np.nan

            
            
            
            
            # Dimensión empleo y protección social
            
            # Dificultades para acceder a empleo remunerado
            
            bd["nbi_6"] = np.nan
            
            # nbi_6 = 0 si:
            
            bd.loc[(bd["CH06"].between(16, 59)) & (bd["CH04"] == 1) & ((bd["ESTADO"] == 1) | (bd["ESTADO"] == 3) | ((bd["PP02E"] == 1) | (bd["PP02E"] == 2) | (bd["PP02E"] == 4))), "nbi_6"] = 0  # Hombre

            
            bd.loc[(bd["CH06"].between(16, 64)) & (bd["CH04"] == 2) & ((bd["ESTADO"] == 1) | (bd["ESTADO"] == 3) | ((bd["PP02E"] == 1) | (bd["PP02E"] == 2) | (bd["PP02E"] == 4))), "nbi_6"] = 0  # Mujer

            # nbi_6 = 1 si:
            
            bd.loc[(bd["CH06"].between(16, 59)) & (bd["CH04"] == 2) & ((bd["ESTADO"] == 2) | ((bd["PP02E"] == 3) | (bd["PP02E"] == 5))), "nbi_6"] = 1  # Mujer

            
            bd.loc[(bd["CH06"].between(16, 64)) & (bd["CH04"] == 1) & ((bd["ESTADO"] == 2) | (bd["PP02E"] == 3) | (bd["PP02E"] == 5)), "nbi_6"] = 1 
            # Hombre

            
            
            # Precariedad laboral.
            # Considera a toda aquella persona ocupada que no es un asalariado registrado, patrón o empleador, trabajador por cuenta propia de calificación profesional o técnica; dejando, así a los trabajadores por cuenta propia de calificación operativa o carentes de calificación (de los que se asume que no realizan aportes a la seguridad social), a los asalariados no registrados y al personal de servicio doméstico.
            
            
            bd["nbi_7"] = np.nan
            
            # nbi_7 = 0 si:
            
            bd.loc[(bd["CAT_OCUP"] == 2) & (bd["NIVEL_ED"].between(4, 6)), "nbi_7"] = 0
            # Cuenta propista con secundario completo o universitario
            
            bd.loc[(bd["PP07I"] == 1) | (bd["PP07H"] == 1), "nbi_7"] = 0    # tiene descuento por aporte jubilatorio o aporta por si mismo
            
            bd.loc[(bd["PP04B1"] == 1 ) & ((bd["PP07I"] == 1) | (bd["PP07H"] == 1)), "nbi_7"] = 0  # Presta servicio domestico en hogares particulares y  tiene descuento por aporte jubilatorio o aporta por si mismo
            
            
            # nbi_7 = 1 si:
            
            bd.loc[(bd["CAT_OCUP"] == 2) & ((bd["NIVEL_ED"] <= 3) | (bd["NIVEL_ED"] == 7)), "nbi_7"] = 1

            # Ocupado con educación secundario incompleta o nivel educativo menor      
            
            bd.loc[(bd["PP07I"] == 2) | (bd["PP07H"] == 2), "nbi_7"] = 1 # No tiene descuento jubilatorio o no aporta por sí mismo
            
            bd.loc[(bd["PP04B1"] == 1 ) & ((bd["PP07I"] == 2) | (bd["PP07H"] == 2)), "nbi_7"] = 1 # Presta servicio domestico en hogares particulares y  No tiene descuento jubilatorio o no aporta por sí mismo
            
            

            # *Cobertura previsional.
            
            #V2_M: monto percibido por jubilacion/pension
            

            bd["nbi_8"] = np.nan

            # nbi_8 = 0 si: 
            
            bd.loc[(bd["CH06"] >= 65) & (bd["CH06"].notna()) & (bd["CH04"] == 1) & (bd["V2_M"] >= 0) & (bd["V2_M"].notna()), "nbi_8"] = 0

            bd.loc[(bd["CH06"] >= 60) & (bd["CH06"].notna()) & (bd["CH04"] == 0) & (bd["V2_M"] >= 0) & (bd["V2_M"].notna()), "nbi_8"] = 0
            
            # nbi_8 = 1 si:

            bd.loc[(bd["CH06"] >= 65) & (bd["CH06"].notna()) & (bd["CH04"] == 1) & (bd["V2_M"] == 0) & (bd["V2_M"].notna()), "nbi_8"] = 1

            bd.loc[(bd["CH06"] >= 60) & (bd["CH06"].notna()) & (bd["CH04"] == 0) & (bd["V2_M"] == 0) & (bd["V2_M"].notna()), "nbi_8"] = 1

            
            
            
            # Capacidad de subsistencia.  Hogares que tuvieran 4 o más personas por miembro  ocupado y, además, cuyo jefe tuviera baja educación (primaria incompleta).
            
            bd["nbi_9"] = np.nan
            
            # Auxiliar variable ocupados por grupo id
            bd["ocupado"] = 0
            bd.loc[bd["ESTADO"] == 1, "ocupado"] = 1
            
            bd["n_ocupados"] = bd.groupby('id')['ocupado'].transform(pd.Series.sum)
            
            # Auxiliar ratio de ocupados por grupo
            
            bd["aux_ratio"] = bd["IX_TOT"] / bd["n_ocupados"]
            
            # Jefe de hogar
            
            bd["jefe_hogar"] = 0
            bd.loc[bd["CH03"] == 1, "jefe_hogar"] = 1
            
            # Auxiliar 
                        
            bd["aux"] = 0
            bd.loc[(bd["jefe_hogar"] == 1) & (bd["NIVEL_ED"].between(2, 6)), "aux"] = 1
            bd.loc[(bd["jefe_hogar"] == 1) & ((bd["NIVEL_ED"] == 1) | (bd["NIVEL_ED"] == 7)), "aux"] = 1

            # Crear la variable edu_jefe por grupo id
            bd["edu_jefe"] = bd.groupby('id')['aux'].transform(pd.Series.sum)

            # nbi_9 = 1 si:
            bd.loc[(bd["aux_ratio"] >= 4) & (bd["edu_jefe"] > 0), "nbi_9"] = 1

            # Eliminar columnas auxiliares
            bd = bd.drop(columns=["aux", "aux_ratio", "jefe_hogar", "ocupado", "n_ocupados"]) # No borro la columna edu_jefe pero se puede borrar si es necesario
            
            
            ### Total dimensión empleo y protección social
            
            bd["nbi_empleo"] = 0


            bd.loc[(bd["nbi_6"] == 1) | (bd["nbi_7"] == 1) | (bd["nbi_8"] == 1) | (bd["nbi_9"] == 1), "nbi_empleo"] = 1 
            bd.loc[(bd["nbi_6"].isna()) & (bd["nbi_7"].isna()) & (bd["nbi_8"].isna()) & (bd["nbi_9"].isna()), "nbi_empleo"] = np.nan
            
            
            lista_bd_nbi.append(bd)
            
    return lista_bd_nbi

        
