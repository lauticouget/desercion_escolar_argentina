import pandas
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.over_sampling import RandomOverSampler
from collections import Counter

# Ver head del preprocessed.csv
df = pandas.read_csv("data/preprocessed/preprocessed_dataset.csv")
print(df.head())


# Asigno todas las columnas menos DESERTO como variables explicativas variable_explicada_df a DESERTO como variable explicada

# se extrajo la columna
variables_explicativas_df = df.drop("DESERTO", axis=1)
print(variables_explicativas_df)
variable_explicada_df = df.loc[:, "DESERTO"]
print(variable_explicada_df)

# Hago loop con minoritaria a 0.2 hasta 0.5 de la mayoritaria

muestra_minoritaria = 0.2
muestra_mayoritaria = 0.8

for i in range(7):

    sampling_strategy = round(muestra_minoritaria / muestra_mayoritaria, 2)
    print(sampling_strategy)
    # Probamos primero con un Oversampling estandar

    df_resampled_oversampled, variable_explicada_df_resampled = RandomOverSampler(
        sampling_strategy=sampling_strategy
    ).fit_resample(df, variable_explicada_df)
    df_resampled_oversampled = pandas.DataFrame(df_resampled_oversampled)

    # df_resampled_oversampled.assign(variable_explicada_df_resampled)
    print(df_resampled_oversampled.head())

    # print(sorted(Counter(variable_explicada_df_resampled).items()))
    df_resampled_oversampled.to_csv(
        f"./data/stage/df_resampled_oversampled_{round(muestra_minoritaria,2)}.csv",
        sep=",",
        index=False,
        encoding="utf-8",
    )

    muestra_minoritaria = muestra_minoritaria + 0.05
    muestra_mayoritaria = muestra_mayoritaria - 0.05


"""df2.to_csv(
    "./data/balanceo_de_clases_oversampled.csv",
    sep=",",
    index=False,
    encoding="utf-8",
)
"""
"""
# Crear el objeto SMOTE variable_explicada_df ADASYN
smote = SMOTE()
adasyn = ADASYN()

# Aplicar SMOTE a tus datos
df_resampled_oversampled, variable_explicada_df_resampled = (
    smote.fit_resample(variables_explicativas_df, variable_explicada_df)
)

clf_smote = LogisticRegression().fit(
    df_resampled_oversampled, variable_explicada_df_resampled
)
df_resampled_oversampled, variable_explicada_df_resampled = (
    adasyn.fit_resample(variables_explicativas_df, variable_explicada_df)
)

clf_adasyn = LogisticRegression().fit(
    df_resampled_oversampled, variable_explicada_df_resampled
)
"""
