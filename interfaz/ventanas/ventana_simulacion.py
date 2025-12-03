import tkinter as tk    
import tkinter.font as tkfont
from logic.sistema_eventos.eventos import *
from logic.estado_simulacion import EstadoSimulacion
from tkinter import messagebox, simpledialog
import random


def iniciar_simulacion(ventana_actual, semilla, ruta_tren: str = None, ruta_est: str = None):
    """Tu versión original, no la toco."""
    ventana_actual.withdraw()

    ventana_simulacion = tk.Toplevel()
    ventana_simulacion.title("Simulación en curso")
    ventana_simulacion.state('zoomed')
    ventana_simulacion.configure(bg="#e8e8e8")
    
    # Inicializa el estado de la simulación
    valor = semilla.get().strip()
    semilla_val = int(valor) if valor.isdigit() else random.randint(0,10000)
    ruta_tr = ruta_tren if ruta_tren is not None else "modelos/trenes.json"
    ruta_es = ruta_est if ruta_est is not None else "modelos/estaciones.json"
    estado = EstadoSimulacion(semilla=semilla_val, ruta_tren=ruta_tr, ruta_est=ruta_es)
    
    def volver_menu():
        respuesta = messagebox.askyesnocancel(
            "Volver al menú principal",
            "¿Quieres guardar tu simulación antes de volver al menú principal?"
        )

        if respuesta is None:
            return

        if respuesta:
            nombre = simpledialog.askstring(
                "Guardar simulación",
                "Escribe un nombre para tu guardado:"
            )
            if nombre:
                try:
                    estado.guardar_simulacion(nombre)
                    messagebox.showinfo(
                        "Guardado exitoso",
                        f"Tu simulación se ha guardado como '{nombre}'."
                    )
                except Exception as e:
                    messagebox.showerror(
                        "Error al guardar",
                        f"No se pudo guardar la simulación:\n{e}"
                    )
                    return

        try:
            estado.guardar_historial()
        except Exception:
            pass

        ventana_simulacion.destroy()
        ventana_actual.deiconify()
        ventana_actual.state('zoomed')

    boton_volver = tk.Button(
        ventana_simulacion,
        text="Volver al menú principal",
        command=volver_menu,
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
        estado.segundos_desde_ultimo_evento = 0
        estado.proximo_evento = random.randint(5, 15)
        
        
    #funcion para saltar al siguiente evento
    #max pq sino puede saltar atras si ya paso el evento
    #toda la funcion que tenia estaba mala, esto esta casi completamente hecho con IA
    def saltar_siguiente_evento():
        nonlocal pausa
        pausa = False

        # segundos hasta el próximo evento
        segundos_a_saltar = max(0, estado.proximo_evento - estado.segundos_desde_ultimo_evento)

        #generar pasajeros
        estado.generar_pasajeros_en_estaciones(segundos=segundos_a_saltar)
        # Avanzar tiempo
        estado.avanzar_tiempo(segundos=segundos_a_saltar)
        estado.segundos_desde_ultimo_evento = estado.proximo_evento

    
    boton_saltar = tk.Button(
    ventana_simulacion,
    text="Saltar al siguiente evento",
    command=saltar_siguiente_evento,
    font=("Arial", 14),
    bg="yellow",
    fg="black"
    )
    boton_saltar.pack(side=tk.BOTTOM, pady=10)

        
    #funcion para actualizar tiempo, cada 1000ms se llama denuevo a si misma, actualizando cosas
    pausa = False
    def actualizar_tiempo():
        if not pausa:
            
            #actualizar fecha y hora
            hora, fecha = estado.actualizar_display()
            label_reloj.config(text=f"Hora: {hora}   Fecha: {fecha}")
            
            status_text = "Estado Trenes:\n"
            for t in estado.trenes:
                # velocidad_actual es tu atributo dinámico
                current_speed = getattr(t, 'velocidad_actual', t.velocidad_max)
                passengers = estado.pasajeros_a_bordo.get(t.nombre, 0)
                status_text += f"{t.nombre}: {passengers} pasajeros, {current_speed} km/h\n"
            label_trenes.config(text=status_text)
            
            #mostrar en pantalla los pasajeros 
            status_pasajeros = "Pasajeros en estaciones:\n"
            for est in estado.estaciones:
                status_pasajeros += f"{est.nombre}: {len(est.pasajeros_esperando)} esperando\n"
            label_eventos.config(text=status_pasajeros)
            
            #manejo de tiempos
            estado.avanzar_tiempo(segundos=1)
            estado.segundos_desde_ultimo_evento += 1
            
            #genera eventos si paso el tiempo 
            if estado.segundos_desde_ultimo_evento >= estado.proximo_evento:
                generar_evento()
        
            # Genera pasajeros cada minuto
            if estado.tiempo_actual.second % 60 == 0:  
                for est in estado.estaciones:
                    nuevos_pasajeros = est.generar_pasajeros(1, estado.estaciones)  # 1 minuto de simulación
                    est.pasajeros_esperando.extend(nuevos_pasajeros)
            
            
        ventana_simulacion.after(1000, actualizar_tiempo)
    

    def generar_evento():
        nonlocal pausa
        pausa = True

        evento = crear_evento_niebla(estado)
        mostrar_evento_en_ventana(evento,estado, lambda:reanudar_tiempo())
        
    actualizar_tiempo()

