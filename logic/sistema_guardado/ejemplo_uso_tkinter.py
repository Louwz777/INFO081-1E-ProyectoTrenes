"""
Ejemplo de uso del sistema de guardado con Tkinter.
Este archivo demuestra cómo integrar el SistemaGuardado en una interfaz gráfica.
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
from logic.sistema_guardado.sistema_guardado import SistemaGuardado 
# ^ para que funcione el sistema de guardado se debe agregar la carpeta logic al path del proyecto


class EjemploGUI:
    """
    Ejemplo de interfaz gráfica que usa el SistemaGuardado.
    Muestra cómo integrar el sistema de guardado con callbacks y diálogos.
    """
    
    def __init__(self):
        # Crear ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Ejemplo - Sistema de Guardado con Tkinter")
        self.ventana.geometry("600x400")
        
        # Crear área de texto para mostrar mensajes
        self.area_mensajes = scrolledtext.ScrolledText(
            self.ventana,
            width=70,
            height=20,
            wrap=tk.WORD
        )
        self.area_mensajes.pack(padx=10, pady=10)
        
        # Inicializar el sistema de guardado con callback
        # El callback redirige los mensajes al área de texto de la GUI
        self.sistema_guardado = SistemaGuardado(
            carpeta_datos="data",
            callback_mensaje=self.mostrar_mensaje_en_gui
        )
        
        # Frame para botones
        frame_botones = tk.Frame(self.ventana)
        frame_botones.pack(pady=10)
        
        # Botones de acción
        btn_guardar = tk.Button(
            frame_botones,
            text="Guardar Simulación",
            command=self.ejemplo_guardar,
            width=20
        )
        btn_guardar.grid(row=0, column=0, padx=5)
        
        btn_cargar = tk.Button(
            frame_botones,
            text="Cargar Simulación",
            command=self.ejemplo_cargar,
            width=20
        )
        btn_cargar.grid(row=0, column=1, padx=5)
        
        btn_guardar_como = tk.Button(
            frame_botones,
            text="Guardar Como...",
            command=self.ejemplo_guardar_como,
            width=20
        )
        btn_guardar_como.grid(row=1, column=0, padx=5, pady=5)
        
        btn_cargar_desde = tk.Button(
            frame_botones,
            text="Cargar Desde...",
            command=self.ejemplo_cargar_desde,
            width=20
        )
        btn_cargar_desde.grid(row=1, column=1, padx=5, pady=5)
        
        # Mensaje inicial
        self.mostrar_mensaje_en_gui("Sistema de guardado inicializado.")
        self.mostrar_mensaje_en_gui("Usa los botones para probar las funcionalidades.\n")
    
    def mostrar_mensaje_en_gui(self, mensaje):
        """
        Callback para mostrar mensajes en el área de texto de la GUI.
        Este es el método que se pasa al SistemaGuardado como callback_mensaje.
        
        Args:
            mensaje (str): Mensaje a mostrar.
        """
        self.area_mensajes.insert(tk.END, mensaje + "\n")
        self.area_mensajes.see(tk.END)  # Auto-scroll al final
    
    def crear_estado_ejemplo(self):
        """
        Crea un objeto de estado de ejemplo para demostración.
        En tu aplicación real, esto sería tu EstadoSimulacion con datos reales.
        """
        class EstadoEjemplo:
            def __init__(self):
                self.hora_actual = 150
                self.trenes = [
                    {"id": 1, "nombre": "Tren Express", "velocidad": 80},
                    {"id": 2, "nombre": "Tren Local", "velocidad": 60}
                ]
                self.estaciones = [
                    {"id": 1, "nombre": "Estación Central", "capacidad": 500},
                    {"id": 2, "nombre": "Estación Sur", "capacidad": 300}
                ]
                self.pasajeros = [
                    {"id": 1, "nombre": "Juan", "destino": "Sur"},
                    {"id": 2, "nombre": "María", "destino": "Central"},
                    {"id": 3, "nombre": "Pedro", "destino": "Norte"}
                ]
                self.configuracion = {
                    "velocidad_max": 100,
                    "capacidad_total": 800
                }
        
        return EstadoEjemplo()
    
    def ejemplo_guardar(self):
        """
        Ejemplo de guardar usando la carpeta por defecto (data/).
        """
        estado = self.crear_estado_ejemplo()
        resultado = self.sistema_guardado.guardar_simulacion(estado)
        
        if resultado:
            messagebox.showinfo("Éxito", "Simulación guardada correctamente en 'data/'")
        else:
            messagebox.showerror("Error", "No se pudo guardar la simulación")
    
    def ejemplo_cargar(self):
        """
        Ejemplo de cargar desde la carpeta por defecto (data/).
        """
        datos = self.sistema_guardado.cargar_simulacion()
        
        if datos:
            messagebox.showinfo("Éxito", "Simulación cargada correctamente desde 'data/'")
        else:
            messagebox.showwarning("Advertencia", "No se pudo cargar la simulación")
    
    def ejemplo_guardar_como(self):
        """
        Ejemplo de guardar usando un diálogo para seleccionar carpeta.
        """
        estado = self.crear_estado_ejemplo()
        resultado = self.sistema_guardado.guardar_como_gui(estado, self.ventana)
        
        if resultado:
            messagebox.showinfo("Éxito", "Simulación guardada en carpeta personalizada")
    
    def ejemplo_cargar_desde(self):
        """
        Ejemplo de cargar usando un diálogo para seleccionar carpeta.
        """
        datos = self.sistema_guardado.cargar_desde_gui(self.ventana)
        
        if datos:
            messagebox.showinfo("Éxito", "Simulación cargada desde carpeta personalizada")
    
    def ejecutar(self):
        """
        Inicia el bucle principal de la interfaz gráfica.
        """
        self.ventana.mainloop()


# ==================== EJEMPLO DE USO EN TU APLICACIÓN REAL ====================

def ejemplo_integracion_en_tu_app():
    """
    Ejemplo de cómo integrar el SistemaGuardado en tu aplicación.
    
    Para usar en tu interfaz (interfaz/ventanas/window.py):
    
    1. Importar el sistema:
       from logic.sistema_guardado.sistema_guardado import SistemaGuardado
    
    2. En el __init__ de tu ventana principal:
       
       # Crear callback para mostrar mensajes en tu GUI
       def mi_callback_mensaje(mensaje):
           # Opción A: Mostrar en un widget Text o Label
           self.mi_label_estado.config(text=mensaje)
           
           # Opción B: Mostrar en consola de logs
           self.area_logs.insert(tk.END, mensaje + "\\n")
           
           # Opción C: Usar messagebox para mensajes importantes
           if "Error" in mensaje:
               messagebox.showerror("Error", mensaje)
       
       # Inicializar el sistema de guardado
       self.sistema_guardado = SistemaGuardado(
           carpeta_datos="data",
           callback_mensaje=mi_callback_mensaje
       )
    
    3. En tus botones de guardar/cargar:
       
       def on_click_guardar(self):
           # Obtener el estado actual de tu simulación
           estado = self.obtener_estado_simulacion()
           
           # Guardar
           if self.sistema_guardado.guardar_simulacion(estado):
               messagebox.showinfo("Éxito", "Guardado correctamente")
       
       def on_click_cargar(self):
           # Cargar datos
           datos = self.sistema_guardado.cargar_simulacion()
           
           if datos:
               # Reconstruir tu estado desde los datos cargados
               self.restaurar_estado_desde_datos(datos)
               messagebox.showinfo("Éxito", "Cargado correctamente")
    """
    pass


if __name__ == "__main__":
    # Ejecutar el ejemplo de GUI
    app = EjemploGUI()
    app.ejecutar()
