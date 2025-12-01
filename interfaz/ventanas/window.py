import sys
import os
import tkinter as tk    
import json
from PIL import ImageTk, Image

###ROOT
ruta_raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)


ruta_imagen = os.path.join(ruta_raiz, "interfaz", "images", "bg.png")

###IMPORTACIONES
from modelos.clases import estacion, guardar_objetos
from interfaz import settings as config


#ESTACIONES CREADAS
lista_estaciones = []

##################################################################################

def iniciar_simulacion(ventana_actual):
    """Abre una nueva ventana de simulación y oculta la principal."""
    ventana_actual.withdraw()  

    nueva = tk.Toplevel()
    nueva.title("Simulación en curso")
    nueva.geometry("800x600")
    nueva.configure(bg="#e8e8e8")

    # Mensaje dentro de la nueva ventana
    etiqueta = tk.Label(
        nueva,
        text="SIMULACION",
        font=("Arial", 20, "bold"),
        bg="#e8e8e8",
        fg="#333"
    )
    etiqueta.pack(pady=50)

    def volver_menu():
        nueva.destroy()
        ventana_actual.deiconify()  # Muestra de nuevo la ventana principal

    boton_volver = tk.Button(
        nueva,
        text="Volver al menú principal",
        command=volver_menu,
        font=("Arial", 14),
        bg="white",
        fg="black"
    )
    boton_volver.pack(pady=20)

def ventana_principal():
    ###Inicio desarrollo ventanas
    ventana = tk.Tk()
    ventana.title("Simulador para operarios")
    ventana.geometry(f"{config.ANCHO_VENTANA}x{config.ALTO_VENTANA}")
    
    ###CANVAS
    canvas = canvas = tk.Canvas(ventana, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    bg_normal = Image.open(ruta_imagen)
    bg_res = bg_normal.resize(
        (config.ANCHO_VENTANA, config.ALTO_VENTANA),
        Image.LANCZOS
    )
    imagen_fondo = ImageTk.PhotoImage(bg_res)
    canvas.create_image(0, 0, anchor="nw", image=imagen_fondo)
    canvas.image = imagen_fondo  # Mantener referencia

        # --- Función para redimensionar y mostrar el fondo ---
    def redibujar_fondo(event):
        if bg_normal:
            nueva_img = bg_normal.resize((event.width, event.height), Image.LANCZOS)
            imagen_fondo = ImageTk.PhotoImage(nueva_img)
            canvas.image = imagen_fondo  # mantener referencia
            canvas.create_image(0, 0, anchor="nw", image=imagen_fondo)

    # --- Vincular evento de redimensionamiento ---
    canvas.bind("<Configure>", redibujar_fondo)


    boton = tk.Button(
        ventana,
        text="INICIAR SIMULACIÓN",
        command=lambda: iniciar_simulacion(ventana), 
        bg=config.COLOR_BLANCO,
        fg=config.COLOR_GRIS,
        font=("Arial", 10),
        width=30,   
        height=3     
    )
    boton.place(relx=0.2, rely=0.9, anchor="center", width=200, height=100)
    
    boton_crear = tk.Button(
        ventana,
        text="CREAR ESTACIÓN",
        command=lambda: crear_estacion(ventana),
        bg=config.COLOR_AZUL,
        fg=config.COLOR_BLANCO,
        font=("Arial", 10),
        width=30,
        height=3,
        cursor="hand2"
    )
    boton_crear.place(relx=0.8, rely=0.9, anchor="center", width=200, height=100)
    boton_ver = tk.Button(
        ventana,
        text="VER ESTACIONES",
        command=lambda: ver_estaciones(ventana),
        bg=config.COLOR_VERDE,
        fg=config.COLOR_BLANCO,
        font=("Arial", 10),
        width=30,
        height=3,
        cursor="hand2"
    )
    boton_ver.place(relx=0.5, rely=0.9, anchor="center", width=200, height=100)
    ventana.mainloop()

def crear_estacion(ventana_actual):
    """Abre ventana nueva estación."""
    ventana_actual.withdraw()
    ventana_estacion = tk.Toplevel()
    ventana_estacion.title("Crear nueva estación")
    ventana_estacion.geometry("600x500")
    ventana_estacion.configure(bg=config.COLOR_GRIS)
    
    # Título
    titulo = tk.Label(
        ventana_estacion,
        text="CREAR ESTACIÓN",
        font=("Arial", 24, "bold"),
        bg=config.COLOR_GRIS,
        fg=config.COLOR_BLANCO
    )
    titulo.pack(pady=30)
    
    # Formulario
    frame_form = tk.Frame(ventana_estacion, bg=config.COLOR_GRIS)
    frame_form.pack(pady=20)
    
    #Nombre
    tk.Label(
        frame_form,
        text="Nombre de la estación:",
        font=("Arial", 12),
        bg=config.COLOR_GRIS,
        fg=config.COLOR_BLANCO
    ).grid(row=0, column=0, padx=10, pady=15, sticky="w")
    
    entry_nombre = tk.Entry(frame_form, font=("Arial", 12), width=30)
    entry_nombre.grid(row=0, column=1, padx=10, pady=15)
    
    #Población
    tk.Label(
        frame_form,
        text="Población:",
        font=("Arial", 12),
        bg=config.COLOR_GRIS,
        fg=config.COLOR_BLANCO
    ).grid(row=1, column=0, padx=10, pady=15, sticky="w")
    
    entry_poblacion = tk.Entry(frame_form, font=("Arial", 12), width=30)
    entry_poblacion.grid(row=1, column=1, padx=10, pady=15)
    
    #Líneas
    tk.Label(
        frame_form,
        text="Líneas (separadas por coma):",
        font=("Arial", 12),
        bg=config.COLOR_GRIS,
        fg=config.COLOR_BLANCO
    ).grid(row=2, column=0, padx=10, pady=15, sticky="w")
    
    entry_lineas = tk.Entry(frame_form, font=("Arial", 12), width=30)
    entry_lineas.grid(row=2, column=1, padx=10, pady=15)
    
    tk.Label(
        frame_form,
        text="Ejemplo: L1, L2, L3",
        font=("Arial", 9, "italic"),
        bg=config.COLOR_GRIS,
        fg=config.COLOR_BLANCO
    ).grid(row=3, column=1, sticky="w", padx=10)
    
    #Label mensaje
    label_mensaje = tk.Label(
        ventana_estacion,
        text="",
        font=("Arial", 11),
        bg=config.COLOR_GRIS
    )
    label_mensaje.pack(pady=10)
    
    def guardar_estacion():
        nombre = entry_nombre.get().strip()
        poblacion_str = entry_poblacion.get().strip()
        lineas_str = entry_lineas.get().strip()
        
        # Validar entradas
        if not nombre:
            label_mensaje.config(text="El nombre es obligatorio", fg=config.COLOR_ROJO)
            return
        
        if not poblacion_str.isdigit():
            label_mensaje.config(text="La población debe ser un número", fg=config.COLOR_ROJO)
            return
        
        if not lineas_str:
            label_mensaje.config(text="Debe ingresar al menos una línea", fg=config.COLOR_ROJO)
            return
        

        poblacion = int(poblacion_str)
        lineas = [linea.strip() for linea in lineas_str.split(",")]
        nueva_estacion = estacion(nombre, poblacion, lineas)
        lista_estaciones.append(nueva_estacion)
        # Guardar en JSON dentro de modelos
        archivo_estaciones = os.path.join(ruta_raiz, "modelos", "estaciones.json")
        try:
            guardar_objetos(nueva_estacion.convertir_dicc(), archivo_estaciones)
            print(f"Guardado en: {archivo_estaciones}")
        except Exception as e:
            print(f"Error guardando estación en disco: {e}")
        
        #Confirmar
        label_mensaje.config(
            text=f"✓ Estación '{nombre}' creada exitosamente",
            fg=config.COLOR_VERDE
        )
        ###VER EN CONSOLA!!!
        print(f"\nEstación creada:")
        print(f"  Nombre: {nueva_estacion.nombre}")
        print(f"  Población: {nueva_estacion.poblacion}")
        print(f"  Líneas: {nueva_estacion.lineas}")
        print(f"Total de estaciones: {len(lista_estaciones)}")
        
        #Limpiar
        entry_nombre.delete(0, tk.END)
        entry_poblacion.delete(0, tk.END)
        entry_lineas.delete(0, tk.END)
    
    #Botones
    frame_botones = tk.Frame(ventana_estacion, bg=config.COLOR_GRIS)
    frame_botones.pack(pady=30)
    
    boton_guardar = tk.Button(
        frame_botones,
        text="Guardar Estación",
        command=guardar_estacion,
        font=("Arial", 14, "bold"),
        bg=config.COLOR_VERDE,
        fg=config.COLOR_BLANCO,
        width=18,
        height=2,
        cursor="hand2"
    )
    boton_guardar.pack(side=tk.LEFT, padx=10)
    
    def volver():
        ventana_estacion.destroy()
        ventana_actual.deiconify()
    
    boton_volver = tk.Button(
        frame_botones,
        text="Volver",
        command=volver,
        font=("Arial", 14, "bold"),
        bg=config.COLOR_AZUL,
        fg=config.COLOR_BLANCO,
        width=18,
        height=2,
        cursor="hand2"
    )
    boton_volver.pack(side=tk.LEFT, padx=10)

# ===== VER ESTACIONES =====
def ver_estaciones(ventana_actual):
    """Muestra todas las estaciones creadas."""
    # Refrescar lista desde disco antes de mostrar
    global lista_estaciones
    lista_estaciones = cargar_estaciones_desde_disco()

    ventana_actual.withdraw()
    ventana_lista = tk.Toplevel()
    ventana_lista.title("Lista de Estaciones")
    ventana_lista.geometry("700x600")
    ventana_lista.configure(bg=config.COLOR_GRIS)
    
    # Título
    titulo = tk.Label(
        ventana_lista,
        text="ESTACIONES REGISTRADAS",
        font=("Arial", 24, "bold"),
        bg=config.COLOR_GRIS,
        fg=config.COLOR_BLANCO
    )
    titulo.pack(pady=30)
    
    # Frame con scroll
    frame_scroll = tk.Frame(ventana_lista, bg=config.COLOR_GRIS)
    frame_scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Text widget
    texto = tk.Text(
        frame_scroll,
        font=("Courier", 11),
        bg=config.COLOR_NEGRO,
        fg=config.COLOR_BLANCO,
        wrap=tk.WORD
    )
    texto.pack(fill=tk.BOTH, expand=True)
    
    # Mostrar estaciones (usando datos cargados desde disco si existen)
    if lista_estaciones:
        for i, est in enumerate(lista_estaciones, 1):
            texto.insert(tk.END, f"{i}. {est.nombre}\n")
            texto.insert(tk.END, f"   Población: {est.poblacion:,}\n")
            texto.insert(tk.END, f"   Líneas: {', '.join(est.lineas)}\n\n")
    else:
        texto.insert(tk.END, "No hay estaciones registradas aún.\n")
    
    texto.config(state=tk.DISABLED)
    
    # Botón volver
    def volver():
        ventana_lista.destroy()
        ventana_actual.deiconify()
    
    boton_volver = tk.Button(
        ventana_lista,
        text="Volver",
        command=volver,
        font=("Arial", 14, "bold"),
        bg=config.COLOR_AZUL,
        fg=config.COLOR_BLANCO,
        width=20,
        height=2,
        cursor="hand2"
    )
    boton_volver.pack(pady=20)

def cargar_estaciones_desde_disco():

    archivo_estaciones = os.path.join(ruta_raiz, "modelos", "estaciones.json")
    estaciones = []
    if not os.path.exists(archivo_estaciones):
        return estaciones
    try:
        with open(archivo_estaciones, 'r', encoding='utf-8') as f:
            contenido = json.load(f)
    except Exception as e:
        print(f"Error leyendo archivo de estaciones: {e}")
        return estaciones

    for nombre, datos in contenido.items():
        try:
            poblacion = int(datos.get("poblacion", 0))
            lineas = datos.get("lineas", []) or []
            estaciones.append(estacion(nombre, poblacion, lineas))
        except Exception as e:
            print(f"Omitiendo entrada inválida {nombre}: {e}")
    return estaciones


                             
if __name__ == "__main__":
    ventana_principal()