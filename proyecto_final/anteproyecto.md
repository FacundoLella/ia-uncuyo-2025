# **Anteproyecto – Inteligencia Artificial I**

## **Título del proyecto**
**Overtake Advisor: un sistema inteligente de recomendación de adelantamientos en Fórmula 1 mediante aprendizaje por refuerzo**

## **Código del proyecto**
**OVERTAKE**

## **Integrantes**
- Facundo Lella y Alejandro Moreno

---

## **Descripción**

**Overtake Advisor** propone el desarrollo de una **prueba de concepto** basada en **aprendizaje por refuerzo (Q-Learning / Deep Q-Learning)** para determinar **cuándo y dónde realizar un adelantamiento en una carrera de Fórmula 1**, utilizando datos reales de telemetría obtenidos a través de la librería [FastF1](https://docs.fastf1.dev/).

El objetivo principal es **entrenar un agente inteligente capaz de detectar momentos óptimos de adelantamiento** considerando el contexto dinámico de la pista (posición del rival, velocidad, distancia, DRS, curva actual, etc.) y **maximizar la probabilidad de éxito sin comprometer la carrera**.

El sistema actuará como un **asesor virtual**, recomendando en tiempo real si **adelantar**, **esperar** o **preparar el adelantamiento** en las siguientes curvas o sectores. No se busca implementar un simulador físico ni una interfaz gráfica final, sino **demostrar el comportamiento inteligente emergente del modelo entrenado** bajo distintas condiciones de carrera.

### **Objetivos**
- Desarrollar un modelo de aprendizaje por refuerzo que aprenda decisiones de adelantamiento basadas en estados dinámicos de carrera.  
- Simular escenarios de carrera simplificados para evaluar las decisiones del agente.  
- Medir el desempeño del modelo en términos de **tasa de adelantamientos exitosos**,**tiempo promedio hasta completar el adelantamiento**,etc.

### **Alcance**
- Se implementará una **simulación reducida**.
- El agente se entrenará con datos históricos y escenarios generados a partir de telemetría de FastF1.    

### **Limitaciones**
- El entorno será discreto y simplificado (ejemplo: dividir la pista en sectores y discretizar velocidades y distancias).   
- El modelo no planificará estrategias de carrera completas, sólo decisiones locales de adelantamiento.  

### **Evaluación y métricas**
El rendimiento del agente se evaluará mediante:
- **Tasa de adelantamientos exitosos (%)**  
- **Posicion final de la carrera usando el over**  
- **tiempo promedio hasta completar el adelantamiento**

---

## **Justificación**

El problema del **momento óptimo para adelantar en F1** es inherentemente **no determinista, dinámico y dependiente del contexto**, por lo que **no puede resolverse eficazmente mediante reglas fijas o algoritmos deterministas**.  
Las decisiones dependen de múltiples factores cambiantes (distancia al rival, energía del DRS, velocidad, ángulo de curva, grip del neumático, etc.) y del resultado de acciones anteriores.

Por ello, se propone el uso de **algoritmos de Inteligencia Artificial basados en Aprendizaje por Refuerzo (RL)**, en los cuales un agente aprende por experiencia directa a maximizar su recompensa acumulada mediante la interacción con un entorno.  
En particular, **Q-Learning** (o su versión con redes neuronales, **Deep Q-Learning**) permite que el agente aprenda una política de decisión sin requerir un modelo exacto del entorno físico, lo que lo hace ideal para escenarios de conducción simulada.

El uso de IA, y no de programación tradicional, se justifica en que **el espacio de estados y acciones es altamente complejo y variable**, y la **estrategia óptima no puede derivarse mediante un conjunto finito de reglas lógicas predefinidas**.

---

## **Listado de actividades**

| Nº | Actividad | Duración estimada |
|----|------------|------------------|
| 1 | Recopilación de bibliografía y simulación F1. | 7 días |
| 2 | Obtención, entendimiento y limpieza de datos de telemetría (FastF1). | 4 días |
| 3 | Definición del entorno de simulación y estados posibles (velocidad, distancia, DRS, sector, etc.). | 3 días |
| 4 | Implementación del entorno simplificado para entrenamiento del agente. | 6 días |
| 5 | Implementación del algoritmo de Q-Learning / Deep Q-Learning. | 7 días |
| 6 | Diseño de la función de recompensa y parámetros de entrenamiento. | 3 días |
| 7 | Entrenamiento del agente y registro de métricas (recompensa promedio, tasa de éxito). | 3 días |
| 8 | Validación del modelo y análisis de resultados. | 3 días |
| 9 | Redacción del informe final con resultados y conclusiones. | 3 días |

---

## **Cronograma estimado (Gantt)**

```text
Semanas →  1  2  3  4  5  6  7  8
1. Bibliografía         ████
2. Datos                ████
3. Diseño entorno          ████
4. Implementación entorno    ████
5. Q-Learning                  ████
6. Recompensa                   ██
7. Entrenamiento                   ███
8. Validación                        ██
10. Informe final                      ██

```
Referencias

FastF1: API de análisis de datos de Fórmula 1 — https://docs.fastf1.dev





