import pandas
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

# preprocessed_train
df = pandas.read_csv("data/preprocessed/preprocessed_train.csv")


# Asigno todas las columnas menos DESERTO como variables explicativas variable_explicada_df a DESERTO como variable explicada
variables_explicativas_df = df.drop(["CODUSU"], axis=1)
variable_explicada_df = df.loc[:, "DESERTO"]
# Hago loop con minoritaria a 0.2 hasta 0.5 de la mayoritaria
muestra_minoritaria = 0.2
muestra_mayoritaria = 0.8

for i in range(7):
    # Establezco la sampling strategy
    sampling_strategy = round(muestra_minoritaria / muestra_mayoritaria, 2)

    # Probamos primero con un Oversampling estandar
    df_resampled_oversampled, variable_explicada_df_resampled = RandomOverSampler(
        sampling_strategy=sampling_strategy
    ).fit_resample(variables_explicativas_df, variable_explicada_df)
    df_resampled_oversampled = pandas.DataFrame(df_resampled_oversampled)

    # Guardo como CSV cada muestra resampleada con el método correspondiente
    df_resampled_oversampled.to_csv(
        f"data/stage/train_oversampled_{round(muestra_minoritaria,2)}.csv",
        sep=",",
        index=False,
        encoding="utf-8",
    )

    # Probamos primero con un Undersampling estandar
    df_resampled_undersampled, variable_explicada_df_undersampled = RandomUnderSampler(
        sampling_strategy=sampling_strategy
    ).fit_resample(variables_explicativas_df, variable_explicada_df)
    df_resampled_undersampled = pandas.DataFrame(df_resampled_undersampled)

    # Guardo como CSV cada muestra resampleada con el método correspondiente
    df_resampled_undersampled.to_csv(
        f"data/stage/train_undersampled_{round(muestra_minoritaria,2)}.csv",
        sep=",",
        index=False,
        encoding="utf-8",
    )

    muestra_minoritaria = muestra_minoritaria + 0.05
    muestra_mayoritaria = muestra_mayoritaria - 0.05
