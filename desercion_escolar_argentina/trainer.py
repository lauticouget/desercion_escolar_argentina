import os

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from catboost import CatBoostClassifier

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from desercion_escolar_argentina.utils import file_handler as fh
from desercion_escolar_argentina.artifacts import imputer as im
from desercion_escolar_argentina.artifacts import scaler as sc
from desercion_escolar_argentina.artifacts import encoder as enc

def _resample(df, target_col, kind='up'):
    df_1 = df[df[target_col] == 1]
    df_0 = df[df[target_col] == 0]
    if kind == 'up':
        resampled = resample(df_1, replace=True, n_samples=len(df_0), random_stat=42)
        return pd.concat(df_0, resampled)
    if kind == 'down':
        resampled = resample(df_0, replace=True, n_samples=len(df_1), random_stat=42)
        return pd.concat(df_1, resampled)
    return None

id_cols = [
    'CODUSU', 'NRO_HOGAR', 'COMPONENTE', 'ANO4', 'TRIMESTRE', 'PONDERA'
]

repo_path = fh.get_repo_path()
data_path = os.path.join(repo_path, 'data', 'preprocessed', 'preprocessed_train.csv')
data = pd.read_csv(data_path)
data = data.loc[:, ~data.columns.isin(id_cols)]
print(f'El shape del dataframe es {data.shape}.')


X = data.loc[:, data.columns != 'DESERTO']
y = data.loc[:, data.columns == 'DESERTO'].values.ravel()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=99, stratify=y)

pipeline = Pipeline([
    ('imputer', im.make_imputer()),
    ('scaler', sc.make_scaler()),
    ('encoder', enc.make_encoder()),
    ('classifier', LogisticRegression())
])

n_samples = len(data.DESERTO)
n_classes = data.DESERTO.nunique()
balanced = n_samples / (n_classes * np.bincount(data.DESERTO))
weights = np.linspace(0., balanced, 10)
class_weights = [{0: x[0], 1: x[1]} for x in weights]
param_grid = [
    {'classifier': [LogisticRegression(solver='liblinear')],
     'classifier__penalty': ['passthrough', 'l1'],
     'classifier__class_weight': class_weights},
    {'classifier': [KNeighborsClassifier()],
     'classifier__n_neighbors': range(2, 15),
     'classifier__weights': ['uniform', 'distance']},
    {'classifier': [DecisionTreeClassifier()],
     'classifier__max_depth': range(8, 36, 2),
     'classifier__criterion': ['gini', 'entropy'],
     'classifier__class_weight': class_weights},
    {'classifier': [RandomForestClassifier()],
     'classifier__n_estimators': range(8, 36, 2),
     'classifier__criterion': ['gini', 'entropy'],
     'classifier__class_weight': class_weights},
    {'classifier': [BaggingClassifier(estimator=DecisionTreeClassifier())],
     'classifier__n_estimators': range(2, 20, 2),
     'classifier__estimator__class_weight': class_weights,
     'classifier__estimator__criterion': ['gini', 'entropy'],
     'classifier__estimator__max_depth': range(8, 36, 4)}
    # {'classifier': [CatBoostClassifier()],
    #  'classifier__iterations': [100, 200, 300],
    #  'classifier__depth': range(4, 10),
    #  'classifier__verbose': [False]}
]

model = GridSearchCV(pipeline, param_grid, scoring=['recall', 'f1'], cv=5, verbose=2, refit='f1')
model.fit(X_train, y_train)
results=pd.DataFrame(model.cv_results_)
result_path = os.path.join(repo_path, 'models')
results.to_csv(os.path.join(result_path, 'results.csv'))
print(model.best_estimator_)

# mejor modelo
best = model.best_estimator_
print(f'El mejor modelo fue {best}).')
# entrenamiento
best.fit(X_train, y_train)
# performance
y_pred = best.predict(X_test)
print(f'El recall del mejor modelo en el set de test es: {best.score(X_test, y_test):.2f}')

confusion_matrix = confusion_matrix(y_test, y_pred)
class_names = ['No desertó', 'Desertó']

Display = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=class_names)

Display.plot(cmap=plt.cm.Blues)
plt.title(f'Matriz de confusión {best})')
plt.show()

# importances = best.named_steps['classifier'].feature_importances_
# feature_importances = pd.Series(importances, index=data.columns[:-1])
# feature_importances.sort_values(ascending=True, inplace=True)
# print(feature_importances[-20:])

# fig, ax = plt.subplots()
# feature_importances.plot(kind='barh', ax=ax)
# ax.set_title("Feature importances using MDI")
# ax.set_ylabel("Mean decrease in impurity")
# fig.tight_layout()
# plt.show()