import sys
import os
import tkinter as tk    
import tkinter.font as tkfont
from logic.sistema_eventos.eventos import crear_evento_niebla
from logic.estado_simulacion import EstadoSimulacion
import random


def iniciar_simulacion(ventana_actual,semilla):
    """Abre una nueva ventana de simulación y oculta la principal."""
    ventana_actual.withdraw()  

    ventana_simulacion = tk.Toplevel()
    ventana_simulacion.title("Simulación en curso")
    ventana_simulacion.geometry("800x600")
    ventana_simulacion.configure(bg="#e8e8e8")
    
    # Inicializa el estado de la simulación
    #si semilla no es un numero, se genera una aleatoria
    valor = semilla.get().strip()
    semilla =int(valor) if valor.isdigit() else random.randint(0,10000)
    estado=EstadoSimulacion(semilla=int(semilla))
    
 # Muestra de nuevo la ventana principal
    def volver_menu():
        ventana_simulacion.destroy()
        ventana_actual.deiconify() 

    boton_volver = tk.Button(
        ventana_simulacion,
        text="Volver al menú principal",
        command=volver_menu,
        font=("Arial", 14),
        bg="white",
        fg="black"
    )
    # Place the return button at the bottom so it is always visible
    boton_volver.pack(side=tk.BOTTOM, pady=10)
    

    
    label_reloj = tk.Label(
        ventana_simulacion,
        text="",
        font=("Arial", 24, "bold"),
        bg="#e8e8e8",
        fg="#0066cc"
    )
    label_reloj.pack(pady=100)
    
    label_eventos = tk.Label(
        ventana_simulacion,
        text="",
        font=("Arial", 24, "bold"),
        bg="#e8e8e8",
        fg="#cc0000"
        )
    label_eventos.pack(pady=20)
    
    frame_opciones = tk.Frame(ventana_simulacion, bg="#e8e8e8")
    frame_opciones.pack(pady=20)
    

    
    #funcion para actualizar tiempo, cada 1000ms se llama denuevo a si misma, actualizando el texto
    
    pausa = False
    
    def actualizar_tiempo():
        # Update clock display every second. If there's an active event message
        # show a short version of it alongside the hour (e.g. "Niebla densa").
        if not pausa:
            hora, fecha = estado.actualizar_display()
            # get first line of event text (if any) to keep clock concise
            evento_text = label_eventos.cget('text') or ""
            if evento_text:
                primera_linea = evento_text.splitlines()[0]
                label_reloj.config(text=f"Hora: {hora}   Fecha: {fecha}   - {primera_linea}")
            else:
                label_reloj.config(text=f"Hora: {hora}   Fecha: {fecha}")
            estado.avanzar_tiempo(segundos=1)
        ventana_simulacion.after(1000, actualizar_tiempo)

    def aplicar_opcion(op):
        resultado = op.efecto(estado)
        label_eventos.config(text=str(resultado))
        nonlocal pausa
        pausa = False

    #genera un evento al azar cada cierto tiempo         
    def generar_evento():
        nonlocal pausa
        pausa = True

        evento = crear_evento_niebla(estado)
        # Show the full event text in the events label
        label_eventos.config(text=f"Evento: {evento.nombre}\n{evento.descripcion}")
        # Also update the clock immediately so the event name appears beside it
        # (the clock updater will continue including the first line of this text)
        hora, fecha = estado.actualizar_display()
        primera_linea = f"Evento: {evento.nombre}".splitlines()[0]
        label_reloj.config(text=f"Hora: {hora}   Fecha: {fecha}   - {primera_linea}")
                
        for widget in frame_opciones.winfo_children():
            widget.destroy()
        
        boton1 = tk.Button(
            frame_opciones,
            text=evento.opcion1.descripcion,
            command=lambda: aplicar_opcion(evento.opcion1),
            font=("Arial", 12),
            bg="white"
        )
        boton1.pack(pady=5)
        # Botón opción 2
        boton2 = tk.Button(
            frame_opciones,
            text=evento.opcion2.descripcion,
            command=lambda: aplicar_opcion(evento.opcion2),
            font=("Arial", 12),
            bg="white"
        )
        boton2.pack(pady=5)
    
        tiempo_siguiente = random.randint(5, 15) * 1000  
        ventana_simulacion.after(tiempo_siguiente, generar_evento) 
              

    actualizar_tiempo()
    ventana_simulacion.after(1000,generar_evento)