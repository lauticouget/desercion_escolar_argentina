import os

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer

from desercion_escolar_argentina.utils import file_handler as fh

columnas_cat_nominales = [
    'REGION', 'CH03', 'CH07', 'CH15', 'CH09', 'CH16', 'ESTADO', 
    'ESTADO_jefx', 'ESTADO_conyuge', 'PP02E'
]

def make_encoder(cols = None):
    if cols is None:
        cols = columnas_cat_nominales
    ohencoder = make_column_transformer(
        (OneHotEncoder(drop='first', 
                       sparse_output=False,
                       handle_unknown='infrequent_if_exist'), cols),
        remainder='passthrough',
        verbose_feature_names_out=False
    )
    return ohencoder


if __name__ == '__main__':
    repo_path = fh.get_repo_path()
    data_path = os.path.join(repo_path, 'data', 'preprocessed',
                             'preprocessed_train.csv')
    data = pd.read_csv(data_path)
    encoder = make_encoder()
    encoder.fit_transform(data)
    encoded = pd.DataFrame(encoder.fit_transform(data), 
                           columns=encoder.get_feature_names_out())
    save_path = os.path.join(repo_path, 'data', 'preprocessed',
                             'preprocessed_train_encoded.csv')
    encoded.to_csv(save_path, index=False)
