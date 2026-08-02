import pandas as pd
import networkx as nx
from pyvis.network import Network

from funciones_proyecto import cargar_datos, calcular_compatibilidad, pesos

# 1. Cargar datos
empleados, tareas = cargar_datos()

# 2. Calcular todas las conexiones empleado–tarea
# Con 75 empleados y 30 tareas, habrá 75 × 30 = 2.250 conexiones.
aristas = []

# Recorremos todos los empleados.
for _, emp in empleados.iterrows():
    # Para cada empleado, recorremos todas las tareas.
    for _, tarea in tareas.iterrows():
        score = calcular_compatibilidad(emp, tarea, pesos)

# Guardamos la conexión calculada.
        aristas.append({
            "Empleado": emp["Empleado_ID"],
            "Tarea": tarea["Tarea_ID"],
            "Compatibilidad": float(score)
        })

# Convertimos la lista de conexiones en un DataFrame.
grafo_df = pd.DataFrame(aristas)

# 3. Crear y exportar tabla de conexiones
# Creamos una columna más legible para el archivo Excel.
# Ejemplo: 82.5 pasa a mostrarse como "82.5%".
grafo_df["Compatibilidad_%"] = (
    grafo_df["Compatibilidad"].round(1).astype(str) + "%"
)
grafo_df.to_excel("grafo_completo.xlsx", index=False)

# 4. Construir el grafo bipartito con NetworkX
# Creamos un grafo no dirigido:
# una arista representa la relación entre empleado y tarea.
G = nx.Graph()

# Obtenemos las listas de IDs originales.
empleados_ids = empleados["Empleado_ID"].tolist()
tareas_ids = tareas["Tarea_ID"].tolist()

# Agregamos los empleados como un grupo del grafo bipartito.
G.add_nodes_from(empleados_ids, bipartite="empleado")
# Agregamos las tareas como el otro grupo del grafo bipartito.
G.add_nodes_from(tareas_ids, bipartite="tarea")

# Agregamos una arista por cada combinación empleado–tarea.
for _, fila in grafo_df.iterrows():
    G.add_edge(
        fila["Empleado"],
        fila["Tarea"],
        compatibilidad=fila["Compatibilidad"]
    )

# 4. Crear grafo interactivo con pyvis
# Configuramos el área donde se mostrará el grafo.
red = Network(
    height="900px",
    width="100%",
    bgcolor="#ffffff",
    font_color="#222222",
    directed=False
)

# Posiciones fijas: empleados a la izquierda, tareas a la derecha
for i, empleado in enumerate(empleados_ids):
    red.add_node(
        empleado,
        label=f"Empleado {empleado}",
        title=f"Empleado: {empleado}",
        color="#4C78A8",
        shape="dot",
        size=10,
        x=-500,
        y=i * 25,
        physics=False
    )

for i, tarea in enumerate(tareas_ids):
    red.add_node(
        tarea,
        label=f"Tarea {tarea}",
        title=f"Tarea: {tarea}",
        color="#F58518",
        shape="box",
        x=500,
        y=i * 60,
        physics=False
    )

# Aristas: color y grosor según compatibilidad
 # Recuperamos el puntaje de compatibilidad.
for _, fila in grafo_df.iterrows():
    score = fila["Compatibilidad"]
   # Definimos el color según el nivel de compatibilidad.
    if score >= 80:
        color = "#2CA02C"  # alta
    elif score >= 50:
        color = "#FFBF00"  # media
    else:
        color = "#D62728"  # baja
 # Agregamos la conexión entre el empleado y la tarea.
    red.add_edge(
        fila["Empleado"],
        fila["Tarea"],
         # value controla visualmente el grosor de la arista.
        # A mayor compatibilidad, más visible será la línea.
        value=max(score / 20, 0.2),
                # Se usa transparencia para que las 2.250 conexiones
        # no tapen completamente los nodos.
        color={"color": color, "opacity": 0.25},
        # Información visible al pasar el mouse por la arista.
        title=f"Compatibilidad: {score:.1f}%"
    )
#CONFIGURAR EL COMPORTAMIENTO DEL GRAFO
red.set_options("""
{
  "interaction": {
    "hover": true,
    "tooltipDelay": 100
  },
  "physics": {
    "enabled": false
  },
  "edges": {
    "smooth": false
  }
}
""")
# 10. GUARDAR EL GRAFO INTERACTIVO
# Genera un archivo HTML que puede abrirse en cualquier navegador.
red.write_html("grafo_bipartito.html")

print("Excel creado: grafo_completo.xlsx")
print("Grafo creado: grafo_bipartito.html")

# Grafo reducido
# Filtrar únicamente conexiones con compatibilidad alta (>= 80%)
grafo_reducido_df = grafo_df[grafo_df["Compatibilidad"] >= 80].copy()

grafo_reducido_df["Compatibilidad_Normalizada"] = grafo_reducido_df["Compatibilidad"] / 100
# Exportar tabla filtrada
grafo_reducido_df.to_excel("grafo_reducido_80.xlsx", index=False)


# Crear grafo bipartito reducido
G_reducido = nx.Graph()

# Se usan prefijos para evitar conflictos si un empleado y una tarea
# tienen el mismo número de ID.
empleados_reducidos = grafo_reducido_df["Empleado"].unique().tolist()
tareas_reducidas = grafo_reducido_df["Tarea"].unique().tolist()

G_reducido.add_nodes_from(
    [f"emp_{empleado}" for empleado in empleados_reducidos],
    bipartite="empleado"
)
G_reducido.add_nodes_from(
    [f"tar_{tarea}" for tarea in tareas_reducidas],
    bipartite="tarea"
)

for _, fila in grafo_reducido_df.iterrows():
    G_reducido.add_edge(
        f"emp_{fila['Empleado']}",
        f"tar_{fila['Tarea']}",
        compatibilidad=fila["Compatibilidad"]
    )

# Crear visualización interactiva del grafo reducido
red_reducida = Network(
    height="900px",
    width="100%",
    bgcolor="#ffffff",
    font_color="#222222",
    directed=False
)

# Empleados conectados: columna izquierda
for i, empleado in enumerate(empleados_reducidos):
    red_reducida.add_node(
        f"emp_{empleado}",
        label=f"Empleado {empleado}",
        title=f"Empleado: {empleado}",
        color="#4C78A8",
        shape="dot",
        size=12,
        x=-500,
        y=i * 35,
        physics=False
    )

# Tareas conectadas: columna derecha
for i, tarea in enumerate(tareas_reducidas):
    red_reducida.add_node(
        f"tar_{tarea}",
        label=f"Tarea {tarea}",
        title=f"Tarea: {tarea}",
        color="#F58518",
        shape="box",
        x=500,
        y=i * 70,
        physics=False
    )

# Aristas filtradas: todas son verdes porque tienen compatibilidad >= 80%
for _, fila in grafo_reducido_df.iterrows():
    score = fila["Compatibilidad"]

    red_reducida.add_edge(
        f"emp_{fila['Empleado']}",
        f"tar_{fila['Tarea']}",
        value=max(score / 20, 0.2),
        color={"color": "#2CA02C", "opacity": 0.65},
        title=f"Compatibilidad: {score:.1f}%"
    )

red_reducida.set_options("""
{
  "interaction": {
    "hover": true,
    "tooltipDelay": 100
  },
  "physics": {
    "enabled": false
  },
  "edges": {
    "smooth": false
  }
}
""")

red_reducida.write_html("grafo_bipartito_reducido_80.html")

print("Excel reducido creado: grafo_reducido_80.xlsx")
print("Grafo reducido creado: grafo_bipartito_reducido_80.html")

# Grafo reducido top 3 tareas por empleado
# Ordenamos cada empleado desde su compatibilidad más alta a la más baja
# y conservamos las primeras 3 tareas.
grafo_top3_df = (
    grafo_df
    .sort_values(
        by=["Empleado", "Compatibilidad"],
        ascending=[True, False]
    )
    .groupby("Empleado", group_keys=False)
    .head(3)
    .copy()
)
grafo_top3_df["Compatibilidad_Normalizada"] = grafo_top3_df["Compatibilidad"] / 100
# Exportar las 225 conexiones seleccionadas
grafo_top3_df.to_excel("grafo_top_3_tareas_por_empleado.xlsx", index=False)

# Comprobación: debe indicar 225 si hay 75 empleados
print(f"Cantidad de aristas del grafo Top 3: {len(grafo_top3_df)}")

# Crear el grafo con NetworkX
G_top3 = nx.Graph()

empleados_top3 = grafo_top3_df["Empleado"].unique().tolist()
tareas_top3 = grafo_top3_df["Tarea"].unique().tolist()

# Prefijos distintos para asegurar que empleados y tareas
# nunca se mezclen aunque sus IDs numéricos coincidan.
G_top3.add_nodes_from(
    [f"emp_{empleado}" for empleado in empleados_top3],
    bipartite="empleado"
)
G_top3.add_nodes_from(
    [f"tar_{tarea}" for tarea in tareas_top3],
    bipartite="tarea"
)

for _, fila in grafo_top3_df.iterrows():
    G_top3.add_edge(
        f"emp_{fila['Empleado']}",
        f"tar_{fila['Tarea']}",
        compatibilidad=fila["Compatibilidad"]
    )

# Visualización interactiva
red_top3 = Network(
    height="900px",
    width="100%",
    bgcolor="#ffffff",
    font_color="#222222",
    directed=False
)

# Nodos de empleados a la izquierda
for i, empleado in enumerate(empleados_top3):
    red_top3.add_node(
        f"emp_{empleado}",
        label=f"Empleado {empleado}",
        title=f"Empleado: {empleado}",
        color="#4C78A8",
        shape="dot",
        size=12,
        x=-500,
        y=i * 25,
        physics=False
    )

# Nodos de tareas a la derecha
for i, tarea in enumerate(tareas_top3):
    red_top3.add_node(
        f"tar_{tarea}",
        label=f"Tarea {tarea}",
        title=f"Tarea: {tarea}",
        color="#F58518",
        shape="box",
        x=500,
        y=i * 55,
        physics=False
    )

# Aristas: color según nivel de compatibilidad
for _, fila in grafo_top3_df.iterrows():
    score = fila["Compatibilidad"]

    if score >= 80:
        color = "#2CA02C"      # Alta
    elif score >= 50:
        color = "#FFBF00"      # Media
    else:
        color = "#D62728"      # Baja

    red_top3.add_edge(
        f"emp_{fila['Empleado']}",
        f"tar_{fila['Tarea']}",
        value=max(score / 20, 0.2),
        color={"color": color, "opacity": 0.65},
        title=f"Compatibilidad: {score:.1f}%"
    )

red_top3.set_options("""
{
  "interaction": {
    "hover": true,
    "tooltipDelay": 100
  },
  "physics": {
    "enabled": false
  },
  "edges": {
    "smooth": false
  }
}
""")

red_top3.write_html("grafo_bipartito_top_3.html")

print("Excel creado: grafo_top_3_tareas_por_empleado.xlsx")
print("Grafo creado: grafo_bipartito_top_3.html")