import pandas
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.under_sampling import AllKNN

# Ver head del preprocessed.csv
df = pandas.read_csv("data/preprocessed/preprocessed_dataset.csv")
print(df.head())


# Asigno todas las columnas menos DESERTO como variables explicativas variable_explicada_df a DESERTO como variable explicada

# se extrajo la columna
variables_explicativas_df = df.drop("DESERTO", axis=1)
print(variables_explicativas_df)
variable_explicada_df = df.loc[:, "DESERTO"]
print(variable_explicada_df)

# Crear el objeto SMOTE variable_explicada_df ADASYN
smote = SMOTE()
adasyn = ADASYN()
allknn = AllKNN()
# Hago loop con minoritaria a 0.2 hasta 0.5 de la mayoritaria

muestra_minoritaria = 0.2
muestra_mayoritaria = 0.8

for i in range(7):
    # Establezco la sampling strategy
    sampling_strategy = round(muestra_minoritaria / muestra_mayoritaria, 2)
    print(sampling_strategy)

    # Probamos primero con un Oversampling estandar
    df_resampled_oversampled, variable_explicada_df_resampled = RandomOverSampler(
        sampling_strategy=sampling_strategy
    ).fit_resample(df, variable_explicada_df)
    df_resampled_oversampled = pandas.DataFrame(df_resampled_oversampled)

    # Printeo el head para ver como se guardará
    print(df_resampled_oversampled.head())

    # Guardo como CSV cada muestra resampleada con el método correspondiente
    df_resampled_oversampled.to_csv(
        f"./data/stage/df_resampled_oversampled_{round(muestra_minoritaria,2)}.csv",
        sep=",",
        index=False,
        encoding="utf-8",
    )
    # Aplicamos Metodo SMOTE
    df_resampled_SMOTE, variable_explicada_df_SMOTE = smote.fit_resample(
        sampling_strategy=sampling_strategy
    ).fit_resample(df, variable_explicada_df)
    df_resampled_SMOTE = pandas.DataFrame(df_resampled_SMOTE)

    # Printeo el head para ver como se guardará
    print(df_resampled_SMOTE.head())

    # Guardo como CSV cada muestra resampleada con el método correspondiente
    df_resampled_SMOTE.to_csv(
        f"./data/stage/df_resampled_SMOTE_{round(muestra_minoritaria,2)}.csv",
        sep=",",
        index=False,
        encoding="utf-8",
    )

    # Aplicamos Metodo ADASYN
    df_resampled_ADASYN, variable_explicada_df_ADASYN = adasyn.fit_resample(
        sampling_strategy=sampling_strategy
    ).fit_resample(df, variable_explicada_df)
    df_resampled_ADASYN = pandas.DataFrame(df_resampled_ADASYN)

    # Printeo el head para ver como se guardará
    print(df_resampled_ADASYN.head())

    # Guardo como CSV cada muestra resampleada con el método correspondiente
    df_resampled_ADASYN.to_csv(
        f"./data/stage/df_resampled_ADASYN_{round(muestra_minoritaria,2)}.csv",
        sep=",",
        index=False,
        encoding="utf-8",
    )
    # Probamos primero con un Undersampling estandar
    df_resampled_undersampled, variable_explicada_df_undersampled = RandomUnderSampler(
        sampling_strategy=sampling_strategy
    ).fit_resample(df, variable_explicada_df)
    df_resampled_undersampled = pandas.DataFrame(df_resampled_undersampled)

    # Printeo el head para ver como se guardará
    print(df_resampled_undersampled.head())

    # Guardo como CSV cada muestra resampleada con el método correspondiente
    df_resampled_undersampled.to_csv(
        f"./data/stage/df_resampled_undersampled_{round(muestra_minoritaria,2)}.csv",
        sep=",",
        index=False,
        encoding="utf-8",
    )

    # Probamos primero con un Undersampling AllKNN
    df_resampled_AllKNN, variable_explicada_df_AllKNN = allknn(
        sampling_strategy=sampling_strategy
    ).fit_resample(df, variable_explicada_df)
    df_resampled_AllKNN = pandas.DataFrame(df_resampled_AllKNN)

    # Printeo el head para ver como se guardará
    print(df_resampled_AllKNN.head())

    # Guardo como CSV cada muestra resampleada con el método correspondiente
    df_resampled_AllKNN.to_csv(
        f"./data/stage/df_resampled_AllKNN_{round(muestra_minoritaria,2)}.csv",
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
