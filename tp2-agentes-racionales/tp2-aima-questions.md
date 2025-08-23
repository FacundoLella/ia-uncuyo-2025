Agente Perfectamente Racioanl: Un agente perfectamente racional actúa en todo momento para maximizar su utilidad esperada, dada 
la información que ha adquirido del entorno.

2.10 Consider a modified version of the vacuum environment in Exercise 2.8, in which the agent is penalized one point for each movement.

a. Can a simple reflex agent be perfectly rational for this environment? Explain.
 - No, dado que al ser reflexivo simple no tiene informacion de lo que paso anteriormente podria volver a celdas que ya limpio sin
   razon una y otra vez.
  
b. What about a reflex agent with state? Design such an agent.
  - No creo que este tipo pueda ser perfectamente racional al no tener la informacion del entorno completo, siempre habra un movimiento que no maximice su utilidad esperada.

c. How do your answers to a and b change if the agent’s percepts give it the clean/dirty status of every square in the environment?
  - Si tenemos todos los cuadrados donde estan limpios y sucios, podriamos programar una secuencia de movimientos para poder limpiar todo el tablero. Esto lo
    pueden implementar ambos agentes.

2.11 Consider a modified version of the vacuum environment in Exercise 2.8, in which thegeography of the environment—its extent, boundaries, and obstacles—is unknown, as is the
initial dirt configuration. (The agent can go Up and Down as well as Left and Right.)

a. Can a simple reflex agent be perfectly rational for this environment? Explain.
 - No, al ser random y no recordar estados podria estar chocandose paredes lo cual ya no es un agente perfectamente racional.
   
b. Can a simple reflex agent with a randomized agent function outperform a simple reflex agent? Design such an agent and measure its performance on several environments.
  - Si, el agente reflexivo simple con cierta reglas definidas podria caer en un bucle debido a no tener informacion del entorno, en cambio el
    reflexivo simple aleatorio podria escapar de estas situaciones y poder mejorar la performance.
    
c. Can you design an environment in which your randomized agent will perform poorly? Show your results.
  - En los ejercicios hechos anteriormente podemos ver en el tp2-report.md como el random presenta una peor performance.

d. Can a reflex agent with state outperform a simple reflex agent? Design such an agent and measure its performance 
on several environments. Can you design a rational agent of this type?
  - 





