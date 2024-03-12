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

# Tratamiento de columnas binarias: se identifican NaNs y se convierten a -999, se codifica en 0 y 1


def is_binary_column(values):
    # Determinar si una columna del DataFrame es binaria y cumple con la condicion {0, 1, 4.0, 9.0, 0.0, 1.0}
    unique_values = set(values)
    return unique_values.issubset({0, 1, 4.0, 9.0, 0.0, 1.0})


def convert_binary_features(df, columns):
    df_nominales_binarias = df[columns].copy()

    # Reemplazar valores categorizados con numeros (-9, 4) como faltantes por nan
    for col in columns:
        if is_binary_column(df_nominales_binarias[col]):
            replace_dict = {9.0: -999, 4.0: -999, 9: -999, 4: -999}

        else:
            replace_dict = {}
            if df_nominales_binarias[col].dtype == 'object':
                replace_dict.update(
                    {'1': 1, '2': 0, '9.0': -999, '4.0': -999, 'S': 0, 'N': 1, 'NO': 1})
            elif df_nominales_binarias[col].dtype == 'int64':
                replace_dict.update({1: 1, 2: 0, 9: -999, 4: -999})

            elif df_nominales_binarias[col].dtype == 'float64':
                replace_dict.update(
                    {1.0: 1.0, 2.0: 0.0, 9.0: -999, 4.0: -999})

        df_nominales_binarias[col] = df_nominales_binarias[col].replace(
            replace_dict)

    # Reemplazar los NaN en las columnas 'PP07I', 'PP07H', 'PP04B1' con -999
    df_nominales_binarias[['PP07I', 'PP07H', 'PP04B1']] = df_nominales_binarias[[
        'PP07I', 'PP07H', 'PP04B1']].fillna(-999)

    # Convertir al tipo category
    df_nominales_binarias[columns] = df_nominales_binarias[columns].astype(
        'int64')

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

    for col in columns:
        # Reemplazar valores 9 por -999
        if col in ['CH16', 'CH15', 'CH07']:
            df_nominales_no_binarias[col] = df_nominales_no_binarias[col].replace(
                {9: -999})
        # Conevertir a integer
        df_nominales_no_binarias = df_nominales_no_binarias[columns].astype(
            'int64')

    # Crear variables dummy
    df_nominales_no_binarias = pd.get_dummies(
        df_nominales_no_binarias, columns=columns, drop_first=True)

    return df_nominales_no_binarias


columnas_cat_nominales = [
    'NRO_HOGAR', 'COMPONENTE', 'REGION', 'CH03',
    'CH07', 'CH15', 'CH09', 'CH16', 'ESTADO', 'ESTADO_jefx', 'ESTADO_conyuge',
    'CAT_INAC', 'PP02E', 'PP02E_jefx'
]

df_categoricas_no_binarias = convert_cat_nominal_features(
    df, columnas_cat_nominales)


# Tratamiento de categoricas nominales multiclase especiales: se dejan sin cambios

columnas_nominales = ['NRO_HOGAR', 'COMPONENTE', 'AGLOMERADO']
df_columnas_nominales = df[columnas_nominales].copy()

# Tratamiento de categoricas ordinales


def convert_cat_ordinal_features(df, columns, fill_value=None, non_numeric_code=-999):
    df_ordinales = df[columns].copy()

    # Imputar NaN con fill_value si se especifica
    if fill_value is not None:
        df_ordinales.fillna(fill_value, inplace=True)

    # Convertir a categórica y categorizar con números enteros
    for col in columns:
        df_ordinales[col] = pd.to_numeric(
            df_ordinales[col], errors='coerce')  # Convertir a numérico
        # Máscara para valores no numéricos
        non_numeric_mask = df_ordinales[col].isnull()
        # Reemplazar valores no numéricos con código específico
        df_ordinales.loc[non_numeric_mask, col] = non_numeric_code
        df_ordinales[col] = df_ordinales[col].astype(int)  # Convertir a entero

    return df_ordinales

# Aplicar la función a las columnas ordinales


columnas_cat_ordinales = ['II8', 'IV6', 'IV7', 'IV9', 'IV10', 'IV11', 'CH08', 'TRIMESTRE', 'CAT_OCUP', 'DECINDR',
                          'NIVEL_ED', 'IV1', 'IV3', 'IV4', 'II7', 'DECCFR',  'NIVEL_ED_jefx',
                          'CAT_OCUP_jefx', 'ANO4', 'II9']

df_ordinales_cleaned = convert_cat_ordinal_features(
    df, columnas_cat_ordinales, fill_value=-999)

# Tratamiento de AGLOMERADO: cambia a valor numerico como distancia desde Capital CABA

data_x_y = {
    'eph_codagl': [13, 29, 31, 25, 34, 7, 26, 15, 4, 91, 18, 23, 30, 12, 20, 93, 8, 14, 6, 5, 3, 9, 22, 36, 38, 38, 10, 19, 2, 32, 17, 33, 27],
    'eph_aglome': ['Gran Córdoba', 'Gran Tucumán - Tafi Viejo', 'Ushuaia - Rio Grande', 'La Rioja', 'Mar del Plata - Batán', 'Posadas', 'San Luis - El Chorrillo', 'Formosa', 'Gran Rosario', 'Rawson - Trelew', 'Santiago del Estero - La Banda', 'Salta', 'Santa Rosa - Toay', 'Corrientes', 'Rio Gallegos', 'Viedma - Carmen de Patagones', 'Gran Resistencia', 'Concordia', 'Gran Paraná', 'Gran Santa Fe', 'Bahia Blanca - Cerri', 'Comodoro Rivadavia - Rada Tilly', 'Gran Catamarca', 'Rio Cuarto', 'San Nicolas - Villa Constitiución', 'San Nicolas - Villa Constitiución', 'Gran Mendoza', 'Jujuy - Palpalá', 'Gran La Plata', 'CABA', 'Neuquén - Plottier', 'Partidos del GBA', 'Gran San Juan'],
    'x': [3.668196e+06, 3.575528e+06, 3.368650e+06, 3.433735e+06, 4.238702e+06, 4.500828e+06, 3.470658e+06, 4.290676e+06, 3.989413e+06, 3.561793e+06, 3.671129e+06, 3.558820e+06, 3.652175e+06, 4.215852e+06, 3.274586e+06, 3.754150e+06, 4.194276e+06, 4.258864e+06, 4.023207e+06, 4.008905e+06, 3.824880e+06, 3.382300e+06, 3.520630e+06, 3.656809e+06, 4.035477e+06, 4.029783e+06, 3.231898e+06, 3.560475e+06, 4.234043e+06, 4.193488e+06, 3.310530e+06, 4.180647e+06, 3.260047e+06],
    'y': [6.533650e+06, 7.036009e+06, 3.980855e+06, 6.726538e+06, 5.760505e+06, 6.922012e+06, 6.318389e+06, 7.090830e+06, 6.346344e+06, 5.211965e+06, 6.926946e+06, 7.258796e+06, 5.947417e+06, 6.941437e+06, 4.274342e+06, 5.478764e+06, 6.944114e+06, 6.501289e+06, 6.473109e+06, 6.487715e+06, 5.709612e+06, 4.921987e+06, 6.858955e+06, 6.336869e+06, 6.293741e+06, 6.307894e+06, 6.360832e+06, 7.329096e+06, 6.103368e+06, 6.144082e+06, 5.686581e+06, 6.148549e+06, 6.509854e+06]
}

df_x_y = pd.DataFrame(data_x_y)

# Crear DataFrame de ejemplo
columnas_nominales = ['AGLOMERADO']
df_aglomerado = df[columnas_nominales].copy()

# Agregar columnas temporales 'x_temp' e 'y_temp' a df_aglomerado
df_aglomerado['x_temp'] = None
df_aglomerado['y_temp'] = None
df_aglomerado['DISTANCIA'] = None

# Coordenadas de la capital
capital_x = 4.193488e+06
capital_y = 6.144082e+06

for index, row in df_aglomerado.iterrows():
    eph_codagl = row['AGLOMERADO']
    matching_row = df_x_y[df_x_y['eph_codagl'] == eph_codagl]
    if not matching_row.empty:
        x_temp = matching_row['x'].values[0]
        y_temp = matching_row['y'].values[0]
        distancia = np.sqrt((x_temp - capital_x)**2 + (y_temp - capital_y)**2)
        df_aglomerado.at[index, 'DISTANCIA'] = distancia

# Eliminar columnas temporales 'x_temp' e 'y_temp'
df_aglomerado['AGLOMERADO'] = df_aglomerado['DISTANCIA']
df_aglomerado.drop(columns=['x_temp', 'y_temp', 'DISTANCIA'], inplace=True)
print(df_aglomerado)


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


# Aplicar la función a las columnas numericas
columnas_numericas = ['PONDERA', 'CH06', 'T_VI', 'V2_M', 'IV2', 'II1', 'II2',
                      'IX_TOT', 'IX_MEN10', 'IX_MAYEQ10', 'ITF', 'CH06_jefx', 'ratio_ocupados']
df_numericas = convert_numeric_features(df, columnas_numericas)

columnas_numericas_aglomerado = ['AGLOMERADO']
df_numericas_aglomerado = convert_numeric_features(
    df_aglomerado, columnas_numericas_aglomerado)


# Armado y guardado del dataframe final

if __name__ == '__main__':
    try:
        # Lista de dataframes
        dataframes = [df_categoricas_no_binarias, df_binarias, df_ordinales_cleaned,
                      df_numericas_aglomerado, df_numericas]

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
