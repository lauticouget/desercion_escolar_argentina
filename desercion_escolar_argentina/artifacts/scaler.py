import os

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer

from desercion_escolar_argentina.utils import file_handler as fh

# Tratamiento de numericas: se identifican NaNs se imputa en principio la media y se escala con una estandarizaciòndelo datos

columnas_numericas = ['AGLOMERADO', 'CH06', 'IV2', 'II2', 'IX_TOT', 
                      'IX_MEN10', 'CH06_jefx', 'ratio_ocupados']

def make_scaler(cols = None):
    if cols == None:
        cols = columnas_numericas
    stdscaler = make_column_transformer(
        (StandardScaler().set_output(transform='pandas'), cols),
        remainder='passthrough',
        verbose_feature_names_out=False   
    )
    return stdscaler.set_output(transform='pandas')


if __name__ == '__main__':
    repo_path = fh.get_repo_path()
    data_path = os.path.join(repo_path, 'data', 'preprocessed',
                             'preprocessed_train.csv')
    data = pd.read_csv(data_path)
    scaler = make_scaler()
    scaler.fit_transform(data)
    scaled = pd.DataFrame(scaler.fit_transform(data), 
                           columns=scaler.get_feature_names_out())
    save_path = os.path.join(repo_path, 'data', 'preprocessed',
                             'preprocessed_train_scaled.csv')
    scaled.to_csv(save_path, index=False)
