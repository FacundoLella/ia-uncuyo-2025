library(dplyr)

# ------------------------------------------
# Funciones del clasificador aleatorio
# ------------------------------------------
agregar_prediction_prob <- function(df) {
  df %>%
    mutate(prediction_prob = runif(n()))
}

random_classifier <- function(df) {
  df %>%
    mutate(prediction_class = ifelse(prediction_prob > 0.5, 1, 0))
}

# ------------------------------------------
# Lectura y preparación del dataset
# ------------------------------------------
df_valid <- read.csv("arbolado-mendoza-dataset-validation.csv", sep = ",")
colnames(df_valid) <- trimws(tolower(colnames(df_valid)))  

df_valid <- df_valid %>%
  mutate(inclinacion_peligrosa = case_when(
    inclinacion_peligrosa %in% c("si", "SI", "true", "1") ~ 1,
    inclinacion_peligrosa %in% c("no", "NO", "false", "0") ~ 0,
    TRUE ~ as.numeric(inclinacion_peligrosa)
  ))

df_valid <- agregar_prediction_prob(df_valid)
df_valid <- random_classifier(df_valid)

# ------------------------------------------
# Cálculo de TP, TN, FP, FN
# ------------------------------------------
TP <- df_valid %>% filter(inclinacion_peligrosa == 1 & prediction_class == 1) %>% nrow()
TN <- df_valid %>% filter(inclinacion_peligrosa == 0 & prediction_class == 0) %>% nrow()
FP <- df_valid %>% filter(inclinacion_peligrosa == 0 & prediction_class == 1) %>% nrow()
FN <- df_valid %>% filter(inclinacion_peligrosa == 1 & prediction_class == 0) %>% nrow()

# ------------------------------------------
# Mostrar los resultados
# ------------------------------------------
cat("True Positive (TP):", TP, "\n")
cat("True Negative (TN):", TN, "\n")
cat("False Positive (FP):", FP, "\n")
cat("False Negative (FN):", FN, "\n\n")

# ------------------------------------------
# Matriz de confusión
# ------------------------------------------
matriz_confusion <- matrix(
  c(TP, FP, FN, TN),
  nrow = 2,
  byrow = TRUE,
  dimnames = list(
    "Real (inclinacion_peligrosa)" = c("1 = Sí", "0 = No"),
    "Predicho (prediction_class)" = c("1 = Sí", "0 = No")
  )
)

print(matriz_confusion)

# Guardar matriz de confusión
write.csv(matriz_confusion, "matriz_confusion_random_classifier.csv", row.names = TRUE)
cat("\n✅ Matriz de confusión guardada: matriz_confusion_random_classifier.csv\n")

# Guardar predicciones
write.csv(df_valid, "arbolado-mendoza-validation-predictions.csv", row.names = FALSE)
cat("✅ Archivo guardado: arbolado-mendoza-validation-predictions.csv\n")

# ------------------------------------------
# Funciones para métricas
# ------------------------------------------
accuracy <- function(TP, TN, FP, FN) {
  (TP + TN) / (TP + TN + FP + FN)
}

precision <- function(TP, FP) {
  if ((TP + FP) == 0) return(NA)
  TP / (TP + FP)
}

sensitivity <- function(TP, FN) {
  if ((TP + FN) == 0) return(NA)
  TP / (TP + FN)
}

specificity <- function(TN, FP) {
  if ((TN + FP) == 0) return(NA)
  TN / (TN + FP)
}

# ------------------------------------------
# Calcular métricas
# ------------------------------------------
acc <- accuracy(TP, TN, FP, FN)
prec <- precision(TP, FP)
sens <- sensitivity(TP, FN)
spec <- specificity(TN, FP)

# Mostrar resultados
cat("\n📈 Métricas del clasificador aleatorio:\n")
cat("Accuracy:", round(acc, 4), "\n")
cat("Precision:", round(prec, 4), "\n")
cat("Sensitivity:", round(sens, 4), "\n")
cat("Specificity:", round(spec, 4), "\n")

# Guardar métricas
metricas_df <- data.frame(
  Accuracy = acc,
  Precision = prec,
  Sensitivity = sens,
  Specificity = spec
)

write.csv(metricas_df, "metricas_random_classifier.csv", row.names = FALSE)
cat("\n✅ Métricas guardadas: metricas_random_classifier.csv\n")
