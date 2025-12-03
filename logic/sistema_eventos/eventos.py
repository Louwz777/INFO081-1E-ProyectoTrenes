"""
Eventos aleatorios que pueden ocurrir durante la simulacion
cada evento tendra una descripcion y dos opciones a escoger.
se guardara cada opcion elegida por el usuario.
"""
from __future__ import annotations
from typing import Callable,Any
import random;
import tkinter as tk

"""
ventana para eventos
"""
def mostrar_evento_en_ventana(evento, estado,continuar):
    ventana = tk.Toplevel()
    ventana.title(evento.nombre)
    ventana.geometry("400x300")
    ventana.configure(bg="#ffe6e6")
    
    
    # Deshabilitar el cierre de la ventana, porque no puedes escapar tus responsabilidades, tienes que elegir
    def evitar_cierre():
        if not ventana.allowed_close:
            pass
    def cerrar_ventana():
        ventana.allowed_close = True
        ventana.destroy()
        continuar()
        
    ventana.allowed_close = False
    ventana.protocol("WM_DELETE_WINDOW", lambda: evitar_cierre())

    tk.Label(
        ventana,
        text=evento.nombre,
        font=("Arial", 18, "bold"),
        bg="#ffe6e6",
        fg="red"
    ).pack(pady=10)

    tk.Label(
        ventana,
        text=evento.descripcion,
        font=("Arial", 12),
        bg="#ffe6e6"
    ).pack(pady=10)

    frame = tk.Frame(ventana, bg="#ffe6e6")
    frame.pack(pady=20)

    # Botón opción 1
    tk.Button(
        frame,
        text=evento.opcion1.descripcion,
        command=lambda: (evento.opcion1.ejecutar_efecto(estado, evento.nombre), cerrar_ventana()),
        bg="white"
    ).pack(pady=5)

    # Botón opción 2
    tk.Button(
        frame,
        text=evento.opcion2.descripcion,
        command=lambda: (evento.opcion2.ejecutar_efecto(estado, evento.nombre), cerrar_ventana()),
        bg="white"
    ).pack(pady=5)

    return ventana

"""
clases para eventos y opciones
"""
class opcion:
    def __init__(self,descripcion:str,efecto: Callable[[Any], Any] = None):
        """
        Inicializa una opción con su descripción y su efecto.
        Args:
            descripcion (str): Descripción de la opción.
            efecto (callable): Función que representa el efecto de la opción.
        """
        self.descripcion = descripcion
        self.efecto = efecto
        
    def ejecutar_efecto(self, estado, nombre_evento: str):
        #guarda la eleccion en el historial
        estado.historial_elecciones.append(self.descripcion)
        estado.historial_eventos.append(nombre_evento)
        return self.efecto(estado)

class Evento:
    def __init__(self,nombre:str, descripcion:str, opcion1:opcion,opcion2:opcion):
        """
        Inicializa un evento con su descripción y opciones.
        
        Args:
            descripcion (str): Descripción del evento.
            opciones (list): Lista de opciones disponibles para el evento.
        """
        self.nombre = nombre
        self.descripcion = descripcion
        self.opcion1 = opcion1
        self.opcion2 = opcion2

     
"""
funciones para crear eventos
"""
 
def crear_evento_niebla(estado:Callable[[Any], Any] = None)->Evento:
    """
    Escoge un tren al azar y crea un evento de niebla que afecta su velocidad.
    la idea es que ocurra cuando el tren este esperando en una estacion, sino no tiene sentido.
    """
    tren = random.choice(estado.trenes)
    
    efecto_reducir_velocidad= lambda s: (
        setattr(tren, 'velocidad', tren.velocidad * 0.5),
        f"La velocidad del tren {tren.nombre} se ha reducido a {tren.velocidad} km/h debido a la niebla."
    )
    
    #FALTA IMPLEMENTAR EFECTO DE ESPERAR
    efecto_esperar= lambda s: (
        f"El tren {tren.nombre} va a esperar hasta que la niebla se disipe."  
    )
        
    

    descripcion_evento = f"Hay una densa niebla que afecta al tren {tren.nombre}. ¿Qué deseas hacer?"
    opcion1 = opcion(
        descripcion="hacer que el tren vaya a menor velocidad.", 
        efecto=efecto_reducir_velocidad
    )
    opcion2= opcion(
        descripcion="Hacer que el tren espere hasta que la niebla se disipe.",
        efecto=efecto_esperar
    )
    return Evento(
        nombre="Niebla densa",
        descripcion=descripcion_evento,
        opcion1=opcion1,
        opcion2=opcion2
    )
    
        