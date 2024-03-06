import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler

# Obtener la ruta del directorio base del proyecto
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(
    base_dir, '..', 'data', 'preprocessed'))

# Guardar el archivo en el directorio
file_path = os.path.join(data_dir, 'preprocessed_dataset.csv')

# Cargar el archivo CSV en un DataFrame
df = pd.read_csv(file_path)

# Tratamiento de columnas binarias: se identifican NaNs y se codifican en 0 y 1


def is_binary_column(values):
    # Determinar si una columna del DataFrame es binaria y cumple con la condicion {0, 1, 4.0, 9.0, 0.0, 1.0}
    unique_values = set(values)
    return unique_values.issubset({0, 1, 4.0, 9.0, 0.0, 1.0})


def convert_binary_features(df, columns):
    df_nominales_binarias = df[columns].copy()

    # Reemplazar valores categorizados con numeros (-9, 4) como faltantes por nan
    for col in columns:
        if is_binary_column(df_nominales_binarias[col]):
            replace_dict = {9.0: np.nan, 4.0: np.nan}

        else:
            replace_dict = {}
            if df_nominales_binarias[col].dtype == 'object':
                replace_dict.update(
                    {'1': 1, '2': 0, '9.0': np.nan, '4.0': np.nan, 'S': 0, 'N': 1, 'NO': 1})
            elif df_nominales_binarias[col].dtype == 'int64':
                replace_dict.update({1: 1, 2: 0, 9: np.nan, 4: np.nan})

            elif df_nominales_binarias[col].dtype == 'float64':
                replace_dict.update(
                    {1.0: 1.0, 2.0: 0.0, 9.0: np.nan, 4.0: np.nan})

        df_nominales_binarias[col] = df_nominales_binarias[col].replace(
            replace_dict)

    # Reemplazar los NaN en las columnas 'PP07I', 'PP07H', 'PP04B1' con 0
    df_nominales_binarias[['PP07I', 'PP07H', 'PP04B1']] = df_nominales_binarias[[
        'PP07I', 'PP07H', 'PP04B1']].fillna(np.nan)

    # Convertir al tipo category
    df_nominales_binarias[columns] = df_nominales_binarias[columns].astype(
        'category')

    return df_nominales_binarias


columnas_binarias = [
    'H15', 'CH11', 'PP02H', 'PP07I', 'PP07H', 'PP04B1', 'REALIZADA', 'IV5', 'IV8',
    'IV12_1', 'IV12_2', 'IV12_3', 'II3', 'II4_1', 'II4_2', 'II4_3', 'V1', 'V2',
    'V21', 'V22', 'V3', 'V5', 'V6', 'V7', 'V8', 'V11', 'V12', 'V13', 'V14',
    'REALIZADA_jefx', 'CH04_jefx', 'PP07I_jefx', 'PP07H_jefx', 'PP04B1_jefx',
    'REALIZADA_conyuge', 'CH04_conyuge', 'JEFE_TRABAJA', 'CONYUGE_TRABAJA',
    'JEFA_MUJER', 'HOGAR_MONOP', 'NBI_SUBSISTENCIA', 'NBI_COBERTURA_PREVISIONAL',
    'NBI_DIFLABORAL', 'NBI_HACINAMIENTO', 'NBI_SANITARIA', 'NBI_TENENCIA',
    'NBI_TRABAJO_PRECARIO', 'NBI_VIVIENDA', 'NBI_ZONA_VULNERABLE', 'DESERTO',
    'MAS_500', 'CH04'
]

df_binarias = convert_binary_features(df, columnas_binarias)

# Tratamiento de categoricas nominales multiclase: se pasan a dummies


def convert_cat_nominal_features(df, columns):
    df_nominales_no_binarias = df[columns].copy()

    # Conevertir a categorica
    df_nominales_no_binarias = df_nominales_no_binarias[columns].astype(
        'category')

    return df_nominales_no_binarias


columnas_cat_nominales = [
    'NRO_HOGAR', 'COMPONENTE', 'AGLOMERADO', 'REGION', 'CH03',
    'CH07', 'CH15', 'CH16', 'ESTADO', 'CAT_INAC', 'PP02E', 'PP02E_jefx'
]

df_categoricas_no_binarias = convert_cat_nominal_features(
    df, columnas_cat_nominales)

# Tratamiento de categoricas ordinales


def convert_cat_ordinal_features(df, columns):
    df_ordinales = df[columns].copy()

    # Conevertir a categorica
    df_ordinales = df_ordinales[columns].astype(
        'category')

    return df_ordinales


columnas_cat_ordinales = ['II8', 'IV6', 'IV7', 'IV9', 'IV10', 'IV11', 'CH08', 'TRIMESTRE', 'CAT_OCUP', 'DECINDR',
                          'NIVEL_ED', 'IV1', 'IV3', 'IV4', 'II7', 'DECCFR', 'ESTADO_jefx', 'NIVEL_ED_jefx',
                          'CAT_OCUP_jefx', 'ANO4', 'II9', 'ESTADO_conyuge']

df_ordinales = convert_cat_ordinal_features(
    df, columnas_cat_ordinales)


# Tratamiento de numericas: se identifican NaNs se imputa la media y se escala con una estandarizaciòndelo datos
"""CatBoost trata los valores NaN como una categoría separada y los procesa. También 
se puede usar el parámetro nan_mode = Zero (solo dejarìa esa opcion para las categoricas)
"""


def convert_numeric_features(df, columns):
    df_numericas = df[columns].copy()

    for col in columns:
        # Reemplazar valores -9 y 99 por NaN
        if col in ['T_VI', 'V2_M', 'IV2', 'II1', 'II2']:
            df_numericas[col] = df_numericas[col].replace(
                {-9: np.nan, 99: np.nan})

    # Imputar los valores faltantes con la mediana de cada columna (se puede elegir otro metodo depende de distribuciòn)
    df_numericas = df_numericas.fillna(df_numericas.median())

    # Instanciar el StandardScaler
    scaler = StandardScaler()

    # Escalar las columnas numéricas
    df_numericas_scaled = pd.DataFrame(scaler.fit_transform(
        df_numericas), columns=df_numericas.columns)

    return df_numericas_scaled


columnas_numericas = ['PONDERA', 'CH06', 'T_VI', 'V2_M', 'IV2', 'II1', 'II2',
                      'IX_TOT', 'IX_MEN10', 'IX_MAYEQ10', 'ITF', 'CH06_jefx', 'ratio_ocupados']

df_numericas = convert_numeric_features(df, columnas_numericas)


# Armado y guardado del dataframe final

if __name__ == '__main__':
    try:
        # Lista de dataframes
        dataframes = [
            df_categoricas_no_binarias, df_binarias, df_ordinales,
            df_numericas]

        # Concatenar los dataframes
        data = pd.concat(dataframes, axis=1)

       # Obtener la ruta del directorio base del proyecto
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.abspath(os.path.join(
            base_dir, '..', 'data', 'preprocessed'))

        # Guardar el archivo en el directorio
        output_file_path = os.path.join(
            data_dir, 'preprocessed_codificacion_catboost.csv')
        data.to_csv(output_file_path, index=False)
        print(f"Archivo guardado en {output_file_path}")

    except Exception as e:
        print(f"Error: {e}")
