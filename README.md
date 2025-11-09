# INFO081-1E-ProyectoTrenes
(Estado: **Entrega N°1**).  

### Resumen:
Se desarrolla una aplicación de nombre “TrailSim Dinamic” la cual busca servir como simulador de gestión de trafico ferroviario en tiempo real (simulado), dando la posibilidad de ejecutar diversos escenarios en los que el operario deberá gestionar diversos eventos que se puedan desarrollar en la simulación.

### Descripción de los dos indicadores utilizados en la interfaz:
Cantidad de Pasajeros a bordo y Tiempo restante para llegar al destino.

### Como se buscan implementar las persistencias de datos.
Se usará el formato .json, para guardar la configuración inicial que incluye las estaciones, los tipos de trenes y los tipos de eventos.

Se eligió .csv para almacenar el estado de la simulación. Cada fila será un guardado distinto y cada columna un dato diferente.

La lista de pasajeros incluirá un numero identificador, lugar de inicio, destino, horas de llegada y vuelta. Las cuales se almacenará en un archivo de formato .parquet, el cual se eligió por sobre 
.csv por su capacidad para almacenar los miles de millones de datos de los habitantes.


### Estudiantes participantes:
  Danilo Arce Castro (Nylooooon, LeNylon, ropero-s).  
  Sebastian Burgos Maldonado (Louwz777).  
  Lukas Álvarez Jaramillo (Insaidaaa).  
  Tomás Fabián Torres Quezadaa (BattleBeast1).
