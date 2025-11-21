"""
Módulo para el sistema de guardado de la simulación.
"""
import json
from tkinter import filedialog, messagebox
class SistemaGuardado:
    """
    Clase encargada de guardar y cargar el estado de la simulación.
    """
    def guardar_simulacion(self, estado, ventana_principal):
        """
        Guarda el estado de la simulación.
        Args:
            estado (EstadoSimulacion): El estado actual de la simulación a guardar.
            ventana_principal: Ventana de tkinter.
        """
        archivo = filedialog.asksaveasfilename(
            parent=ventana_principal,
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
        )
        if not archivo:
            return
        try:
            with open(archivo, 'w') as f:
                json.dump(estado, f , indent=4)
            messagebox.showinfo("Guardar Simulación", "Simulación guardada exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la simulación: {e}")
    def cargar_simulacion(self, ventana_principal):
        """
        Carga el estado de la simulación desde un archivo JSON.
        Args:
            ventana_principal: Ventana de tkinter (root).
        Returns:
            dict: El estado cargado de la simulación, o None si falla.
        """
        archivo = filedialog.askopenfilename(
            parent=ventana_principal,
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        if not archivo:
            return None
        try:
            with open(archivo, 'r') as f:
                estado = json.load(f)
            messagebox.showinfo("Cargado", "Simulación cargada exitosamente.")
            return estado
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la simulación: {e}")
            return None
