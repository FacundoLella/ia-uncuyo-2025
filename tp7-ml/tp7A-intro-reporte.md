Respuestas Trabajo Practico N°7 - Parte A - 
1. En cada uno de los siguientes ejercicios, indique si en general se espera que un metodo de
aprendizaje de maquinas flexible se comporte mejor o peor que uno inflexible. Justifique su
respuesta.

a) El tamaño de la muestra n es extremadamente grande, y el numero de predictores p es
pequeño.

Un modelo flexible seria mejor. Debido a la gran muestra esto nos ayudaria a controlar el ruido por lo tanto 
bajar la varianza y aprovechar el poco sesgo de los modelos flexibles.

b) El numero de predictores p es extremadamente grande, y el numero de observaciones n es
pequeño.

Un modelo flexible seria peor. Pocas observaciones y muchos predictores harian que la varianza
suba y halla problemas de sobreajuste. En este caso es mejor usar uno inflexible.

c) La relacion entre los predictores y la variable dependiente es altamente no lineal.

Un modelo flexible seria mejor, ya que las técnicas flexibles pueden capturar 
esas no linealidades y reducir el sesgo, mejorando la predicción siempre que haya suficientes datos para controlar la varianza.


d ) La varianza de los terminos de error, σ2 = Var(ϵ), es extremadamente alta.

Un modelo flexible seria peor. Al tener mucho ruido los modelos flexibles aprenden de el asi aumentando la varianza del estimador.
En cambio los modelos inflexibles son mas robustos ante el ruido.

2. Explique si cada escenario representa un problema de clasificacion o de regresion, e indique si
el interes principal es inferir o predecir. Especifique n (cantidad de observaciones) y p (cantidad
de predictores) en cada caso.

a) Se recopila un conjunto de datos sobre las 500 empresas mas importantes de Estados
Unidos. Para cada una de las empresas se registran las ganancias, el numero de empleados,
la industria y el salario del director ejecutivo. Se tiene interes en comprender que factores
afectan el salario de los directores ejecutivos.

. En este caso se intenta inferir si un factor afecta o no el salario de los directores ejecutivos.
. p (predictores): 4 -> Ganancias, numero de empleados, la industria y el salario del director ejecutivo
. n (observaciones): 500


b) Se esta considerando lanzar un nuevo producto y se desea saber si sera un exito o un fracaso.
Se recolectan datos de 20 productos similares que fueron lanzados previamente. Para cada
producto se ha registrado si fue un exito o un fracaso, el precio cobrado por el producto,
el presupuesto de marketing, el precio de la competencia, y otras diez variables.

. Se intenta inferir si un producto es un fracasa o un exito.
. p (predictores): 13 -> precio cobrado por producto, presupuesto de marketing, precio competencia, otras diez variables.
. n (observaciones): 20


c) Se tiene interes en predecir el % de cambio en el tipo de cambio USD/Euro en relacion a
los cambios semanales en los mercados de valores mundiales. Para eso se recolectan datos
semanalmente durante todo el 2021. Para cada semana se registran el % de cambio de
USD/Euro, el % de cambio en el mercado estadounidense, el % de cambio en el mercado
britanico, y el % de cambio en el mercado aleman

. Se quiere predecir el % de cambio en el tipo de cambio USD/EURO.
. p (predictores): 4 % de cambio de USD/EURO, de cambio en el mercado estadounidense, de cambio en el mercado britanico y en el mercado aleman
. n (observaciones): Si cada semana obtenian una observacion entonces en el año obtenian 52 observaciones.

3. ¿Cuales son las ventajas y desventajas de un enfoque muy flexible (versus uno menos flexible)
para la regresion o clasificacion? ¿Bajo que circunstancias podrıa preferirse un enfoque mas
flexible a uno menos flexible? ¿Cu´ando podrıa preferirse un enfoque menos flexible?
- Ventajas-
. Menor Sesgo: son mejores para describir la relaciones no lineales o complejas.
. Con gran volumen de observaciones pueden mejorar sus estimaciones.
- Desventajas -
. Son muy sensibles a los datos ruidosos (mayor varianza)
. Dificil de interpretar ha medida que aumentan los predictores.

- Podriamos preferir un enfoque flexible cuando hay muchos datos y estos son no lineales y queremos hacer predicciones.

4. Describa las diferencias entre un enfoque parametrico y uno no parametrico. ¿Cuales son las
ventajas y desventajas de un enfoque parametrico para regresion o clasificacion, a diferencia de
un enfoque no parametrico?

- Enfoque Parametrico

Una de las formas más comunes de estimar f(X) es suponer que sigue una forma funcional específica, y luego ajustar sus 
parámetros a los datos observados. Este enfoque se denomina modelo paramétrico.

Paramétrico	
 Ventajas
- Sencillo e interpretable.
- Computacionalmente eficiente.
- Funciona bien con pocos datos.
 Desventajas
- Supones una forma funcional fija (puede ser incorrecta).
- Menos flexible, alto sesgo si la relación no es lineal.
No paramétrico
 Ventajas
- Muy flexible.
- Captura patrones no lineales.
- Menor sesgo si hay muchos datos.
  Desventajas
- - Alta varianza.
- Menor interpretabilidad.
- Requiere muchos datos (maldición de la dimensionalidad).

5. La siguiente tabla muestra un conjunto de entrenamiento que consta de seis observaciones, tres
predictores, y una variable dependiente cualitativa.

Obs. X1 X2 X3 Y
1 0 3 0 Rojo
2 2 0 0 Rojo
3 0 1 3 Rojo
4 0 1 2 Verde
5 -1 0 1 Verde
6 1 1 1 Rojo

Suponga que se quiere usar este dataset para predecir Y cuando X1 = X2 = X3 = 0 usando K
vecinos mas cercanos.
a) Calcule la distancia Euclidiana entre cada observacion y el punto de prueba X1 = X2 =
X3 = 0.

1) sqrt(0² + 3² + 0²) = 3.00 Rojo
2) sqrt(2² + 0² + 0²) = 2.00 Rojo
3) sqrt(0² + 1² + 3²) = 3.16 Rojo
4) sqrt(0² + 1² + 2²) = 	2.24 Verde
5) sqrt((-1)² + 0² + 1²)	= 1.41 Verde
6) sqrt(1² + 1² + 1²) = 1.73 Rojo

b) ¿Cual es la prediccion con K = 1? Justifique.
Con K=1 la obs. mas cercana es la 5 con una distancia de 1.41, por lo tanto inferimos que es Verde
c) ¿Cual es la prediccion con K = 3? Justifique.
Con K=3 debemos tomar las 3 obs. mas cercanas que serian la 2 (Rojo),5(Verde),6(Rojo), para inferir un valor debemos ver cual es el
color que predomina en este caso el Rojo
d ) Si el limite de decision de Bayes en este problema es altamente no lineal, ¿se espera que el
mejor valor para K sea grande o pequeno? ¿Por que?
Se espera que el mejor K sea pequeño, porque un K pequeño produce una frontera más flexible (capta la no linealidad, bajo sesgo, alta varianza).










