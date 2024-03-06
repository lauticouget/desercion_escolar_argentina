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

    # Reemplazar valores categorizados con numeros (-9, 4) como faltantes por 0
    for col in columns:
        if is_binary_column(df_nominales_binarias[col]):
            # replace_dict = {9.0: np.nan, 4.0: np.nan}
            replace_dict = {9.0: 0, 4.0: 0}
        else:
            replace_dict = {}
            if df_nominales_binarias[col].dtype == 'object':
                replace_dict.update(
                    {'1': 1, '2': 0, '9.0': 0, '4.0': 0, 'S': 0, 'N': 1, 'NO': 1})
            elif df_nominales_binarias[col].dtype == 'int64':
                replace_dict.update({1: 1, 2: 0, 9: 0, 4: 0})

            elif df_nominales_binarias[col].dtype == 'float64':
                replace_dict.update(
                    {1.0: 1.0, 2.0: 0.0, 9.0: 0.0, 4.0: 0.0})

        df_nominales_binarias[col] = df_nominales_binarias[col].replace(
            replace_dict)

    # Reemplazar los NaN en las columnas 'PP07I', 'PP07H', 'PP04B1' con 0
    df_nominales_binarias[['PP07I', 'PP07H', 'PP04B1']] = df_nominales_binarias[[
        'PP07I', 'PP07H', 'PP04B1']].fillna(0)

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

    # Crear variables dummy
    df_nominales_no_binarias = pd.get_dummies(
        df_nominales_no_binarias, columns=columns)

    return df_nominales_no_binarias


columnas_cat_nominales = [
    'REGION', 'CH03', 'CH07', 'CH15', 'CH16',
    'ESTADO', 'CAT_INAC', 'PP02E', 'PP02E_jefx'
]

df_categoricas_no_binarias = convert_cat_nominal_features(
    df, columnas_cat_nominales)

# Tratamiento de categoricas nominales multiclase especiales: se dejan sin cambios

columnas_nominales = ['NRO_HOGAR', 'COMPONENTE', 'AGLOMERADO']
df_columnas_nominales = df[columnas_nominales].copy()

# Tratamiento de numericas: se identifican NaNs se imputa en principio la media y se escala con una estandarizaciòndelo datos


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
        dataframes = [df_columnas_nominales,
                      df_categoricas_no_binarias, df_binarias, df_numericas]

        # Concatenar los dataframes
        data = pd.concat(dataframes, axis=1)

       # Obtener la ruta del directorio base del proyecto
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.abspath(os.path.join(
            base_dir, '..', 'data', 'preprocessed'))

        # Guardar el archivo en el directorio
        output_file_path = os.path.join(
            data_dir, 'preprocessed_codificacion.csv')
        data.to_csv(output_file_path, index=False)
        print(f"Archivo guardado en {output_file_path}")

    except Exception as e:
        print(f"Error: {e}")
