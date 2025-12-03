"""
Módulo para el manejo del estado de la simulación.
"""
import os
from datetime import datetime, timedelta, time
from modelos.clases import *
from logic.sistema_eventos.eventos import *
import random
import json
fecha_base="2015-01-01 07:00:00"
trenD="modelos/trenes.json"
estD="modelos/estaciones.json"

class EstadoSimulacion:

    def __init__(self, fecha_inicio_str=fecha_base,ruta_tren="trenD",ruta_est="estD", semilla=random.randint(0,10000)):
        """
        Inicializa el estado de la simulación con la hora actual y la semilla para eventos aleatorios.
        
        Args:
            fecha_inicio_str (str): Fecha y hora inicial en formato "YYYY-MM-DD HH:MM:SS".
                tiene valor predeterminado 1 de enero de 2015 a las 07:00:00.
            semilla (int): Semilla para la generación aleatoria de eventos.
                tiene valor predeterminado un número aleatorio entre 0 y 10000.
        
        """
        try:
            self.tiempo_actual = datetime.strptime(fecha_inicio_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            self.tiempo_actual = datetime(2015, 1, 1, 7, 0, 0)
        
        random.seed(semilla)
        
        #parametros guardado
        
        self.historial_eventos = []
        self.historial_elecciones = []
        
        #parametros objetos (allow custom paths for simulation runs)
        self.trenes = cargar_objetos(ruta_tren, tren)
        self.estaciones = cargar_objetos(ruta_est, estacion)
        
        #parametros tiempo
        self.proximo_evento= random.randint(0, 15)  #segundos hasta el proximo evento
        self.segundos_desde_ultimo_evento = 0
        
        #Mantiene un registro de cuantos pasajeros hay en cada tren
        #inicializa en 0 para cada tren
        try:
            self.pasajeros_a_bordo = {t.nombre: 0 for t in self.trenes}
        except Exception:
            self.pasajeros_a_bordo = {}


    def actualizar_display(self):
        """
        Devuelve la hora y la fecha formateadas.
        Returns:
            (str, str): Hora en formato "HH:MM:SS", Fecha en formato "DD/MM/YYYY"
        """
        hora = self.tiempo_actual.strftime("%H:%M:%S")
        fecha = self.tiempo_actual.strftime("%d/%m/%Y")
        return hora, fecha
    
    def avanzar_tiempo(self, segundos=1):
        """
        Avanza la hora simulado por cierta cantidad de segundos.
        Args:
            segundos (int): cantidad de segundos a avanzar.
        Returns:
            datetime: Nuevo tiempo simulado.
        """
        self.tiempo_actual += timedelta(seconds=segundos)
        
        if self.tiempo_actual.hour >= 20:
            nueva_fecha = self.tiempo_actual.date() + timedelta(days=1)
            self.tiempo_actual = datetime.combine(nueva_fecha, time(7, 0, 0))
        
        return self.tiempo_actual

    def guardar_historial(self, ruta_archivo="historial_simulacion.json"):
        """
        Guarda el historial de eventos y elecciones en un archivo JSON.
        Args:
            ruta_archivo (str): Ruta del archivo donde se guardará el historial.
        """
        historial = {
            "eventos": self.historial_eventos,
            "elecciones": self.historial_elecciones,
            "semilla": self.semilla
        }
        with open(ruta_archivo, 'w') as archivo:
            json.dump(historial, archivo, indent=4)
    
    def __str__(self):
        hora, fecha = self.actualizar_display()
        return f"EstadoSimulacion(hora_actual={hora}, fecha={fecha})"

    ##########guardar simulacion##########      
    def guardar_simulacion(self, nombre_guardado: str, carpeta="guardado"):
        """
        Guarda el estado completo de la simulación en un archivo JSON
        dentro de la carpeta indicada (por defecto 'guardado').
        """

        # Carpeta 'guardado' en la raíz del proyecto
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        carpeta_completa = os.path.join(base_dir, carpeta)
        os.makedirs(carpeta_completa, exist_ok=True)

        # --- Trenes serializables ---
        datos_trenes = []
        for t in self.trenes:
            datos_trenes.append({
                "nombre": t.nombre,
                "velocidad_max": getattr(t, "velocidad_max", None),
                "velocidad_actual": getattr(t, "velocidad", getattr(t, "velocidad_max", None)),
                "capacidad": t.capacidad() if hasattr(t, "capacidad") else None,
                "pasajeros": self.pasajeros_a_bordo.get(t.nombre, 0),
            })

        # --- Estaciones serializables ---
        datos_estaciones = []
        for e in self.estaciones:
            datos_estaciones.append({
                "nombre": e.nombre,
                "poblacion": getattr(e, "poblacion", None),
            })

        # --- Estructura general del guardado ---
        datos = {
            "tiempo_actual": self.tiempo_actual.strftime("%Y-%m-%d %H:%M:%S"),
            "historial_eventos": self.historial_eventos,
            "historial_elecciones": self.historial_elecciones,
            "pasajeros_a_bordo": self.pasajeros_a_bordo,
            "trenes": datos_trenes,
            "estaciones": datos_estaciones,
        }

        ruta_archivo = os.path.join(carpeta_completa, f"{nombre_guardado}.json")
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)