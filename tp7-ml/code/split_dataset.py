import pandas as pd

df = pd.read_csv('arbolado-mza-dataset.csv')

df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)

train_size = int(0.8 * len(df_shuffled))

train_df = df_shuffled.iloc[:train_size]
val_df = df_shuffled.iloc[train_size:]


train_df.to_csv('arbolado-mendoza-dataset-train.csv', index=False)
val_df.to_csv('arbolado-mendoza-dataset-validation.csv', index=False)

print("✅ Archivos generados correctamente.")
