import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import pyeph 

# Diccionario de datos 
años = (2021, 2022)
houses = {}
individuals = {}
for a in años:
    for i in range(1,5):
        houses[f"house_{i}_{a}"] = pyeph.get(data="eph", year=a, period=i, base_type='hogar')
        individuals[f"individual_{i}_{a}"] = pyeph.get(data="eph", year=a, period=i, base_type='individual')
        

# Concatenar los datos en un DataFrame

housesdf = pd.concat(houses.values(), ignore_index=True)
individualsdf = pd.concat(individuals.values(), ignore_index=True)

housesdf.head()
housesdf.tail()
individualsdf.head()
individualsdf.tail()

housesdf.info()
individualsdf.info()

# Unifico los datos en un DataFrame
df = pd.merge(housesdf, individualsdf, on=["CODUSU", "NRO_HOGAR"])

# Crear una nueva columna "id" agrupando por "codusu" y "nro_hogar"
df["id"] = df.groupby(["CODUSU", "NRO_HOGAR"]).ngroup()

# Eliminar filas donde "nro_hogar" sea 51 o 71 (Servicio doméstico en hogares y pensionistas)

df = df.drop(df[df["NRO_HOGAR"].isin([51, 71])].index)


# Creación de variablés de interés

# Indicadores de NBI (pobreza multidimensional)

# Renombrar columnas
# Dimensión vivienda
df.rename(columns={"IV1": "tipo_viv"}, inplace=True) # Tipo de vivienda
df.rename(columns={"IV3": "piso"}, inplace=True) # Piso
df.rename(columns={"IV4": "techo"}, inplace=True) # Techo
df.rename(columns={"IV5": "cielorraso"}, inplace=True) # Cielorraso o revestimiento de techo
df.rename(columns={"II7": "tenencia"}, inplace=True) # Tenencia insegura
df.rename(columns={"IV12_3": "villa"}, inplace=True) # Vivienda en zona vulnerable
df.rename(columns={"IV12_1": "basural"}, inplace=True) # Vivienda en zona de basural
df.rename(columns={"IV10": "baño_descarga"}, inplace=True) # Condiciones sanitarias

# Hacinamiento

df.rename(columns={"IX_TOT": "miembros"}, inplace=True) # Miembros del hogar
df.rename(columns={"IV2": "ambientes"}, inplace=True) # Ambientes de la vivienda


# Crear indicadores de NBI

## nbi1: Vivienda precariedad de los materiales 

df["nbi1"] = np.nan

# nbi1 = 0 si:

df.loc[df["piso"] <= 2, "nbi1"] = 0 # piso = Mosaico/baldosa/madera/cerámica/alfombra/Cemento/ladrillo fijo
df.loc[(df["techo"] <= 3) & (df["cielorraso"] == 1), "nbi1"] = 0
df.loc[(df["techo"] == 4) & (df["cielorraso"] == 1), "nbi1"] = 0
df.loc[(df["techo"] == 5) & (df["cielorraso"] == 1), "nbi1"] = 0

# nbi1 = 1 si:

df.loc[df["piso"] == 3, "nbi1"] = 1  # piso = ladrillo suelto/ tierra y/o 
df.loc[(df["techo"] == 4) & (df["cielorraso"] == 2), "nbi1"] = 1 # techo = techo de chapa de metal sin revestimiento
df.loc[(df["techo"] == 5) & (df["cielorraso"] == 2), "nbi1"] = 1 # techo = techo de chapa de fibra sin revestimiento
df.loc[df["techo"] == 6, "nbi1"] = 1 # techo = techo de cartón
df.loc[df["techo"] == 7, "nbi1"] = 1  # techo = techo de Caña/tabla/paja 

# Generar la variable a nivel hogar:

## nbi2 : Hacinamiento. Hogar con 3 o más personas por cuarto

df["nbi2"] = np.nan

# Crear variable auxiliar miembros/ambientes

df["aux"] = df["miembros"] / df["ambientes"]


#nbi2 = 0 si:
df.loc[(df['aux'] <= 3), 'nbi2'] = 0

#nbi2 = 1 si:
df.loc[(df['aux'] >= 3) & ~df['aux'].isna(), 'nbi2'] = 1

# eliminor variable aux
df.drop('aux', axis=1, inplace=True)

# Generar la variable a nivel hogar:




## nbi3: Tenencia insegura. el hogar ocupa la vivienda sin permiso, o bien sólo es propietario de la vivienda (y no del terreno).

df["nbi3"] = np.nan

#nbi3 = 0 si:

df.loc[df["tenencia"] == 1, "nbi3"] = 0 # tenencia = Propietario de la vivienda y el terreno
df.loc[df["tenencia"] == 3, "nbi3"] = 0  # tenencia = Inquilino/arrendatario de la vivienda
df.loc[df["tenencia"] == 4, "nbi3"] = 0  # tenencia =  Ocupante por pago de impuestos/expensas
df.loc[df["tenencia"] == 5, "nbi3"] = 0  # tenencia =  Ocupante en relación de dependencia
df.loc[df["tenencia"] == 6, "nbi3"] = 0  # tenencia =  Ocupante gratuito/ con permiso
df.loc[df["tenencia"] == 8, "nbi3"] = 0  # tenencia = está en sucesión

#nbi3 = 1 si:

df.loc[df["tenencia"] == 2, "nbi3"] = 1  # tenencia = Propietario de la vivienda y no del terreno
df.loc[df["tenencia"] == 7, "nbi3"] = 1  # tenencia = ocupante de hecho (sin permiso)

# Generar la variable a nivel hogar:

# Total dimensión de la vivienda 

# Individuo
df["nbi_viv_p"] = np.nan

# nbi_viv_p = 0 si:
df.loc[df["nbi1"] == 0, "nbi_viv_p"] = 0
df.loc[df["nbi2"] == 0, "nbi_viv_p"] = 0
df.loc[df["nbi3"] == 0, "nbi_viv_p"] = 0
df.loc[df["nbi1"].isna(), "nbi_viv_p"] = 0
df.loc[df["nbi2"].isna(), "nbi_viv_p"] = 0
df.loc[df["nbi3"].isna(), "nbi_viv_p"] = 0


# nbi_viv_p = 1 si:
df.loc[df["nbi1"] == 1, "nbi_viv_p"] = 1
df.loc[df["nbi2"] == 1, "nbi_viv_p"] = 1
df.loc[df["nbi3"] == 1, "nbi_viv_p"] = 1

df["nbi_viv_p"].value_counts()


# Dimensión habitat y servicios

## nbi4: Condiciones sanitarias. Hogares que no tuvieran ningún tipo de retrete con descarga de agua.

