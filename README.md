
# INFO081-1E — PROYECTO DE PROGRAMACION
##### Estado: casi-FINALIZADO (*firma de sangre)

## Resumen / Contexto

Se desarrolla una aplicación de simulación ferroviaria donde un operario (usuario) monitorea el tráfico de trenes y toma decisiones ante eventos dinámicos como congestión, fallas mecánicas, condiciones climáticas adversas y arribos de pasajeros.

La interfaz gráfica está desarrollada con **Tkinter** con soporte para redimensionamiento dinámico e imágenes de fondo. La lógica de simulación y el modelo de datos se organizan en los paquetes `logic/`, `modelos/` y submódulos especializados para gestión de eventos y generación temporizada.

### Integrantes

- Danilo Arce Castro (Nylooooon, LeNylon, ropero-s)
- Sebastian Burgos Maldonado (Louwz777)
- Lukas Álvarez Jaramillo (Insaidaaa)
- Tomás Fabián Torres Quezada (BattleBeast1)

## Componentes Principales

### 1. Interfaz (`interfaz/`)

- **`window.py`**: Ventana principal del menú con opciones para:
  - Iniciar simulación (modo por defecto o personalizado)
  - Editar trenes y estaciones
  - Configurar semilla de aleatoriedad (0-10000)
  
- **`ventana_simulacion.py`**: Ventana de simulación activa que muestra indicadores en tiempo real y gestiona eventos.

- **`pages.py`**: Módulo de páginas de edición para trenes y estaciones con formularios interactivos.

- **`settings.py`**: Configuración centralizada (colores, posiciones de botones, tamaños de fuente responsivos).

### 2. Lógica de Simulación (`logic/`)

- **`estado_simulacion.py`**: Clase `EstadoSimulacion` que mantiene:
  - Reloj de simulación (avanza de 07:00 a 20:00, reinicia al día siguiente)
  - Lista de trenes y estaciones cargados desde JSON
  - Historial de eventos y elecciones del usuario
  - Diccionario `pasajeros_a_bordo` por tren

- **`sistema_eventos/eventos.py`**: Define:
  - Clase `Evento`: contiene nombre, descripción y dos opciones
  - Clase `opcion`: acción ejecutable con descripción y efecto
  - Función `mostrar_evento_en_ventana()`: modal bloqueante que requiere elección del usuario
  - Ejemplo: `crear_evento_niebla()` que reduce velocidad o hace esperar a un tren

### 3. Modelo de Datos (`modelos/`)

- **`clases.py`**: Define clases de dominio y funciones de persistencia:
  - Clase `tren`: nombre, velocidad, ppv (pasajeros por vagón), ccv (cantidad de vagones)
    - Método `capacidad()`: retorna ppv × ccv
  - Clase `pasajero`: id, creacion, inicio, destino, retorno
  - Clase `estacion`: nombre, poblacion, lineas, rutas
  - `guardar_objetos(datos: dict, ruta: str)`: guarda en JSON (clave única: "nombre")
  - `guardar_pasajeros(datos: dict, ruta: str)`: guarda/actualiza en Parquet
  - `cargar_objetos(archivo: str, clase)`: carga lista de objetos desde JSON

- **Archivos de datos**:
  - `trenes.json` / `trenes_default.json`
  - `estaciones.json` / `estaciones_default.json`
  - `pasajeros.parquet`

### 4. Submódulos

- **`ppdc-event-manager`** (submódulo Git):
  - Gestor de línea de eventos con prioridad y ordenamiento temporal
  - Ubicación: carpeta `ppdc-event-manager/ppdc_event_manager/`

- **`ppdc-timed-generator`** (submódulo Git):
  - Sistema de generadores temporizados para eventos aleatorios
  - Ubicación: carpeta `ppdc-timed-generator/ppdc_timed_generator/`
  - Generadores incluyen distribución uniforme

---

## Indicadores de Simulación

- **Hora de simulación**
  - **Qué**: Reloj de la simulación (`EstadoSimulacion.tiempo_actual`)
  - **Dónde**: Cabecera de la ventana de simulación
  - **Formato**: Hora (HH:MM:SS) y Fecha (DD/MM/YYYY)
  - **Comportamiento**: Avanza segundo a segundo; reinicia a las 07:00 al pasar las 20:00

- **Ocupación de pasajeros** (planeado)
  - **Qué**: Número de pasajeros en tránsito y porcentaje de ocupación de la flota
  - **Dónde**: Panel de indicadores (número + barra de progreso)
  - **Acción**: Alerta visual si ocupación > 90%

---

## Persistencia de Datos

### Formatos soportados

| Tipo de Datos | Formato | Archivo Ejemplo | Responsable |
|--------------|---------|-----------------|-------------|
| Trenes | JSON | `modelos/trenes.json` | `modelos/clases.py` |
| Estaciones | JSON | `modelos/estaciones.json` | `modelos/clases.py` |
| Pasajeros | Parquet | `modelos/pasajeros.parquet` | `guardar_pasajeros()` |
| Historial | JSON | `historial_simulacion.json` | `EstadoSimulacion.guardar_historial()` |

### Funciones principales

- **Guardado**:
  - `guardar_objetos(datos, ruta)`: JSON con clave única "nombre"
  - `guardar_pasajeros(datos, ruta)`: Parquet con clave única "id"
  - `EstadoSimulacion.guardar_historial(ruta)`: Historial de eventos y elecciones

- **Carga**:
  - `cargar_objetos(archivo, clase)`: Retorna lista de objetos instanciados
  - `json_dicc(ruta)`: Retorna diccionario crudo desde JSON

---

## Ejecución del Programa

### Requisitos

- Python 3.7+
- Tkinter (incluido con Python)
- pandas (para manejo de Parquet)
- PIL/Pillow (para imágenes)

### Instalación de dependencias

```powershell
pip install pandas pillow pyarrow

    # en Linux/deb. based
sudo apt install python3 pip
python3 -m pip install Pillow pandas pyarrow
```

### Ejecutar desde PowerShell

1. **Situarse en la raíz del proyecto**:
   ```
   cd "c:\ruta_de_la_carpeta\INFO081-1E-ProyectoTrenes"
   ```

2. **Opción 1: Ejecutar el lanzador principal**
   ```
   python chuchu.Py
   ```

3. **Opción 2: Ejecutar la ventana principal como módulo**
   ```
   python -m interfaz.ventanas.window
   ```

### Flujo de uso

1. Al iniciar, se muestra el menú principal con:
   - Campo de entrada para semilla (0-10000)
   - Botón "INICIAR SIMULACIÓN"
   - Botones "EDICIÓN TRENES" y "EDICIÓN ESTACIONES"

2. Al hacer clic en "INICIAR SIMULACIÓN", se abre un cuadro modal para elegir:
   - **Inicio por defecto**: Usa `trenes_default.json` y `estaciones_default.json`
   - **Inicio personalizado**: Usa `trenes.json` y `estaciones.json`

3. Durante la simulación:
   - El reloj avanza automáticamente
   - Eventos aleatorios aparecen en modales bloqueantes que requieren decisión del usuario
   - Las elecciones se registran en el historial

4. Al finalizar, el historial se guarda en `historial_simulacion.json`

---