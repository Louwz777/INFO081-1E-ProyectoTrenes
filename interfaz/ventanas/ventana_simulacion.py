import tkinter as tk    
import tkinter.font as tkfont
from logic.sistema_eventos.eventos import *
from logic.estado_simulacion import EstadoSimulacion
import random


def iniciar_simulacion(ventana_actual, semilla, ruta_trenes: str = None, ruta_estaciones: str = None):
    """Abre una nueva ventana de simulación y oculta la principal.
    ruta_trenes / ruta_estaciones: optional paths to JSON files to load for this run.
    """
    ventana_actual.withdraw()

    ventana_simulacion = tk.Toplevel()
    ventana_simulacion.title("Simulación en curso")
    ventana_simulacion.state('zoomed')
    ventana_simulacion.configure(bg="#e8e8e8")
    
    # Inicializa el estado de la simulación
    # si semilla no es un numero, se genera una aleatoria
    valor = semilla.get().strip()
    semilla_val = int(valor) if valor.isdigit() else random.randint(0,10000)
    # Use provided files if given, otherwise default to original files
    ruta_tr = ruta_trenes if ruta_trenes is not None else "modelos/trenes.json"
    ruta_es = ruta_estaciones if ruta_estaciones is not None else "modelos/estaciones.json"
    estado = EstadoSimulacion(semilla=semilla_val, ruta_trenes=ruta_tr, ruta_estaciones=ruta_es)
    
    # Muestra de nuevo la ventana principal
    def volver_menu():
        ventana_simulacion.destroy()
        ventana_actual.deiconify()
        ventana_actual.state('zoomed')
        estado.guardar_historial()

    boton_volver = tk.Button(
        ventana_simulacion,
        text="Volver al menú principal",
        command= volver_menu,
        font=("Arial", 14),
        bg="white",
        fg="black"
    )

    boton_volver.pack(side=tk.BOTTOM, pady=10)
    
    label_reloj = tk.Label(
        ventana_simulacion,
        text="",
        font=("Arial", 24, "bold"),
        bg="#e8e8e8",
        fg="#0066cc"
    )
    label_reloj.place(x=10, y=10)
    
    label_trenes = tk.Label(
        ventana_simulacion,
        text="",
        font=("Arial", 12),
        bg="#e8e8e8",
        fg="black",
        justify=tk.LEFT
    )
    label_trenes.place(x=10, y=60)
    
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
    

    def reanudar_tiempo():
        nonlocal pausa
        pausa = False
        ventana_simulacion.after(random.randint(5, 15) * 1000, generar_evento)
        
    pausa = False
    
    #funcion para actualizar tiempo, cada 1000ms se llama denuevo a si misma, actualizando el texto
    def actualizar_tiempo():
 
        if not pausa:
            hora, fecha = estado.actualizar_display()
 
            label_reloj.config(text=f"Hora: {hora}   Fecha: {fecha}")
            
            # Actualizar estado de los trenes
            status_text = "Estado Trenes:\n"
            
            for t in estado.trenes:
                # Usar velocidad si fue modificada por evento, sino velocidad_max
                current_speed = getattr(t, 'velocidad', t.velocidad_max)
                passengers = estado.pasajeros_a_bordo.get(t.nombre, 0)
                status_text += f"{t.nombre}: {passengers} pasajeros, {current_speed} km/h\n"
            label_trenes.config(text=status_text)
            
            estado.avanzar_tiempo(segundos=1)
        ventana_simulacion.after(1000, actualizar_tiempo)
    

    def aplicar_opcion(op):
        resultado = op.efecto(estado)
        label_eventos.config(text=str(resultado))
        nonlocal pausa
        pausa = False
        tiempo_siguiente = random.randint(5, 15) * 1000  
        ventana_simulacion.after(tiempo_siguiente, generar_evento) 

    #genera un evento al azar cada cierto tiempo         
    def generar_evento():
        nonlocal pausa
        pausa = True

        evento = crear_evento_niebla(estado)
        mostrar_evento_en_ventana(evento,estado, lambda:reanudar_tiempo())
    

              

    actualizar_tiempo()
    ventana_simulacion.after(random.randint(5, 15) * 1000,generar_evento)