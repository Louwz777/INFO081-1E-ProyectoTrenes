"""
Módulo para el sistema de guardado de la simulación.
Maneja la persistencia de datos en formatos JSON, Parquet y CSV.
"""

import json
import csv
import os
from pathlib import Path
from datetime import datetime


class SistemaGuardado:
    """
    Clase encargada de guardar y cargar el estado de la simulación.
    Soporta tres formatos de persistencia:
    - JSON: para objetos del dominio (trenes, estaciones, configuración)
    - Parquet: para datos de pasajeros (eficiencia en tablas grandes)
    - CSV: para datos de simulación (cada fila = guardado distinto)
    """
    
    def __init__(self, carpeta_datos="data", callback_mensaje=None):
        """
        Inicializa el sistema de guardado.
        
        Args:
            carpeta_datos (str): Ruta de la carpeta donde se guardarán los datos.
                                Por defecto es 'data/' en la raíz del proyecto.
            callback_mensaje (callable, opcional): Función para mostrar mensajes en GUI.
                                                   Debe aceptar un parámetro str (mensaje).
                                                   Si es None, usa print() para consola.
        """
        self.carpeta_datos = Path(carpeta_datos)
        self.callback_mensaje = callback_mensaje
        self._crear_carpeta_datos()
    
    def _crear_carpeta_datos(self):
        """
        Crea la carpeta 'data/' si no existe.
        Esta carpeta contendrá todos los archivos de persistencia.
        """
        if not self.carpeta_datos.exists():
            self.carpeta_datos.mkdir(parents=True, exist_ok=True)
            self._mostrar_mensaje(f"Carpeta '{self.carpeta_datos}' creada exitosamente.")
    
    def _mostrar_mensaje(self, mensaje):
        """
        Muestra un mensaje usando el callback de GUI si está disponible,
        o print() si se ejecuta en consola.
        
        Args:
            mensaje (str): Mensaje a mostrar.
        """
        if self.callback_mensaje:
            self.callback_mensaje(mensaje)
        else:
            print(mensaje)
    
    # ==================== MÉTODOS PARA JSON ====================
    
    def guardar_json(self, datos, nombre_archivo):
        """
        Guarda datos en formato JSON.
        Útil para objetos del dominio como trenes, estaciones y configuración.
        
        Args:
            datos (dict o list): Datos a guardar en formato JSON.
            nombre_archivo (str): Nombre del archivo (ej: 'trenes.json').
        
        Returns:
            bool: True si se guardó exitosamente, False en caso contrario.
        """
        try:
            ruta_completa = self.carpeta_datos / nombre_archivo
            with open(ruta_completa, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            self._mostrar_mensaje(f"Datos guardados en JSON: {ruta_completa}")
            return True
        except Exception as e:
            self._mostrar_mensaje(f"Error al guardar JSON '{nombre_archivo}': {e}")
            return False
    
    def cargar_json(self, nombre_archivo):
        """
        Carga datos desde un archivo JSON.
        
        Args:
            nombre_archivo (str): Nombre del archivo (ej: 'trenes.json').
        
        Returns:
            dict o list: Datos cargados desde el archivo JSON.
                        None si el archivo no existe o hay error.
        """
        try:
            ruta_completa = self.carpeta_datos / nombre_archivo
            if not ruta_completa.exists():
                self._mostrar_mensaje(f"Archivo JSON no encontrado: {ruta_completa}")
                return None
            
            with open(ruta_completa, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            self._mostrar_mensaje(f"Datos cargados desde JSON: {ruta_completa}")
            return datos
        except Exception as e:
            self._mostrar_mensaje(f"Error al cargar JSON '{nombre_archivo}': {e}")
            return None
    
    # ==================== MÉTODOS PARA PARQUET ====================
    
    def guardar_pasajeros_parquet(self, pasajeros, nombre_archivo="pasajeros.parquet"):
        """
        Guarda datos de pasajeros en formato Parquet.
        Parquet es eficiente para tablas grandes con muchos pasajeros.
        
        Args:
            pasajeros (list): Lista de diccionarios con datos de pasajeros.
            nombre_archivo (str): Nombre del archivo (ej: 'pasajeros.parquet').
        
        Returns:
            bool: True si se guardó exitosamente, False en caso contrario.
        
        Nota:
            Requiere la librería 'pyarrow' o 'fastparquet'.
            Instalar con: pip install pyarrow
        """
        try:
            import pandas as pd
            
            # Convertir lista de pasajeros a DataFrame
            df = pd.DataFrame(pasajeros)
            
            ruta_completa = self.carpeta_datos / nombre_archivo
            df.to_parquet(ruta_completa, engine='pyarrow', index=False)
            self._mostrar_mensaje(f"Pasajeros guardados en Parquet: {ruta_completa}")
            return True
        except ImportError:
            self._mostrar_mensaje("Error: Se requiere instalar 'pandas' y 'pyarrow' para usar Parquet.")
            self._mostrar_mensaje("Ejecutar: pip install pandas pyarrow")
            return False
        except Exception as e:
            self._mostrar_mensaje(f"Error al guardar Parquet '{nombre_archivo}': {e}")
            return False
    
    def cargar_pasajeros_parquet(self, nombre_archivo="pasajeros.parquet"):
        """
        Carga datos de pasajeros desde un archivo Parquet.
        
        Args:
            nombre_archivo (str): Nombre del archivo (ej: 'pasajeros.parquet').
        
        Returns:
            list: Lista de diccionarios con datos de pasajeros.
                 None si el archivo no existe o hay error.
        """
        try:
            import pandas as pd
            
            ruta_completa = self.carpeta_datos / nombre_archivo
            if not ruta_completa.exists():
                self._mostrar_mensaje(f"Archivo Parquet no encontrado: {ruta_completa}")
                return None
            
            df = pd.read_parquet(ruta_completa, engine='pyarrow')
            pasajeros = df.to_dict(orient='records')
            self._mostrar_mensaje(f"Pasajeros cargados desde Parquet: {ruta_completa}")
            return pasajeros
        except ImportError:
            self._mostrar_mensaje("Error: Se requiere instalar 'pandas' y 'pyarrow' para usar Parquet.")
            return None
        except Exception as e:
            self._mostrar_mensaje(f"Error al cargar Parquet '{nombre_archivo}': {e}")
            return None
    
    # ==================== MÉTODOS PARA CSV ====================
    
    def guardar_simulacion_csv(self, datos_simulacion, nombre_archivo="simulacion.csv"):
        """
        Guarda datos de la simulación en formato CSV.
        Cada fila representa un guardado distinto, cada columna un dato diferente.
        Si el archivo existe, agrega una nueva fila; si no, lo crea con encabezados.
        
        Args:
            datos_simulacion (dict): Diccionario con los datos de la simulación.
                                    Ej: {'hora': 10, 'pasajeros': 50, 'trenes_activos': 3}
            nombre_archivo (str): Nombre del archivo (ej: 'simulacion.csv').
        
        Returns:
            bool: True si se guardó exitosamente, False en caso contrario.
        """
        try:
            ruta_completa = self.carpeta_datos / nombre_archivo
            
            # Agregar timestamp automáticamente
            datos_simulacion['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Verificar si el archivo existe para decidir si escribir encabezados
            archivo_existe = ruta_completa.exists()
            
            with open(ruta_completa, 'a', newline='', encoding='utf-8') as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=datos_simulacion.keys())
                
                # Escribir encabezados solo si es un archivo nuevo
                if not archivo_existe:
                    escritor.writeheader()
                
                # Escribir los datos de la simulación
                escritor.writerow(datos_simulacion)
            
            self._mostrar_mensaje(f"Simulación guardada en CSV: {ruta_completa}")
            return True
        except Exception as e:
            self._mostrar_mensaje(f"Error al guardar CSV '{nombre_archivo}': {e}")
            return False
    
    def cargar_simulacion_csv(self, nombre_archivo="simulacion.csv"):
        """
        Carga todos los guardados de simulación desde un archivo CSV.
        
        Args:
            nombre_archivo (str): Nombre del archivo (ej: 'simulacion.csv').
        
        Returns:
            list: Lista de diccionarios, cada uno representa un guardado.
                 None si el archivo no existe o hay error.
        """
        try:
            ruta_completa = self.carpeta_datos / nombre_archivo
            if not ruta_completa.exists():
                print(f"Archivo CSV no encontrado: {ruta_completa}")
                return None
            
            with open(ruta_completa, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                guardados = list(lector)
            
            self._mostrar_mensaje(f"Simulaciones cargadas desde CSV: {ruta_completa} ({len(guardados)} guardados)")
            return guardados
        except Exception as e:
            self._mostrar_mensaje(f"Error al cargar CSV '{nombre_archivo}': {e}")
            return None
    
    # ==================== MÉTODOS PRINCIPALES ====================
    
    def guardar_simulacion(self, estado):
        """
        Guarda el estado completo de la simulación usando todos los formatos.
        
        Args:
            estado (EstadoSimulacion): Objeto con el estado actual de la simulación.
                                      Debe tener métodos/atributos como:
                                      - trenes (lista de trenes)
                                      - estaciones (lista de estaciones)
                                      - pasajeros (lista de pasajeros)
                                      - configuracion (dict con configuración)
                                      - hora_actual (hora de simulación)
        
        Returns:
            bool: True si todo se guardó exitosamente, False en caso contrario.
        """
        try:
            self._mostrar_mensaje("\n=== Guardando simulación ===")
            
            # 1. Guardar trenes en JSON
            if hasattr(estado, 'trenes') and estado.trenes:
                trenes_dict = [tren.convertir_dicc() if hasattr(tren, 'convertir_dicc') 
                              else tren.__dict__ for tren in estado.trenes]
                self.guardar_json(trenes_dict, "trenes.json")
            
            # 2. Guardar estaciones en JSON
            if hasattr(estado, 'estaciones') and estado.estaciones:
                estaciones_dict = [est.convertir_dicc() if hasattr(est, 'convertir_dicc') 
                                  else est.__dict__ for est in estado.estaciones]
                self.guardar_json(estaciones_dict, "estaciones.json")
            
            # 3. Guardar configuración en JSON
            if hasattr(estado, 'configuracion') and estado.configuracion:
                self.guardar_json(estado.configuracion, "configuracion.json")
            
            # 4. Guardar pasajeros en Parquet
            if hasattr(estado, 'pasajeros') and estado.pasajeros:
                pasajeros_dict = [pas.convertir_dicc() if hasattr(pas, 'convertir_dicc') 
                                 else pas.__dict__ for pas in estado.pasajeros]
                self.guardar_pasajeros_parquet(pasajeros_dict)
            
            # 5. Guardar resumen de la simulación en CSV
            resumen = {
                'hora_actual': getattr(estado, 'hora_actual', 0),
                'num_trenes': len(getattr(estado, 'trenes', [])),
                'num_estaciones': len(getattr(estado, 'estaciones', [])),
                'num_pasajeros': len(getattr(estado, 'pasajeros', []))
            }
            self.guardar_simulacion_csv(resumen)
            
            self._mostrar_mensaje("=== Simulación guardada exitosamente ===\n")
            return True
        except Exception as e:
            self._mostrar_mensaje(f"Error al guardar la simulación completa: {e}")
            return False
    
    def cargar_simulacion(self):
        """
        Carga el estado completo de la simulación desde todos los formatos.
        
        Returns:
            dict: Diccionario con todos los datos cargados:
                 {
                     'trenes': [...],
                     'estaciones': [...],
                     'pasajeros': [...],
                     'configuracion': {...},
                     'historial_guardados': [...]
                 }
                 None si no se pudo cargar ningún archivo.
        """
        try:
            self._mostrar_mensaje("\n=== Cargando simulación ===")
            
            estado_cargado = {
                'trenes': self.cargar_json("trenes.json"),
                'estaciones': self.cargar_json("estaciones.json"),
                'configuracion': self.cargar_json("configuracion.json"),
                'pasajeros': self.cargar_pasajeros_parquet(),
                'historial_guardados': self.cargar_simulacion_csv()
            }
            
            self._mostrar_mensaje("=== Simulación cargada exitosamente ===\n")
            return estado_cargado
        except Exception as e:
            self._mostrar_mensaje(f"Error al cargar la simulación completa: {e}")
            return None
    
    # ==================== MÉTODOS AUXILIARES PARA TKINTER ====================
    
    def seleccionar_carpeta_datos_gui(self, ventana_padre=None):
        """
        Abre un diálogo de Tkinter para seleccionar la carpeta de datos.
        Útil para interfaces gráficas que quieren cambiar la ubicación de guardado.
        
        Args:
            ventana_padre (tk.Tk o tk.Toplevel, opcional): Ventana padre para el diálogo.
        
        Returns:
            str: Ruta de la carpeta seleccionada, o None si se canceló.
        """
        try:
            from tkinter import filedialog
            
            carpeta = filedialog.askdirectory(
                parent=ventana_padre,
                title="Seleccionar carpeta para guardar datos",
                initialdir=str(self.carpeta_datos)
            )
            
            if carpeta:
                self.carpeta_datos = Path(carpeta)
                self._crear_carpeta_datos()
                self._mostrar_mensaje(f"Carpeta de datos cambiada a: {self.carpeta_datos}")
                return str(self.carpeta_datos)
            return None
        except ImportError:
            self._mostrar_mensaje("Error: Tkinter no está disponible.")
            return None
    
    def guardar_como_gui(self, estado, ventana_padre=None):
        """
        Permite guardar la simulación seleccionando una carpeta mediante diálogo de Tkinter.
        
        Args:
            estado (EstadoSimulacion): Estado de la simulación a guardar.
            ventana_padre (tk.Tk o tk.Toplevel, opcional): Ventana padre para el diálogo.
        
        Returns:
            bool: True si se guardó exitosamente, False en caso contrario.
        """
        carpeta_original = self.carpeta_datos
        
        if self.seleccionar_carpeta_datos_gui(ventana_padre):
            resultado = self.guardar_simulacion(estado)
            return resultado
        else:
            # Restaurar carpeta original si se canceló
            self.carpeta_datos = carpeta_original
            return False
    
    def cargar_desde_gui(self, ventana_padre=None):
        """
        Permite cargar la simulación seleccionando una carpeta mediante diálogo de Tkinter.
        
        Args:
            ventana_padre (tk.Tk o tk.Toplevel, opcional): Ventana padre para el diálogo.
        
        Returns:
            dict: Diccionario con los datos cargados, o None si se canceló o hubo error.
        """
        carpeta_original = self.carpeta_datos
        
        if self.seleccionar_carpeta_datos_gui(ventana_padre):
            resultado = self.cargar_simulacion()
            return resultado
        else:
            # Restaurar carpeta original si se canceló
            self.carpeta_datos = carpeta_original
            return None

