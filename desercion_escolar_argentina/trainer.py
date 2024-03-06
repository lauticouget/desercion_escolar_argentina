import os

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from desercion_escolar_argentina.utils import file_handler as fh

cols = [
        'CH03', 'CH04', 'CH06', 'CH07', 'CH08', 'CH09', 'CH10', 'CH11', 'CH15', 'CH16', 'ESTADO', 'CAT_OCUP', 'CAT_INAC', 'PP02E', 'PP02H', 'PP07I', 'PP07H', 'PP04B1', 'DECINDR', 'T_VI', 'NIVEL_ED', 'V2_M', 'NBI_SUBSISTENCIA', 'NBI_COBERTURA_PREVISIONAL', 'NBI_DIFLABORAL',
        'NBI_HACINAMIENTO', 'NBI_SANITARIA', 'NBI_TENENCIA',
        'NBI_TRABAJO_PRECARIO', 'NBI_VIVIENDA', 'NBI_ZONA_VULNERABLE', 'HOGAR_MONOP', 'IX_TOT', 'IX_MEN10', 'IX_MAYEQ10', 'DESERTO'
]

repo_path = fh.get_repo_path()
data_path = os.path.join(repo_path, 'data', 'preprocessed', 'preprocessed_dataset.csv')
data = pd.read_csv(data_path)[cols].fillna(0)
print(data.shape)

X = data.loc[:, data.columns != 'DESERTO']
y = data.loc[:, data.columns == 'DESERTO'].values.ravel()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=99)

pipeline = Pipeline([
    ('classifier', LogisticRegression)
])

params = {
    
}

param_grid = [
    {'classifier': [KNeighborsClassifier()],
     'classifier__n_neighbors': range(2, 10)},
    {'classifier': [DecisionTreeClassifier()],
     'classifier__max_depth': range(8, 36, 2),
     'classifier__criterion': ['gini', 'entropy']},
    {'classifier': [RandomForestClassifier()],
     'classifier__n_estimators': range(8, 36, 4),
     'classifier__criterion': ['gini', 'entropy']},
     {'classifier': [BaggingClassifier()],
      'classifier__n_estimators': range(2, 20, 2)}
]

model = GridSearchCV(pipeline, param_grid, scoring='accuracy', cv=3)
model.fit(X_train, y_train)
results=pd.DataFrame(model.cv_results_)
result_path = os.path.join(repo_path, 'models')
results.to_csv(os.path.join(result_path, 'results.csv'))
print(model.best_estimator_)

# mejor modelo
best = model.best_estimator_
# entrenamiento
best.fit(X_train, y_train)
# performance
y_pred = best.predict(X_test)
print(f'El accuracy del mejor modelo en el set de test es: {best.score(X_test, y_test):.2f}')

confusion_matrix = confusion_matrix(y_test, y_pred)
class_names = ['No desertó', 'Desertó']

Display = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=class_names)

Display.plot(cmap=plt.cm.Blues)
plt.title('Matriz de confusión (KNClassifier(n_neighbors=8))')
plt.show()

print(Display.confusion_matrix)