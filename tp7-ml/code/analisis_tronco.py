import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Crear carpeta para guardar los gráficos
os.makedirs("graficos", exist_ok=True)

# Configuración de estilo
sns.set(style="whitegrid", palette="viridis", font_scale=1.1)

# Leer el dataset
df = pd.read_csv("arbolado-mendoza-dataset-train.csv", sep=None, engine="python")
df.columns = df.columns.str.strip().str.lower()

# Normalizar columna de inclinación peligrosa
if df['inclinacion_peligrosa'].dtype not in [int, float]:
    df['inclinacion_peligrosa'] = (
        df['inclinacion_peligrosa']
        .astype(str)
        .str.lower()
        .map({'si': 1, 'true': 1, '1': 1, 'no': 0, 'false': 0, '0': 0})
    )

# ==============================
# a) Histograma de circ_tronco_cm con distintos bins
# ==============================
plt.figure(figsize=(8, 6))
for bins in [10, 20, 40, 50 ,60 ,70]:
    sns.histplot(df['circ_tronco_cm'], bins=bins, kde=False, label=f"{bins} bins", alpha=0.5)
plt.legend()
plt.title("Histograma de 'circ_tronco_cm' con distintos números de bins")
plt.xlabel("Circunferencia del Tronco (cm)")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.savefig("graficos/histograma_circ_tronco_bins.png", dpi=300)
plt.close()

# ==============================
# b) Histograma separado por clase 'inclinacion_peligrosa'
# ==============================
plt.figure(figsize=(8, 6))
sns.histplot(
    data=df,
    x='circ_tronco_cm',
    hue='inclinacion_peligrosa',
    bins=30,
    kde=False,
    multiple="stack",
    palette={0: "green", 1: "red"},
)
plt.title("Histograma de 'circ_tronco_cm' separado por 'inclinacion_peligrosa'")
plt.xlabel("Circunferencia del Tronco (cm)")
plt.ylabel("Frecuencia")
plt.legend(title="Peligrosa", labels=["No", "Sí"])
plt.tight_layout()
plt.savefig("graficos/histograma_circ_tronco_peligrosa.png", dpi=300)
plt.close()

# ==============================
# c) Crear variable categórica circ_tronco_cm_cat
# ==============================
# Usamos los cuartiles del histograma como puntos de corte
q1 = df['circ_tronco_cm'].quantile(0.25)
q2 = df['circ_tronco_cm'].quantile(0.50)
q3 = df['circ_tronco_cm'].quantile(0.75)

# Crear categorías según los puntos de corte
def categorizar_tronco(x):
    if x <= q1:
        return 'bajo'
    elif x <= q2:
        return 'medio'
    elif x <= q3:
        return 'alto'
    else:
        return 'muy alto'

df['circ_tronco_cm_cat'] = df['circ_tronco_cm'].apply(categorizar_tronco)

# Guardar nuevo CSV
df.to_csv("arbolado-mendoza-dataset-circ_tronco_cm-train.csv", index=False)

# ==============================
# Verificar proporciones de las categorías
# ==============================
plt.figure(figsize=(8, 6))
sns.countplot(x='circ_tronco_cm_cat', data=df, order=['bajo', 'medio', 'alto', 'muy alto'], palette='crest')
plt.title("Distribución de Categorías de 'circ_tronco_cm_cat'")
plt.xlabel("Categoría del Tronco")
plt.ylabel("Cantidad de Árboles")
plt.tight_layout()
plt.savefig("graficos/categorias_circ_tronco.png", dpi=300)
plt.close()

print("✅ Gráficos y archivo generados correctamente:")
print("- graficos/histograma_circ_tronco_bins.png")
print("- graficos/histograma_circ_tronco_peligrosa.png")
print("- graficos/categorias_circ_tronco.png")
print("- arbolado-mendoza-dataset-circ_tronco_cm-train.csv")
print("\nPuntos de corte (en cm):")
print(f"   Bajo ≤ {q1:.2f}")
print(f"   Medio ≤ {q2:.2f}")
print(f"   Alto ≤ {q3:.2f}")
print(f"   Muy Alto > {q3:.2f}")
