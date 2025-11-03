Resultados del Trabajo Practico N°4 - Busquedas Locales. Algoritmos utilizados
- Random
  
- SA = Simulated Annealing con 
  #CRITERIOS DE DETENCION:
  #Si encuentra una solucion (fitness = 0)
  #Si exploro mas de 1000 estados
  #Si rechazo 30 estados consecutivos
  
- HC = Hill Climbing Puro
  
- GA = Algoritmo Genetico (con estados incosistentes) con
  #ESTRATEGIA DE SELECCION: RANDOM
  #ESTRATEGIA DE REEMPLAZO: SI EL HIJO ES MEJOR QUE EL PEOR DE LA POBLACION, LO REEMPLAZA
  #OPERADORES: CRUZAMIENTO SIMPLE, MUTACION SIMPLE
  #CRITERIOS DE PARADA: SI ALGUN HIJO TIENE FITNESS 0, 100 GENERACIONES

Resultados: 
- Comparacion de promedio de estados explorados,fitness y tiempo

![4Reinas](./images/boxplots_combinados_N4.png)

![8Reinas](./images/boxplots_combinados_N8.png)

![10Reinas](./images/boxplots_combinados_N10.png)

- Comparacion del trackeo de H.

![4Reinas](./images/Htrace_combinado_N4.png)

![8Reinas](./images/Htrace_combinado_N8.png)

![10Reinas](./images/Htrace_combinado_N10.ng)

Viendo los resultados nos damos cuenta que el claro ganador para estas pruebas es el Algoritmo de SA, mantuvo siempre un fitness entre 0 y 2. Quizas dandole mas generaciones a GA y sacando estados inconsistentes
pueda haber mas competencia.


