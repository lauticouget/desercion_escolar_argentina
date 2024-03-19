import pandas
from sklearn.utils import resample

df = pandas.read_csv("data/preprocessed/preprocessed_dataset.csv")

# Separate majority and minority classes
desertores = df[df.DESERTO == 1]
no_desertores = df[df.DESERTO == 0]

# Calculate the minority new samples needed for a 50/50
count_no_desertores = len(df) - df.DESERTO.sum()

# Upsample minority class 50/50
desertores_upsampled = resample(
    desertores,
    replace=True,  # sample with replacement
    n_samples=count_no_desertores,  # to match majority class
    random_state=0,
)

# Combine majority class with upsampled minority class
df_upsampled = pandas.concat([no_desertores, desertores_upsampled])

# Calculate the percentage of True desertores after resampled
porcentaje_desertores_upsampled = (
    df_upsampled["DESERTO"].sum() / len(df_upsampled)
) * 100
print("Porcentaje Desertores Upsampled", porcentaje_desertores_upsampled)
print("DESERTO Value Counts: \n", df_upsampled.DESERTO.value_counts())

print(df_upsampled.head())

# print(sorted(Counter(variable_explicada_df_resampled).items()))
df_upsampled.to_csv(
    "./data/stage/df_upsampled.csv",
    sep=",",
    index=False,
    encoding="utf-8",
)