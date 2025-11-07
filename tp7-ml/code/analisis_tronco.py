import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Crear carpeta para guardar las imágenes
os.makedirs("graficos", exist_ok=True)

# Cargar el dataset
df = pd.read_csv("arbolado-mendoza-dataset-train.csv")

# Normalizar nombres de columnas
df.columns = df.columns.str.strip().str.lower()

# Convertir a numérico por si acaso
df['circ_tronco_cm'] = pd.to_numeric(df['circ_tronco_cm'], errors='coerce')
df['inclinacion_peligrosa'] = pd.to_numeric(df['inclinacion_peligrosa'], errors='coerce')

# Eliminar filas sin circ_tronco_cm o inclinacion_peligrosa
df = df.dropna(subset=['circ_tronco_cm', 'inclinacion_peligrosa'])

# ==============================================================
# (a) Histograma de frecuencia de circ_tronco_cm con distintos bins
# ==============================================================

plt.figure(figsize=(8, 5))
for bins in [10, 20, 50]:
    sns.histplot(df['circ_tronco_cm'], bins=bins, kde=False, label=f'{bins} bins', alpha=0.5)
plt.title("Histograma de frecuencia de circ_tronco_cm (diferentes bins)")
plt.xlabel("Circunferencia del tronco (cm)")
plt.ylabel("Frecuencia")
plt.legend()
plt.tight_layout()
plt.savefig("graficos/a_histograma_circ_tronco_cm_bins.png", dpi=300)
plt.close()

# ==============================================================
# (b) Histogramas separados por clase 'inclinacion_peligrosa'
# ==============================================================

# Filtrar por clase
df_peligroso = df[df['inclinacion_peligrosa'] == 1]
df_no_peligroso = df[df['inclinacion_peligrosa'] == 0]

# Histograma para árboles peligrosos
plt.figure(figsize=(8, 5))
for bins in [10, 20, 50]:
    sns.histplot(df_peligroso['circ_tronco_cm'], bins=bins, kde=False, label=f'{bins} bins', alpha=0.5, color='red')
plt.title("Histograma de circ_tronco_cm — Árboles PELIGROSOS (1)")
plt.xlabel("Circunferencia del tronco (cm)")
plt.ylabel("Frecuencia")
plt.legend()
plt.tight_layout()
plt.savefig("graficos/b_histograma_peligrosos_bins.png", dpi=300)
plt.close()

# Histograma para árboles NO peligrosos
plt.figure(figsize=(8, 5))
for bins in [10, 20, 50]:
    sns.histplot(df_no_peligroso['circ_tronco_cm'], bins=bins, kde=False, label=f'{bins} bins', alpha=0.5, color='green')
plt.title("Histograma de circ_tronco_cm — Árboles NO peligrosos (0)")
plt.xlabel("Circunferencia del tronco (cm)")
plt.ylabel("Frecuencia")
plt.legend()
plt.tight_layout()
plt.savefig("graficos/b_histograma_no_peligrosos_bins.png", dpi=300)
plt.close()

# ==============================================================
# (c) Crear variable categórica circ_tronco_cm_cat
# ==============================================================

# Usamos cuartiles para definir los cortes
q1 = df['circ_tronco_cm'].quantile(0.25)
q2 = df['circ_tronco_cm'].quantile(0.50)
q3 = df['circ_tronco_cm'].quantile(0.75)

def categorizar_circ(x):
    if x <= q1:
        return 'bajo'
    elif x <= q2:
        return 'medio'
    elif x <= q3:
        return 'alto'
    else:
        return 'muy alto'

df['circ_tronco_cm_cat'] = df['circ_tronco_cm'].apply(categorizar_circ)

# Guardar nuevo CSV
df.to_csv("arbolado-mendoza-dataset-circ_tronco_cm-train.csv", index=False)

# Mostrar puntos de corte
print("✅ Puntos de corte (según cuartiles de circ_tronco_cm):")
print(f"bajo      ≤ {q1:.2f}")
print(f"medio  > {q1:.2f} y ≤ {q2:.2f}")
print(f"alto   > {q2:.2f} y ≤ {q3:.2f}")
print(f"muy alto > {q3:.2f}")

print("\n📊 Archivos generados:")
print("- graficos/a_histograma_circ_tronco_cm_bins.png")
print("- graficos/b_histograma_peligrosos_bins.png")
print("- graficos/b_histograma_no_peligrosos_bins.png")
print("- arbolado-mendoza-dataset-circ_tronco_cm-train.csv")
