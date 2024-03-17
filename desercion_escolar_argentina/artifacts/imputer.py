import os

import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.compose import make_column_transformer

from desercion_escolar_argentina.utils import file_handler as fh

cols9 = ['CH07', 'CH08', 'CH11', 'V1', 
        'V2', 'V3', 'V5', 'V6', 'V7', 'V8', 'V11', 'V12', 
        'V13', 'V14', 'PP07I_jefx']

cols99 = ['IV2', 'II1']

col12 = ['DECCFR']

def make_imputer(c9 = None, c99 = None, c12 = None):
    if c9 is None:
        c9 = cols9
    if c99 is None:
        c99 = cols99
    if c12 is None:
        c12 = col12    
    knnimputer = make_column_transformer(
        (KNNImputer(n_neighbors=1, missing_values=9.), c9),
        (KNNImputer(n_neighbors=1, missing_values=99.), c99),
        (KNNImputer(n_neighbors=1, missing_values=12.), c12),
        remainder='passthrough',
        verbose_feature_names_out=False
    )
    return knnimputer

if __name__ == "__main__":
    repo_path = fh.get_repo_path()
    data_path = os.path.join(repo_path, 'data', 'preprocessed',
                             'preprocessed_train.csv')
    data = pd.read_csv(data_path)
    imputer = make_imputer(cols9, cols99, col12)
    imputer.fit_transform(data)
    imputed = pd.DataFrame(imputer.fit_transform(data), 
                           columns=imputer.get_feature_names_out()).round(0)
    save_path = os.path.join(repo_path, 'data', 'preprocessed',
                             'preprocessed_train_imputed.csv')
    imputed.to_csv(save_path, index=False)
