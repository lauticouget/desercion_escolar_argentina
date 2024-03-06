from desercion_escolar_argentina.utils import file_handler as fh
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

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
y = data.loc[:, data.columns == 'DESERTO']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=99)

# instancia del modelo
logisticRegr = LogisticRegression(max_iter=10000)
# entrenamiento
logisticRegr.fit(x_train, y_train)
# performance
y_pred = logisticRegr.predict(x_test)
print(f'El accuracy de nuestra regresión logística en el set de test es: {logisticRegr.score(x_test, y_test):.2f}')

confusion_matrix = confusion_matrix(y_test, y_pred)
class_names = ['desertó', 'no desertó']

Display = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=class_names)

Display.plot(cmap=plt.cm.Blues)
plt.title('Matriz de confusión/deserción escolar')
plt.show()

print(Display.confusion_matrix)