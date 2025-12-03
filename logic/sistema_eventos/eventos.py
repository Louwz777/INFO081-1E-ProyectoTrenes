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
def mostrar_evento_en_ventana(evento, aplicar_opcion):
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
        command=lambda: (aplicar_opcion(evento.opcion1), cerrar_ventana()),
        bg="white"
    ).pack(pady=5)

    # Botón opción 2
    tk.Button(
        frame,
        text=evento.opcion2.descripcion,
        command=lambda: (aplicar_opcion(evento.opcion2), cerrar_ventana()),
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
    

def crear_evento_abordaje(estado: Callable[[Any], Any] = None) -> Evento:
    """Evento que modela el abordaje y descenso de pasajeros en una estación.
    Presenta dos opciones al usuario:
    - Permitir abordar y descargar una cantidad determinada (se calcula en el evento).
    - Esperar un tiempo para intentar recoger más pasajeros (aumenta el tiempo simulado).
    """
    if not estado or not getattr(estado, 'trenes', None):
        # fallback to a simple event if no train data
        descripcion = "No hay trenes disponibles para el evento de abordaje."
        op1 = opcion(descripcion="No aplicar", efecto=lambda s: "No hay cambios.")
        op2 = opcion(descripcion="Ignorar", efecto=lambda s: "No hay cambios.")
        return Evento(nombre="Abordaje (no disponible)", descripcion=descripcion, opcion1=op1, opcion2=op2)

    tren = random.choice(estado.trenes)
    capacidad = tren.capacidad() if hasattr(tren, 'capacidad') else (tren.ccv * tren.ppv)
    current_onboard = estado.pasajeros_a_bordo.get(tren.nombre, 0)
    available_space = max(0, capacidad - current_onboard)

    # Simulate number of waiting passengers using a burst-friendly heuristic
    waiting = random.randint(0, max(1, int(capacidad * 0.4)))
    # propose drop count (passengers leaving at this station)
    dropping = random.randint(0, current_onboard) if current_onboard > 0 else 0

    descripcion = (
        f"Tren: {tren.nombre}\n" 
        f"Pasajeros a bordo: {current_onboard} / {capacidad}\n"
        f"Espacio disponible: {available_space}\n"
        f"Pasajeros esperando en estación: {waiting}\n\n"
        "Opciones:\n1) Permitir abordar & descargar pasajeros ahora.\n"
        "2) Esperar un tiempo para intentar recoger más pasajeros."
    )

    def efecto_abordar(estado_local):
        # passengers who will board = min(waiting, available_space)
        boarded = min(waiting, available_space)
        # passengers who get off = dropping
        new_onboard = max(0, current_onboard - dropping) + boarded
        estado_local.pasajeros_a_bordo[tren.nombre] = new_onboard
        restante = max(0, capacidad - new_onboard)
        return (f"Se bajaron {dropping} pasajeros y subieron {boarded}.\n"
                f"Ahora a bordo: {new_onboard}. Capacidad restante: {restante}.")

    def efecto_esperar(estado_local):
        # decide waiting time in minutes and advance simulation
        espera_min = random.choice([1, 2, 5, 10])
        # advance time
        estado_local.avanzar_tiempo(segundos=espera_min * 60)
        # after waiting, simulate new arrivals
        nuevos = random.randint(0, max(1, int(capacidad * 0.25)))
        espacio = max(0, capacidad - estado_local.pasajeros_a_bordo.get(tren.nombre, 0))
        suben = min(nuevos, espacio)
        estado_local.pasajeros_a_bordo[tren.nombre] = estado_local.pasajeros_a_bordo.get(tren.nombre, 0) + suben
        return (f"Espera de {espera_min} min. Llegaron {nuevos} pasajeros, subieron {suben}.\n"
                f"A bordo ahora: {estado_local.pasajeros_a_bordo[tren.nombre]} / {capacidad}.")

    op1 = opcion(descripcion=f"Abordar y descargar ahora (subir hasta {min(waiting, available_space)}, bajar {dropping})", efecto=efecto_abordar)
    op2 = opcion(descripcion=f"Esperar para intentar coger más (tiempo variable)", efecto=efecto_esperar)

    return Evento(nombre="Evento: Abordaje en estación", descripcion=descripcion, opcion1=op1, opcion2=op2)
    
        