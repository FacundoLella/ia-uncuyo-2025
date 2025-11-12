TP7B - Desafío Kaggle Arbolado Público Mendoza

Objetivo y estrategia
Entrenar un modelo que clasifique la inclinación peligrosa usando arbolado-mendoza-dataset-train.csv y generar predicciones para los 13676 registros de arbolado-mza-dataset-test.csv, cumpliendo con la métrica AUC > 0.69 exigida por la cátedra. Se eligió LightGBM (lightgbm.LGBMClassifier) porque maneja bien datos tabulares con muchas variables categóricas y ofrece un buen balance entre performance y tiempo de entrenamiento. El set de entrenamiento se parte 80/20 con train_test_split estratificado (semilla 2025) para medir desempeño sin k-folds. Las probabilidades se convierten a 0/1 mediante un umbral adaptativo que replica la tasa de positivos (≈11.2%) del train; así se evita que el submission quede dominado por ceros.

Preprocesamiento

Limpieza numérica: altura, circ_tronco_cm, diametro_tronco, long, lat y area_seccion se pasan a float y se imputan con la mediana del train. Se usa la misma mediana para completar el test.
Variables temporales: ultima_modificacion se parsea con formato día/mes/año para generar mod_year, mod_month, mod_day, mod_hour y mod_wday. Los NA se reemplazan con la mediana del campo correspondiente.
Atributos derivados: densidad_tronco = circ_tronco_cm / (diametro_tronco + 1), relacion_altura_circ = altura / (circ_tronco_cm + 1), altura_div_diametro y long_lat_ratio capturan relaciones geométricas básicas.
Categóricas: especie, seccion y nombre_seccion se normalizan (minúsculas, trim) y se codifican como enteros con un mapeo aprendido en el train. Las clases nuevas del test se envían a un índice adicional para no fallar.

Modelo LightGBM
Hiperparámetros: learning_rate 0.05, hasta 1200 árboles, num_leaves 48, subsample 0.8, colsample_bytree 0.8, reg_lambda 1.0 y scale_pos_weight = (negativos / positivos) para mitigar el desbalance.
Entrenamiento: se entrena con early stopping (50 rondas) sobre el fold de validación. Luego se reentrena un modelo final usando todas las filas del train con el número óptimo de árboles (best_iteration_).
Métricas locales (20% de hold-out): AUC 0.7539, accuracy 0.8374, precision 0.3096, recall 0.3647, umbral adaptativo 0.1787. El AUC supera con margen el objetivo de 0.69 y mantiene un recall razonable para un dataset tan desbalanceado. Las métricas completas están en code/desafio/output/validation_metrics.csv.

Resultados

(Locales)

| AUC  | Accuracy | Precision | Recall |
|------|-----------|------------|---------|
| 0.7539 | 0.8374 | 0.3096 | 0.3647 |


Sin embargo en la competencia kaggle no le fue como se esperaba teniendo un rendimiento muy por 
debajo de lo esperado 0.60 lo cual lo convierte en el 2do peor de todos.

