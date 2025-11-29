# Sistema de Guardado - Compatible con Tkinter

## Resumen de cambios

El archivo `sistema_guardado.py` ha sido modificado para ser completamente compatible con interfaces gráficas de Tkinter, manteniendo compatibilidad con uso en consola.

## Nuevas funcionalidades

### 1. **Callback de mensajes para GUI**
```python
# Uso sin GUI (consola)
sistema = SistemaGuardado()

# Uso con GUI (Tkinter)
def mi_callback(mensaje):
    mi_label.config(text=mensaje)

sistema = SistemaGuardado(callback_mensaje=mi_callback)
```

### 2. **Métodos auxiliares para Tkinter**
- `seleccionar_carpeta_datos_gui(ventana_padre)` - Diálogo para seleccionar carpeta
- `guardar_como_gui(estado, ventana_padre)` - Guardar con diálogo de carpeta
- `cargar_desde_gui(ventana_padre)` - Cargar con diálogo de carpeta

### 3. **Todos los mensajes redirigibles**
Todos los `print()` han sido reemplazados por `self._mostrar_mensaje()` que:
- Si hay `callback_mensaje`: envía el mensaje a la GUI
- Si no hay callback: usa `print()` para consola

## Estructura del código

### Métodos por formato:

#### **JSON** (trenes, estaciones, configuración)
- `guardar_json(datos, nombre_archivo)`
- `cargar_json(nombre_archivo)`

#### **Parquet** (pasajeros)
- `guardar_pasajeros_parquet(pasajeros, nombre_archivo)`
- `cargar_pasajeros_parquet(nombre_archivo)`

#### **CSV** (historial de simulación)
- `guardar_simulacion_csv(datos_simulacion, nombre_archivo)`
- `cargar_simulacion_csv(nombre_archivo)`

#### **Principales** (orquestadores)
- `guardar_simulacion(estado)` - Guarda todo usando los 3 formatos
- `cargar_simulacion()` - Carga todo desde los 3 formatos

#### **Auxiliares Tkinter**
- `seleccionar_carpeta_datos_gui(ventana_padre)`
- `guardar_como_gui(estado, ventana_padre)`
- `cargar_desde_gui(ventana_padre)`

## Ejemplo de uso en tu aplicación

### Integración básica en `window.py`:

```python
from logic.sistema_guardado.sistema_guardado import SistemaGuardado

class VentanaPrincipal:
    def __init__(self):
        # ... tu código existente ...
        
        # Crear área para mensajes (opcional)
        self.label_estado = tk.Label(self, text="")
        self.label_estado.pack()
        
        # Inicializar sistema de guardado
        self.sistema_guardado = SistemaGuardado(
            carpeta_datos="data",
            callback_mensaje=self.mostrar_mensaje
        )
        
        # Crear botones
        btn_guardar = tk.Button(self, text="Guardar", 
                               command=self.guardar_simulacion)
        btn_cargar = tk.Button(self, text="Cargar", 
                              command=self.cargar_simulacion)
    
    def mostrar_mensaje(self, mensaje):
        """Callback para mostrar mensajes en la GUI"""
        self.label_estado.config(text=mensaje)
    
    def guardar_simulacion(self):
        """Guardar estado actual"""
        estado = self.obtener_estado()  # Tu método
        if self.sistema_guardado.guardar_simulacion(estado):
            messagebox.showinfo("Éxito", "Guardado correctamente")
    
    def cargar_simulacion(self):
        """Cargar estado guardado"""
        datos = self.sistema_guardado.cargar_simulacion()
        if datos:
            self.restaurar_estado(datos)  # Tu método
            messagebox.showinfo("Éxito", "Cargado correctamente")
```

## 🧪 Probar el ejemplo

Para ver una demostración completa:

```bash
cd c:\Users\sebit\OneDrive\Desktop\proyecto progra\INFO081-1E-ProyectoTrenes
python -m logic.sistema_guardado.ejemplo_uso_tkinter
```

Esto abrirá una ventana de ejemplo que muestra:
- Cómo los mensajes se redirigen a la GUI
- Uso de botones para guardar/cargar
- Diálogos para seleccionar carpetas personalizadas

## 📦 Dependencias

Revisa que tengas estas dependencias instaladas:
- pandas
- pyarrow
- tkinter (viene con Python)

## ✨ Características adicionales

1. **Manejo de errores**: Todos los métodos capturan excepciones y muestran mensajes claros
2. **Timestamp automático**: Los guardados en CSV incluyen timestamp automáticamente
3. **Creación automática de carpeta**: La carpeta `data/` se crea si no existe
4. **Compatibilidad con `convertir_dicc()`**: Detecta automáticamente si las clases tienen este método
5. **Retrocompatibilidad**: Funciona igual que antes si no se usa callback