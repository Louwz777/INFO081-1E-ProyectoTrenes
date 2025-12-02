"""
Módulo para el manejo del estado de la simulación.
"""
from datetime import datetime, timedelta
from modelos.clases import *
from logic.sistema_eventos.eventos import crear_evento_niebla
import random;


class EstadoSimulacion:

    def __init__(self, fecha_inicio_str="2015-01-01 07:00:00",semilla=random.randint(0,10000)):
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
        
        #parametros adicionales 
        
        self.historial_eventos = []
        self.historial_elecciones = []
        
        self.trenes= cargar_objetos("modelos/trenes.json", tren)
        self.estaciones= cargar_objetos("modelos/estaciones.json", estacion)
        
        

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
        return self.tiempo_actual

    def generador_eventos(self):
        """
        Genera eventos de forma aleatoria.
        Returns:
            str: Descripción del evento generado.
        no se utiliza actualmente, ya que window llama a eventos directamente.
        """
        eventos = [
            crear_evento_niebla(self)
        ]
        evento = random.choice(eventos)
        return evento

    def __str__(self):
        hora, fecha = self.actualizar_display()
        return f"EstadoSimulacion(hora_actual={hora}, fecha={fecha})"
        
