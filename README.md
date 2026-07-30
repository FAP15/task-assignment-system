# Análisis de tareas usando Python, Grafos y Power BI
Este proyecto simula la asignación de tareas dentro de una empresa mediante el cálculo de compatibilidad entre empleados y tareas. Utiliza Python para procesar los datos, construir un grafo bipartito y calcular métricas de compatibilidad, mientras que Power BI se emplea para visualizar los resultados mediante un informe interactivo.
# Sistema de Asignación de Tareas Basado en Compatibilidad

## Descripción

Este proyecto implementa un sistema de asignación de tareas basado en el grado de compatibilidad entre empleados y tareas. A partir de un conjunto de datos generado en Python, se calcula un porcentaje de compatibilidad considerando distintas habilidades ponderadas, se construyen grafos bipartitos para representar las relaciones entre empleados y tareas y, finalmente, se desarrollan informes interactivos en Power BI para facilitar el análisis de los resultados.

El objetivo del proyecto es mostrar un flujo completo de análisis de datos utilizando Python para el procesamiento de la información y Power BI para la visualización, simulando un escenario de asignación de tareas dentro de una empresa.

---

# Objetivos

* Generar un conjunto de datos representativo de empleados y tareas.
* Diseñar una métrica que permita calcular el nivel de compatibilidad entre un empleado y una tarea.
* Modelar las relaciones mediante grafos bipartitos.
* Obtener diferentes perspectivas de análisis aplicando filtros sobre la red.
* Desarrollar un dashboard interactivo que facilite la interpretación de los resultados.

---

# Tecnologías utilizadas

* Python
* Pandas
* NetworkX
* OpenPyXL
* Power BI Desktop
* Microsoft Excel

---

# Estructura del proyecto

```text
Proyecto/
│
├── empresa.xlsx
├── funciones_proyecto.py
├── menu_proyecto.py
├── grafos_proyecto.py
├── grafo_completo.xlsx
├── grafo_80.xlsx
├── top3_tareas.xlsx
└── README.md
```

---

# Metodología

## 1. Generación del conjunto de datos

Como punto de partida se desarrolló un conjunto de datos sintético compuesto por **75 empleados** y **30 tareas**.

Cada empleado posee un nivel de dominio en distintas habilidades, mientras que cada tarea define el nivel mínimo requerido para poder realizarla.

Toda la información fue generada mediante Python y posteriormente exportada al archivo **empresa.xlsx**, que constituye la base de datos utilizada durante todo el proyecto.

---

## 2. Modelo de compatibilidad

Para evaluar qué tan adecuado es un empleado para realizar una determinada tarea se definieron cuatro habilidades fundamentales.

| Habilidad               | Peso |
| ----------------------- | ---: |
| Herramientas técnicas   | 0.10 |
| Inglés                  | 0.20 |
| Trabajo en equipo       | 0.30 |
| Resolución de problemas | 0.40 |

Los pesos representan la importancia relativa de cada habilidad dentro del cálculo de compatibilidad.

Cada habilidad puede tomar un nivel comprendido entre **0 y 4**.

| Nivel | Significado |
| ----: | ----------- |
|     0 | Nulo        |
|     1 | Básico      |
|     2 | Intermedio  |
|     3 | Avanzado    |
|     4 | Experto     |

En el caso de los empleados, el nivel representa el dominio que poseen sobre una habilidad determinada.

En las tareas, el valor representa el nivel mínimo requerido para desempeñarlas correctamente.

---

## Cálculo de compatibilidad

El porcentaje de compatibilidad se obtiene comparando el nivel de cada empleado con los requisitos de cada tarea, considerando además la importancia de cada habilidad mediante los pesos definidos.

La lógica utilizada consiste en comparar cuánto de los requerimientos de una tarea puede cubrir un empleado respecto del nivel ideal necesario para realizarla.

De esta forma se obtiene un valor normalizado entre **0 % y 100 %**, lo que permite comparar empleados para cualquier tarea independientemente de la cantidad o importancia de las habilidades requeridas.

La interpretación del resultado es inmediata.
$\sum\times 100 $
Por ejemplo:
$C={{\sum_{i=1}^4 w_i\cdot min(E_i,T_i)}\over {\sum_{i=1}^4 w_i\cdot T_i}}\times 100$

$E_i$= nivel del empleado.
$T_i$= nivel requerido por la tarea.
$w_i$= peso de la habilidad.

${{\sum peso_i\cdot min(skill_{emp,i}, skill_{task,i})}\over {\sum peso_i\cdot skill_{task,i}}}\times 100$

${{a-2} \over 2}5$
**The Cauchy-Schwarz Inequality**\
$$\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)$$
* **100 %** indica que el empleado satisface completamente todos los requerimientos ponderados de la tarea.
* **85,7 %** indica que cumple aproximadamente el 85 % de los requisitos ponderados.
* Valores bajos representan una menor adecuación entre el perfil del empleado y la tarea.

Además, el proyecto contempla el caso particular de tareas sin requisitos específicos, asignándoles automáticamente una compatibilidad del 100 % para evitar divisiones por cero y mantener una interpretación consistente del resultado.

---

## Consulta de compatibilidad

Como primera aplicación del modelo desarrollado se implementó un programa de consola (`menu_proyecto.py`) que permite al usuario ingresar el identificador de un empleado y el identificador de una tarea para obtener el porcentaje de compatibilidad correspondiente.

Esta funcionalidad permite verificar individualmente cualquier relación empleado–tarea generada por el sistema.

---

# Construcción de la red bipartita

Una vez calculadas todas las compatibilidades, se construyeron distintos grafos bipartitos utilizando la biblioteca **NetworkX**.

En estos grafos:

* un conjunto de nodos representa a los empleados;
* el otro conjunto representa las tareas;
* cada arista almacena el porcentaje de compatibilidad entre ambos.

Con el objetivo de analizar la información desde distintas perspectivas se generaron tres grafos diferentes.

## Grafo bipartito completo

Este grafo contiene todas las relaciones posibles entre empleados y tareas.

Cada uno de los **75 empleados** se encuentra conectado con las **30 tareas**, obteniéndose un total de **2250 relaciones**.

Este grafo constituye la representación completa del sistema de compatibilidad y sirve como punto de partida para el resto de los análisis.

> *(Insertar imagen del grafo completo.)*

---

## Grafo de compatibilidades altas

El segundo grafo filtra la red completa y conserva únicamente aquellas relaciones cuya compatibilidad es igual o superior al **80 %**.

Este filtrado permite identificar rápidamente qué empleados resultan adecuados para cada tarea y cuáles son las tareas que cuentan con una mayor cantidad de candidatos compatibles.

> *(Insertar imagen del grafo filtrado.)*

---

## Top 3 tareas por empleado

El tercer grafo selecciona únicamente las tres tareas con mayor porcentaje de compatibilidad para cada empleado.

Esta representación facilita la recomendación de tareas, mostrando aquellas opciones que mejor se ajustan al perfil de cada trabajador.

> *(Insertar imagen del grafo Top 3.)*

---

# Visualización en Power BI

Para complementar el análisis se desarrolló un dashboard interactivo utilizando Power BI Desktop.

Cada uno de los datasets generados mediante Python fue utilizado para construir distintas visualizaciones.

## Hoja 1 — Distribución de compatibilidades

La primera hoja utiliza el conjunto de datos correspondiente al grafo completo.

Incluye un gráfico que muestra la cantidad de relaciones empleado–tarea agrupadas por intervalos de compatibilidad (0–20 %, 20–40 %, 40–60 %, 60–80 % y 80–100 %).

Esta visualización permite conocer cómo se distribuyen todas las compatibilidades calculadas por el sistema.

> *(Insertar captura del dashboard.)*

---

## Hoja 2 — Compatibilidades altas

La segunda hoja utiliza únicamente las relaciones con compatibilidad mayor o igual al 80 %.

Se presentan dos gráficos principales:

* empleados con mayor cantidad de tareas altamente compatibles;
* tareas con mayor cantidad de empleados capaces de realizarlas.

Estas visualizaciones permiten identificar perfiles versátiles y tareas con amplia disponibilidad de personal.

> *(Insertar captura del dashboard.)*

---

## Hoja 3 — Recomendación por empleado

La tercera hoja está orientada al análisis individual.

Mediante un **segmentador (Slicer)** el usuario puede seleccionar un empleado y visualizar automáticamente:

* sus tres tareas con mayor compatibilidad;
* un gráfico de barras con dichas tareas;
* la compatibilidad promedio obtenida.

Esta vista funciona como una herramienta sencilla de recomendación de tareas basada en los resultados obtenidos por el modelo de compatibilidad.

> *(Insertar captura del dashboard.)*

---

# Resultados

El proyecto permitió desarrollar un flujo completo de procesamiento y análisis de datos:

* generación de un conjunto de datos sintético;
* cálculo automático de compatibilidades;
* construcción de grafos bipartitos;
* filtrado de relaciones relevantes;
* recomendación de tareas por empleado;
* desarrollo de un dashboard interactivo para la exploración de los resultados.

En conjunto, estas etapas muestran cómo combinar herramientas de análisis de datos y teoría de grafos para resolver un problema de asignación de tareas de forma clara e interpretable.

---

# Posibles mejoras

El proyecto puede ampliarse de diversas maneras:

* incorporar nuevas habilidades y criterios de evaluación;
* permitir que los pesos de las habilidades sean configurables por el usuario;
* utilizar bases de datos SQL en lugar de archivos Excel;
* desarrollar una interfaz gráfica para facilitar la interacción con el sistema;
* implementar algoritmos de optimización que asignen automáticamente empleados a tareas maximizando la compatibilidad global;
* desplegar la aplicación como una solución web.

---

# Autor

Proyecto desarrollado como parte de un portfolio orientado al análisis de datos, Python, teoría de grafos y Power BI.
