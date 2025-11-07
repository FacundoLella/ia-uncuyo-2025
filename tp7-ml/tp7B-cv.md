CREATE_FOLDS

```{r}
create_folds <- function(df, k = 10) {
  n <- nrow(df)
  indices <- sample(1:n)  # mezcla aleatoria
  folds <- split(indices, cut(seq_along(indices), breaks = k, labels = FALSE))
  names(folds) <- paste0("Fold", 1:k)
  return(folds)
}
```
CROSS_VALIDATION

```{r}
cross_validation <- function(df, folds = 10, target_col, positive_class_value) {
  
  # --- Validación inicial ---
  if (!target_col %in% names(df)) {
    stop(paste("La columna '", target_col, "' no existe en el dataframe."))
  }
  
  df[[target_col]] <- as.factor(df[[target_col]])
  
  if (!positive_class_value %in% levels(df[[target_col]])) {
    stop(paste("El valor '", positive_class_value, "' no se encuentra en la columna '", target_col, "'."))
  }
  
  # --- Función auxiliar ---
  safe_division <- function(numerador, denominador) {
    if (denominador == 0) return(NA)
    numerador / denominador
  }
  
  # --- Crear folds ---
  folds_list <- create_folds(df, folds)
  all_metrics <- list()
  positive_class <- as.character(positive_class_value)
  
  cat(paste0("\nIniciando validación cruzada con ", folds, " folds...\n"))
  cat(paste0("Columna objetivo: ", target_col, "\n"))
  cat(paste0("Clase positiva: ", positive_class, "\n\n"))
  
  # --- Loop principal ---
  for (i in seq_len(folds)) {
    cat("Ejecutando Fold", i, "...\n")
    
    test_indices <- folds_list[[i]]
    train_indices <- setdiff(seq_len(nrow(df)), test_indices)
    
    train_set <- df[train_indices, ]
    test_set  <- df[test_indices, ]
    
    if (nrow(test_set) == 0 || nrow(train_set) == 0) next
    
    # --- Modelo de árbol ---
    formula <- formula(inclinacion_peligrosa ~ altura +
                         circ_tronco_cm + lat + long +
                         seccion + especie)
    
    model <- rpart(formula, data = train_set, method = "class")
    
    # --- Predicción ---
    predictions <- predict(model, newdata = test_set, type = "class")
    actuals <- test_set[[target_col]]
    predictions <- factor(predictions, levels = levels(actuals))
    
    # --- Calcular métricas ---
    TP <- sum(actuals == positive_class & predictions == positive_class)
    TN <- sum(actuals != positive_class & predictions != positive_class)
    FP <- sum(actuals != positive_class & predictions == positive_class)
    FN <- sum(actuals == positive_class & predictions != positive_class)
    
    accuracy <- safe_division(TP + TN, TP + TN + FP + FN)
    precision <- safe_division(TP, TP + FP)
    sensitivity <- safe_division(TP, TP + FN)
    specificity <- safe_division(TN, TN + FP)
    
    all_metrics[[i]] <- data.frame(
      Fold = i,
      Accuracy = accuracy,
      Precision = precision,
      Sensitivity = sensitivity,
      Specificity = specificity
    )
  }
  
  # --- Resultados finales ---
  metrics_df <- do.call(rbind, all_metrics)
  
  mean_metrics <- sapply(metrics_df[, -1], mean, na.rm = TRUE)
  sd_metrics <- sapply(metrics_df[, -1], sd, na.rm = TRUE)
  
  result <- list(
    media = mean_metrics,
    desviacion_estandar = sd_metrics,
    metricas_por_fold = metrics_df
  )
  
  return(result)
}
```

METRICAS:
- MEDIA - 

| Métrica     |  Valor |
| :---------- | :----: |
| Accuracy    | 0.8877 |
| Precision   |   NA   |
| Sensitivity |    0   |
| Specificity |    1   |

- DESVIACION ESTANDAR -

  | Métrica     |  Valor |
| :---------- | :----: |
| Accuracy    | 0.0093 |
| Precision   |   NA   |
| Sensitivity |    0   |
| Specificity |    0   |


