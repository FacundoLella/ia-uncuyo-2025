import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import os

# Crear carpeta de salida
os.makedirs("graficos", exist_ok=True)

# Configuración de estilo
sns.set(style="whitegrid", palette="muted", font_scale=1.1)

# === 1. Leer el dataset (detectando separador automáticamente) ===
df = pd.read_csv("arbolado-mendoza-dataset-train.csv", sep=None, engine='python')
df.columns = df.columns.str.strip().str.lower()

# === 2. Normalizar columna de inclinación peligrosa ===
if 'inclinacion_peligrosa' not in df.columns:
    raise ValueError("⚠️ No se encontró la columna 'inclinacion_peligrosa' en el dataset. Verificá el nombre exacto.")

if df['inclinacion_peligrosa'].dtype not in [int, float]:
    df['inclinacion_peligrosa'] = (
        df['inclinacion_peligrosa']
        .astype(str)
        .str.lower()
        .map({'si': 1, 'true': 1, '1': 1, 'no': 0, 'false': 0, '0': 0})
    )

# Filtrar solo los peligrosos
peligrosos = df[df['inclinacion_peligrosa'] == 1]

# ==============================
# a) Distribución de inclinación peligrosa
# ==============================
plt.figure(figsize=(8, 6))
counts = df['inclinacion_peligrosa'].value_counts().sort_index()
percentages = (counts / counts.sum()) * 100

ax = sns.barplot(x=counts.index.astype(str), y=counts.values, palette="crest")

for i, (count, perc) in enumerate(zip(counts.values, percentages.values)):
    ax.text(i, count / 2, f"{int(count)}", ha='center', va='center', color='white', fontweight='bold')
    ax.text(i, count + (counts.max() * 0.02), f"{perc:.1f}%", ha='center', fontweight='bold')

plt.title("Distribución de la Clase 'Inclinación Peligrosa'")
plt.xlabel("Inclinación Peligrosa (0 = No, 1 = Sí)")
plt.ylabel("Cantidad de Árboles")
plt.tight_layout()
plt.savefig("graficos/grafico_distribucion_inclinacion.png", dpi=300)
plt.close()

# ==============================
# b) Proporción de árboles peligrosos por sección
# ==============================
if 'nombre_seccion' in df.columns:
    total_por_seccion = df.groupby('nombre_seccion').size()
    peligrosos_por_seccion = peligrosos.groupby('nombre_seccion').size()

    proporcion_seccion = (peligrosos_por_seccion / total_por_seccion * 100).sort_values(ascending=False).dropna()
    total_por_seccion = total_por_seccion.loc[proporcion_seccion.index]

    fig_width = max(10, math.ceil(len(proporcion_seccion) * 0.6))
    plt.figure(figsize=(fig_width, 6))
    ax = sns.barplot(x=proporcion_seccion.index, y=proporcion_seccion.values, palette="flare")
    plt.xticks(rotation=45, ha='right')

    for i, (perc, total) in enumerate(zip(proporcion_seccion.values, total_por_seccion.values)):
        ax.text(i, perc / 2, f"{int(total)}", ha='center', va='center', color='white', fontweight='bold')
        ax.text(i, perc + (proporcion_seccion.max() * 0.02), f"{perc:.1f}%", ha='center', fontweight='bold')

    plt.title("Proporción de Árboles Peligrosos por Sección")
    plt.xlabel("Sección")
    plt.ylabel("% de Árboles Peligrosos")
    plt.tight_layout()
    plt.savefig("graficos/grafico_secciones_peligrosas.png", dpi=300)
    plt.close()
else:
    print("⚠️ No se encontró la columna 'nombre_seccion' — se omite gráfico b).")

# ==============================
# c) Proporción de árboles peligrosos por especie
# ==============================
if 'especie' in df.columns:
    total_por_especie = df.groupby('especie').size()
    peligrosos_por_especie = peligrosos.groupby('especie').size()

    proporcion = (peligrosos_por_especie / total_por_especie * 100).sort_values(ascending=False).dropna()
    total_por_especie = total_por_especie.loc[proporcion.index]

    fig_width = max(10, math.ceil(len(proporcion) * 0.6))
    plt.figure(figsize=(fig_width, 6))
    ax = sns.barplot(x=proporcion.index, y=proporcion.values, palette="rocket")
    plt.xticks(rotation=45, ha='right')

    for i, (perc, total) in enumerate(zip(proporcion.values, total_por_especie.values)):
        ax.text(i, perc / 2, f"{int(total)}", ha='center', va='center', color='white', fontweight='bold')
        ax.text(i, perc + (proporcion.max() * 0.02), f"{perc:.1f}%", ha='center', fontweight='bold')

    plt.title("Proporción de Árboles Peligrosos por Especie")
    plt.xlabel("Especie")
    plt.ylabel("% de Árboles Peligrosos")
    plt.tight_layout()
    plt.savefig("graficos/grafico_especies_peligrosas.png", dpi=300)
    plt.close()
else:
    print("⚠️ No se encontró la columna 'especie' — se omite gráfico c).")

# ==============================
print("✅ Gráficos generados exitosamente en carpeta 'graficos/':")
print("- grafico_distribucion_inclinacion.png")
print("- grafico_secciones_peligrosas.png")
print("- grafico_especies_peligrosas.png")
