import pandas as pd

from funciones_proyecto import cargar_datos

empleados, tareas = cargar_datos()

# Pedimos los datos al usuario
id_empleado = int(input("Ingrese ID de empleado: "))
id_tarea = int(input("Ingrese ID de tarea: "))

# Buscamos las filas
empleado = empleados[empleados["Empleado_ID"] == id_empleado].iloc[0]
tarea = tareas[tareas["Tarea_ID"] == id_tarea].iloc[0]

#llamamos a los pesos  
from funciones_proyecto import pesos
#llamamos a la funcion
from funciones_proyecto import calcular_compatibilidad
compatibilidad = calcular_compatibilidad(
    empleado,
    tarea,
    pesos
)

# Mostramos los resultados
print("\nRESULTADO")
print(f"Empleado: {id_empleado}")
print(f"Tarea: {id_tarea}")
print(f"{compatibilidad:.2f}%")
