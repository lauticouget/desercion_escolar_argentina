import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.over_sampling import RandomOverSampler

# Ver head del preprocessed.csv
df = pd.read_csv("data/preprocessed/preprocessed_dataset.csv")
print(df.head())


# Asigno todas las columnas menos DESERTO como variables explicativas variable_explicada_df a DESERTO como variable explicada

variables_explicativas_df = df.drop("DESERTO", axis=1)
print(variables_explicativas_df)
variable_explicada_df = df.loc[:, "DESERTO"]
print(variable_explicada_df)

# Probamos primero con un Oversampling estandar

variables_explicativas_df_resampled, variable_explicada_df_resampled = RandomOverSampler(
    sampling_strategy=1
).fit_resample(variables_explicativas_df, variable_explicada_df)
df2 = df.join(variables_explicativas_df_resampled, variable_explicada_df_resampled)
from collections import Counter

print(sorted(Counter(variable_explicada_df).items()))

df2.to_csv(
    "balanceo_de_clases_oversampled.csv",
    sep=",",
    index=False,
    encoding="utf-8",
)



"""
# Crear el objeto SMOTE variable_explicada_df ADASYN
smote = SMOTE()
adasyn = ADASYN()

# Aplicar SMOTE a tus datos
variables_explicativas_df_resampled, variable_explicada_df_resampled = (
    smote.fit_resample(variables_explicativas_df, variable_explicada_df)
)

clf_smote = LogisticRegression().fit(
    variables_explicativas_df_resampled, variable_explicada_df_resampled
)
variables_explicativas_df_resampled, variable_explicada_df_resampled = (
    adasyn.fit_resample(variables_explicativas_df, variable_explicada_df)
)

clf_adasyn = LogisticRegression().fit(
    variables_explicativas_df_resampled, variable_explicada_df_resampled
)
"""
