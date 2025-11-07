library(dplyr)

# ------------------------------------------
# Clasificador de Mayor Clase
# ------------------------------------------
biggerclass_classifier <- function(df, columna = "inclinacion_peligrosa") {
  major_class <- as.numeric(names(which.max(table(df[[columna]]))))
  df <- df %>% mutate(prediction_class = major_class)
  return(df)
}

# Leer dataset
nombre_archivo <- "arbolado-mendoza-dataset-validation.csv"
mi_df <- read.csv(nombre_archivo)

# Clasificación
nuevo_df <- biggerclass_classifier(mi_df)

# Calcular TP, TN, FP, FN
TP <- nuevo_df %>% filter(inclinacion_peligrosa == 1 & prediction_class == 1) %>% nrow()
TN <- nuevo_df %>% filter(inclinacion_peligrosa == 0 & prediction_class == 0) %>% nrow()
FP <- nuevo_df %>% filter(inclinacion_peligrosa == 0 & prediction_class == 1) %>% nrow()
FN <- nuevo_df %>% filter(inclinacion_peligrosa == 1 & prediction_class == 0) %>% nrow()

# Mostrar conteos
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
    Real = c("1 = Sí", "0 = No"),
    Predicho = c("1 = Sí", "0 = No")
  )
)

print(matriz_confusion)

# Guardar matriz de confusión
write.csv(matriz_confusion, "matriz_confusion_biggerclass.csv", row.names = TRUE)
cat("\n✅ Matriz de confusión guardada: matriz_confusion_biggerclass.csv\n")

# Guardar resultado completo con predicciones
write.csv(nuevo_df, "arbolado-mendoza-dataset-validation-biggerclass.csv", row.names = FALSE)
cat("✅ Archivo guardado: arbolado-mendoza-dataset-validation-biggerclass.csv\n")


# ------------------------------------------
# Funciones de métricas
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
cat("\n📈 Métricas del clasificador de mayor clase:\n")
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

write.csv(metricas_df, "metricas_biggerclass_classifier.csv", row.names = FALSE)
cat("\n✅ Métricas guardadas: metricas_biggerclass_classifier.csv\n")
