import os

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
# from sklearn.metrics import confusion_matrix
# from sklearn.metrics import ConfusionMatrixDisplay
from catboost import CatBoostClassifier

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from desercion_escolar_argentina.utils import file_handler as fh
from desercion_escolar_argentina.artifacts import imputer as im
from desercion_escolar_argentina.artifacts import scaler as sc
from desercion_escolar_argentina.artifacts import encoder as enc


id_cols = [
    'CODUSU', 'NRO_HOGAR', 'COMPONENTE', 'ANO4', 'TRIMESTRE', 'PONDERA'
]

repo_path = fh.get_repo_path()
train_path = os.path.join(repo_path, 'data/preprocessed/', 'preprocessed_train.csv')
test_path = os.path.join(repo_path, 'data/preprocessed/', 'preprocessed_test.csv')
train_data = pd.read_csv(train_path)
train_data = train_data.loc[:, ~train_data.columns.isin(id_cols)]
test_data = pd.read_csv(test_path)
test_data = test_data.loc[:, ~test_data.columns.isin(id_cols)]


X_train = train_data.loc[:, train_data.columns != 'DESERTO']
y_train = train_data.loc[:, train_data.columns == 'DESERTO'].values.ravel()

X_test = test_data.loc[:, test_data.columns != 'DESERTO']
y_test = test_data.loc[:, test_data.columns == 'DESERTO'].values.ravel()


pipeline = Pipeline([
    ('imputer', im.make_imputer()),
    ('scaler', sc.make_scaler()),
    ('encoder', enc.make_encoder()),
    ("reduce_dim", "passthrough"),
    ('classifier', LogisticRegression())
]).set_output(transform='pandas')

n_samples = len(train_data.DESERTO)
n_classes = train_data.DESERTO.nunique()
balanced = n_samples / (n_classes * np.bincount(train_data.DESERTO))
weights = np.linspace(0.01, balanced, 10)
class_weights = [{0: x[0], 1: balanced[1]-x[1]} for x in weights][:-1]
param_grid = [
    {'reduce_dim': [PCA()],
     'reduce_dim__n_components': [10, 20, 30],
     'classifier': [LogisticRegression(penalty='l1', solver='liblinear')],
     'classifier__C': np.logspace(-3, -2, 25),
     'classifier__class_weight': class_weights}
    {'reduce_dim': [PCA()],
     'reduce_dim__n_components': [10, 20, 30],
     'classifier': [DecisionTreeClassifier()],
     'classifier__max_depth': range(8, 36, 2),
     'classifier__class_weight': class_weights},
    {'reduce_dim': [PCA()],
     'reduce_dim__n_components': [10, 20, 30],
     'classifier': [RandomForestClassifier()],
     'classifier__n_estimators': range(8, 38, 2),
     'classifier__class_weight': class_weights}
]

model = GridSearchCV(pipeline, param_grid, scoring='recall', cv=5, verbose=2)
model.fit(X_train, y_train)
results=pd.DataFrame(model.cv_results_)
result_path = os.path.join(repo_path, 'models')
results.to_csv(os.path.join(result_path, 'results_unsampled.csv'))

best = model.best_estimator_
best.fit(X_train, y_train)

with open('model_summary.txt', 'a') as fd:
    fd.write('*--Resumen de mejores modelos--*\n\n')
    fd.write('En data sin resamplear -->')
    fd.write(f'\n{best}. \nSu recall fue de {best.score(X_test, y_test):.2f}\n\n')

resampled_path = os.path.join(repo_path, 'data/stage/')
resampled_data = os.listdir(resampled_path)

cat_features = [
    'REGION', 'CH03', 'CH07', 'CH15', 'CH09', 'CH16', 'ESTADO', 
    'ESTADO_jefx', 'ESTADO_conyuge', 'PP02E', 'CH11', 'PP02H', 'servicio_domestico', 'IV5', 'IV12_2', 'II3', 'II4_1', 'II4_2', 'II4_3', 'V1', 'V2', 'V21', 'V22', 'V3', 'V5', 'V6', 'V7', 'V8', 'V11', 'V12', 'V13', 'V14', 'PP07I_jefx', 'APORTES_JUBILATORIOS_jefx', 'PP04B1_jefx', 'CONYUGE_TRABAJA', 'JEFA_MUJER', 'HOGAR_MONOP', 'NBI_COBERTURA_PREVISIONAL', 'NBI_DIFLABORAL', 'NBI_HACINAMIENTO', 'NBI_SANITARIA', 'NBI_TENENCIA', 'NBI_TRABAJO_PRECARIO', 'NBI_VIVIENDA', 'NBI_ZONA_VULNERABLE', 'MAS_500', 'CH04'
]

cbparams = [
    {'depth': range(6, 11),
     'l2_leaf_reg': np.logspace(-10, 0)}
]

for file in resampled_data:
    filepath = os.path.join(resampled_path, file)
    data = pd.read_csv(filepath)
    train_data = train_data.loc[:, ~train_data.columns.isin(id_cols)]
    X_train = train_data.loc[:, train_data.columns != 'DESERTO']
    y_train = train_data.loc[:, train_data.columns == 'DESERTO'].values.ravel()
    pipeline_resampled = Pipeline([
        ('imputer', im.make_imputer()),
        ('scaler', sc.make_scaler()),
        ('encoder', enc.make_encoder()),
        ("reduce_dim", "passthrough"),
        ('classifier', LogisticRegression())
    ]).set_output(transform='pandas')
    model_resampled = GridSearchCV(pipeline_resampled, param_grid, scoring='recall', cv=5, verbose=2)
    model_resampled.fit(X_train, y_train)
    results_resampled=pd.DataFrame(model_resampled.cv_results_)
    result_path = os.path.join(repo_path, 'models')
    results_resampled.to_csv(os.path.join(result_path, f'results_{file}'))
    best_resampled = model_resampled.best_estimator_
    best_resampled.fit(X_train, y_train)
    with open('model_summary.txt', 'a') as fd:
        fd.write(f'\n\nEn archivo resampleado {file} ---*')
        fd.write(f'\n{best_resampled}. \nSu recall fue de {best_resampled.score(X_test, y_test):.2f}\n\n')
    # catboost
    X_train[cat_features] = X_train[cat_features].astype('object')
    X_test[cat_features] = X_test[cat_features].astype('object')
    cbgrid = GridSearchCV(CatBoostClassifier(), cbparams, scoring='recall', cv=5)
    cbgrid.fit(X_train, y_train)
    best_cb = cbgrid.best_estimator_
    best_cb.fit(X_train, y_train)
    with open('model_summary.txt', 'a') as fd:
        fd.write(f'\n\n CatBoost en archivo resampleado {file} ---*')
        fd.write(f'\n{best_cb}. \nSu recall fue de {best_cb.score(X_test, y_test):.2f}\n\n')






# confusion_matrix = confusion_matrix(y_test, y_pred)
# class_names = ['No desertó', 'Desertó']

# Display = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=class_names)

# Display.plot(cmap=plt.cm.Blues)
# plt.title(f'Matriz de confusión {best})')
# plt.show()