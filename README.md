
# INFO081-1E — PROYECTO DE PROGRAMACION
##### Estado: Entregable N°1

## Resumen

Se desarolla una aplicación llamada "TrailSim Dinamic" Esta aplicación servirá de simulacion para ejecutar escenarios donde un operario (usuario) monitorea el trafico ferroviario y puede tomar decisiones ante los eventos que se le presenten (congestión, fallas, arribos).  
La interfaz gráfica está desarrollada con Tkinter y usa imágenes para el fondo; la lógica de la simulación y el modelo de datos están en los paquetes `logic/` y `modelos/`.

El objetivo principal en esta entrega es presentar la interfaz básica, el modelo de datos (trenes, pasajeros, estaciones) y la estructura inicial para persistencia y control de eventos.

### Integrantes

- Danilo Arce Castro (Nylooooon, LeNylon, ropero-s)
- Sebastian Burgos Maldonado (Louwz777)
- Lukas Álvarez Jaramillo (Insaidaaa)
- Tomás Fabián Torres Quezadaa (BattleBeast1)

## Indicadores* 

- Hora de simulación
  - Qué: valor numérico del reloj de la simulación (`EstadoSimulacion.hora_actual`).
  - Dónde: esquina superior (cabecera) de la ventana de simulación.
  - Acción: visual (color/ícono) según fase; se actualiza cada tick.

- Ocupación de pasajeros
  - Qué: número de pasajeros en tránsito y porcentaje de ocupación de la flota (suma de `tren.capacidad()`).
  - Dónde: widget compacto (número + barra de progreso) en el panel de indicadores.
  - Acción: alerta si % > 90% para sugerir medidas (más frecuencia, reubicación de trenes).

## Persistencia de datos

- Carpeta: `data/` en la raíz del proyecto (el sistema de guardado debe crearla si no existe).
- Formatos que se usarán:
  - JSON -> objetos del dominio (trenes, estaciones, configuración). Ej.: `data/trenes.json`, `data/estaciones.json`.
  - Parquet -> datos de pasajeros (p. ej. `data/pasajeros.parquet`) para eficiencia en tablas grandes.

  - CSV -> Datos de la simulación, donde cada fila será un guardado distinto y cada columna un dato diferente.

- Responsable: `logic/sistema_guardado/sistema_guardado.py` (métodos `guardar_simulacion` / `cargar_simulacion`).

## Archivos principales ejecutables y ejemplo de ejecución

Lista de entradas ejecutables principales:

- `chuchu.Py` (archivo principal) — arranca la aplicación llamando a `interfaz.ventanas.window.ventana_principal()`.
- `interfaz/ventanas/window.py` — contiene la interfaz principal y puede ejecutarse directamente como módulo.

Recomendación: ejecutar desde la raíz del proyecto. 

## Ejecucion del programa (en *powershell*)  
##### Situarse en la raíz del proyecto:  
`> cd "c:\ruta_de_la_carpeta\INFO081-1E-ProyectoTrenes"`

##### Opción 1: ejecutar el lanzador principal
`> python chuchu.Py`

##### Opción 2: ejecutar la ventana principal como módulo (recomendado para respetar imports relativos)
`> python -m interfaz.ventanas.window`

### Ideas para proxima entrega:

- `logic/sistema_guardado/sistema_guardado.py` tiene stubs y requiere implementación para guardar/cargar JSON y Parquet.
- `modelos/clases.py` incluye `convertir_dicc()` en las entidades, lo que facilita serialización.
- En siguientes entregas conviene añadir tests unitarios para serialización y un pequeño script de integración que guarde/cargue un estado de ejemplo.
