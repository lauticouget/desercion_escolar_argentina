import os

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score

import pandas as pd
import numpy as np

from desercion_escolar_argentina.utils import file_handler as fh
from desercion_escolar_argentina.artifacts import imputer as im
from desercion_escolar_argentina.artifacts import scaler as sc
from desercion_escolar_argentina.artifacts import encoder as enc


id_cols = [
    'CODUSU', 'NRO_HOGAR', 'COMPONENTE', 'ANO4', 'TRIMESTRE', 'PONDERA'
]

repo_path = fh.get_repo_path()
train_path = os.path.join(
    repo_path, "data/stage/df_resampled_.csv"
)
test_path = os.path.join(repo_path, 'data/preprocessed/preprocessed_test.csv')
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

param_grid = [
    {'classifier': [LogisticRegression(penalty='l1', solver='liblinear')],
     'classifier__C': np.logspace(-3.5, -2, 25),
     'classifier__class_weight': ['balanced', None]},
    {'classifier': [DecisionTreeClassifier()],
     'classifier__max_depth': range(8, 38, 4),
     'classifier__class_weight': ['balanced', None]},
    {'classifier': [RandomForestClassifier()],
     'classifier__n_estimators': range(8, 38, 4),
     'classifier__class_weight': ['balanced', None]},
    {'classifier': [BaggingClassifier(
        estimator=LogisticRegression(penalty='l1', solver='liblinear'))],
     'classifier__n_estimators': range(10, 32, 2),
     'classifier__estimator__class_weight': ['balanced', None],
     'classifier__estimator__C': np.linspace(0.0025, 0.01, 25)}
]

model = GridSearchCV(pipeline, param_grid, scoring='f1', cv=5, verbose=2)
model.fit(X_train, y_train)
results=pd.DataFrame(model.cv_results_)
result_path = os.path.join(repo_path, 'models')
results.to_csv(os.path.join(result_path, 'results_AllKNN.csv'))


best = model.best_estimator_
y_pred = best.predict(X_test)

with open('model_summary.txt', 'a', encoding='UTF-8') as fd:
    # fd.write('*--Resumen de mejores modelos--*\n\n')
    fd.write('\n\nEn data resampleada con AllKNN-->')
    fd.write(f'\n{best}. \nSu f1_score fue de {f1_score(y_test, y_pred):.2f}\n\n')
