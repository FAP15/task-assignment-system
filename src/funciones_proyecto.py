import pandas as pd

pesos = {
    "H1": 0.1,
    "H2": 0.2,
    "H3": 0.3,
    "H4": 0.4
}

def cargar_datos():

    # Leemos el excel
    archivo = "empresa.xlsx"

    empleados = pd.read_excel(archivo, sheet_name="Empleados")
    tareas = pd.read_excel(archivo, sheet_name="Tareas")

    return empleados, tareas

def calcular_compatibilidad(empleado, tarea, pesos):
    """
    Calcula el porcentaje de compatibilidad entre un empleado
    y una tarea usando una suma ponderada de habilidades.

    Parámetros:
        empleado : fila de DataFrame o diccionario
        tarea    : fila de DataFrame o diccionario
        pesos    : diccionario {skill: peso}

    Retorna:
        compatibilidad en porcentaje (0-100)
    """

    numerador = 0
    denominador = 0

    for skill, peso in pesos.items():

        numerador += peso * min(
            empleado[skill],
            tarea[skill]
    )

        denominador += peso * tarea[skill]

    #compatibilidad = (numerador / denominador) * 100

# Agregamos este segmento de codigo para evitar que el denominador de 0
# si el denominador es 0 automaticamente la compatibilidad sera de 100
# es decir una tarea sin requisitos puede hacerla cualquier empleado sin problemas
    if denominador == 0:
        compatibilidad = 100
    else:
        compatibilidad = (numerador / denominador) * 100

    return compatibilidad
