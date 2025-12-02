import sys
import os
import tkinter as tk    
import tkinter.font as tkfont
import json
import random
from tkinter import messagebox
from PIL import ImageTk, Image
from logic.sistema_eventos.eventos import crear_evento_niebla
###ROOT
ruta_raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)


ruta_imagen = os.path.join(ruta_raiz, "interfaz", "images", "bg.png")

###IMPORTACIONES
from modelos.clases import estacion, guardar_objetos
from interfaz import settings as config
from logic.estado_simulacion import EstadoSimulacion


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
    
 # Muestra de nuevo la ventana principal
    def volver_menu():
        nueva.destroy()
        ventana_actual.deiconify() 

    boton_volver = tk.Button(
        nueva,
        text="Volver al menú principal",
        command=volver_menu,
        font=("Arial", 14),
        bg="white",
        fg="black"
    )
    boton_volver.pack(pady=20)
    
    estado=EstadoSimulacion(semilla=1)
    
    label_reloj = tk.Label(
        nueva,
        text="",
        font=("Arial", 24, "bold"),
        bg="#e8e8e8",
        fg="#0066cc"
    )
    label_reloj.pack(pady=100)
    
    label_eventos = tk.Label(
        nueva,
        text="",
        font=("Arial", 24, "bold"),
        bg="#e8e8e8",
        fg="#cc0000"
        )
    label_eventos.pack(pady=20)
    
    frame_opciones = tk.Frame(nueva, bg="#e8e8e8")
    frame_opciones.pack(pady=20)
    

    
    #funcion para actualizar tiempo, cada 1000ms se llama denuevo a si misma, actualizando el texto
    def actualizar_tiempo():
        hora, fecha = estado.actualizar_display()
        label_reloj.config(text=f"Hora: {hora}   Fecha: {fecha}")
        estado.avanzar_tiempo(segundos=1)
        nueva.after(1000, actualizar_tiempo)
        
    def aplicar_opcion(op):
        resultado = op.efecto(estado)
        label_eventos.config(text=str(resultado))

    #genera un evento al azar cada cierto tiempo         
    def generar_evento():
        evento = crear_evento_niebla(estado)
        
        label_eventos.config(text=f"Evento: {evento.nombre}\n{evento.descripcion}")
        
        for widget in frame_opciones.winfo_children():
            widget.destroy()
        
        boton1 = tk.Button(
            frame_opciones,
            text=evento.opcion1.nombre,
            command=lambda: aplicar_opcion(evento.opcion1),
            font=("Arial", 12),
            bg="white"
        )
        boton1.pack(pady=5)
        # Botón opción 2
        boton2 = tk.Button(
            frame_opciones,
            text=evento.opcion2.nombre,
            command=lambda: aplicar_opcion(evento.opcion2),
            font=("Arial", 12),
            bg="white"
        )
        boton2.pack(pady=5)
    
        tiempo_siguiente = random.randint(5, 15) * 1000  
        nueva.after(tiempo_siguiente, generar_evento) 
              

    
    actualizar_tiempo()
    nueva.after(100,generar_evento)

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


    #Font para botones, escalable
    base_height = config.ALTO_VENTANA if hasattr(config, 'ALTO_VENTANA') else 600
    base_font_size = max(8, int(base_height * 0.016))
    btn_font = tkfont.Font(family="Arial", size=base_font_size)

    #Relative placement para escalar botones
    relw = 0.22
    relh = 0.14

    boton = tk.Button(
        ventana,
        text="INICIAR SIMULACIÓN",
        command=lambda: iniciar_simulacion(ventana), 
        bg=config.COLOR_BLANCO,
        fg=config.COLOR_GRIS,
        font=btn_font,
        cursor="hand2"
    )
    #Colocar en la izquierda abajo
    boton.place(relx=0.2, rely=0.88, anchor="center", relwidth=relw, relheight=relh)

    # Botón para edición de trenes (nuevo)
    boton_trenes = tk.Button(
        ventana,
        text="EDICIÓN TRENES",
        command=lambda: pagina_edicion_trenes(ventana),
        bg=config.COLOR_AZUL,
        fg=config.COLOR_BLANCO,
        font=btn_font,
        cursor="hand2"
    )
    boton_trenes.place(relx=0.5, rely=0.88, anchor="center", relwidth=relw, relheight=relh)

    #Botón de Página de Edición (estaciones)
    boton_pagina = tk.Button(
        ventana,
        text="EDICIÓN ESTACIONES",
        command=lambda: pagina_edicion(ventana),
        bg=config.COLOR_AZUL,
        fg=config.COLOR_BLANCO,
        font=btn_font,
        cursor="hand2"
    )
    boton_pagina.place(relx=0.8, rely=0.88, anchor="center", relwidth=relw, relheight=relh)

    #Escalar fuente al redimensionar ventana
    def on_resize(event):
        # compute font size proportional to height
        new_size = max(8, int(event.height * 0.016))
        btn_font.configure(size=new_size)

    ventana.bind('<Configure>', on_resize)
    ventana.mainloop()

def pagina_edicion(ventana_actual):
    #Muestra la página de edición con botones para editar y ver estaciones
    ventana_actual.withdraw()
    pagina = tk.Toplevel()
    pagina.title("Página de Edición")
    pagina.geometry("640x360")
    pagina.configure(bg=config.COLOR_GRIS)

    titulo = tk.Label(
        pagina,
        text="Página de Edición",
        font=("Arial", 18, "bold"),
        bg=config.COLOR_GRIS,
        fg=config.COLOR_BLANCO
    )
    titulo.pack(pady=12)

    frame = tk.Frame(pagina, bg=config.COLOR_GRIS)
    frame.pack(expand=True)

    btn_editar = tk.Button(
        frame,
        text="Editar Estación",
        command=lambda: abrir_editor_estacion(pagina),
        bg=config.COLOR_AZUL,
        fg=config.COLOR_BLANCO,
        font=("Arial", 12),
        cursor="hand2",
        padx=12,
        pady=8
    )
    btn_editar.pack(side=tk.LEFT, padx=20)

    btn_ver = tk.Button(
        frame,
        text="Ver Estación",
        command=lambda: ver_estaciones(pagina),
        bg=config.COLOR_VERDE,
        fg=config.COLOR_BLANCO,
        font=("Arial", 12),
        cursor="hand2",
        padx=12,
        pady=8
    )
    btn_ver.pack(side=tk.LEFT, padx=20)

    btn_crear = tk.Button(
        frame,
        text="Crear Estación",
        command=lambda: crear_estacion(pagina),
        bg=config.COLOR_VERDE,
        fg=config.COLOR_BLANCO,
        font=("Arial", 12),
        cursor="hand2",
        padx=12,
        pady=8
    )
    btn_crear.pack(side=tk.LEFT, padx=20)

    # --- Selección y borrado de estaciones directamente en la Página de Edición ---
    control_frame = tk.Frame(pagina, bg=config.COLOR_GRIS)
    control_frame.pack(pady=12)

    tk.Label(control_frame, text="Seleccionar estación:", bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO).pack(side=tk.LEFT, padx=(0,8))

    archivo_estaciones = os.path.join(ruta_raiz, "modelos", "estaciones.json")

    def leer_dicc():
        if not os.path.exists(archivo_estaciones):
            return {}
        try:
            with open(archivo_estaciones, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error leyendo estaciones: {e}")
            return {}

    nombres_var = tk.StringVar(pagina)

    def refrescar_nombres():
        datos = leer_dicc()
        nombres = sorted(datos.keys())
        menu = option['menu']
        menu.delete(0, 'end')
        for n in nombres:
            menu.add_command(label=n, command=lambda value=n: nombres_var.set(value))
        if nombres:
            nombres_var.set(nombres[0])
        else:
            nombres_var.set("")

    option = tk.OptionMenu(control_frame, nombres_var, "")
    option.config(bg=config.COLOR_BLANCO, fg=config.COLOR_NEGRO)
    option.pack(side=tk.LEFT, padx=(0,8))

    msg_del = tk.Label(pagina, text="", bg=config.COLOR_GRIS)
    msg_del.pack()

    def borrar_seleccion():
        nombre = nombres_var.get()
        if not nombre:
            msg_del.config(text="No hay estación seleccionada", fg=config.COLOR_ROJO)
            return
        if not messagebox.askyesno("Confirmar borrado", f"¿Eliminar la estación '{nombre}'?"):
            return
        datos = leer_dicc()
        if nombre in datos:
            datos.pop(nombre, None)
            try:
                with open(archivo_estaciones, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, indent=4, ensure_ascii=False)
                msg_del.config(text=f"Estación '{nombre}' eliminada.", fg=config.COLOR_VERDE)
                refrescar_nombres()
            except Exception as e:
                msg_del.config(text=f"Error borrando: {e}", fg=config.COLOR_ROJO)
        else:
            msg_del.config(text="Estación no encontrada", fg=config.COLOR_ROJO)

    btn_borrar = tk.Button(control_frame, text="Borrar estación", command=borrar_seleccion, bg=config.COLOR_ROJO, fg=config.COLOR_BLANCO, cursor="hand2")
    btn_borrar.pack(side=tk.LEFT, padx=8)

    #Inicializar lista de nombres
    refrescar_nombres()

    # Cuando la ventana reciba foco (por ejemplo tras cerrar crear_estacion), refrescar la lista
    pagina.bind('<FocusIn>', lambda e: refrescar_nombres())

    def volver():
        pagina.destroy()
        ventana_actual.deiconify()

    btn_volver = tk.Button(
        pagina,
        text="Volver",
        command=volver,
        bg=config.COLOR_AZUL,
        fg=config.COLOR_BLANCO,
        font=("Arial", 12),
        cursor="hand2",
        padx=8,
        pady=6
    )
    btn_volver.pack(pady=12)

def abrir_editor_estacion(parent):
   #Abre un editor que permite seleccionar, editar y borrar estaciones desde el JSON
    archivo_estaciones = os.path.join(ruta_raiz, "modelos", "estaciones.json")

    def leer_dict():
        if not os.path.exists(archivo_estaciones):
            return {}
        try:
            with open(archivo_estaciones, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error leyendo estaciones: {e}")
            return {}

    data = leer_dict()

    editor = tk.Toplevel()
    editor.title("Editar Estación")
    editor.geometry("800x420")
    editor.configure(bg=config.COLOR_GRIS)

    left = tk.Frame(editor, bg=config.COLOR_GRIS)
    left.pack(side=tk.LEFT, fill=tk.Y, padx=12, pady=12)

    lb_label = tk.Label(left, text="Estaciones:", bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO)
    lb_label.pack(anchor="w")

    listbox = tk.Listbox(left, width=30, height=20)
    listbox.pack(side=tk.LEFT, fill=tk.Y)

    scrollbar = tk.Scrollbar(left, orient=tk.VERTICAL, command=listbox.yview)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)

    nombres = sorted(data.keys())
    for n in nombres:
        listbox.insert(tk.END, n)

    #Panel de edición a la derecha
    right = tk.Frame(editor, bg=config.COLOR_GRIS)
    right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12, pady=12)

    tk.Label(right, text="Nombre:", bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO).grid(row=0, column=0, sticky="w")
    e_nombre = tk.Entry(right, width=40)
    e_nombre.grid(row=0, column=1, pady=6, sticky="w")

    tk.Label(right, text="Población:", bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO).grid(row=1, column=0, sticky="w")
    e_pobl = tk.Entry(right, width=20)
    e_pobl.grid(row=1, column=1, pady=6, sticky="w")

    tk.Label(right, text="Líneas (coma):", bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO).grid(row=2, column=0, sticky="w")
    e_lineas = tk.Entry(right, width=40)
    e_lineas.grid(row=2, column=1, pady=6, sticky="w")

    msg = tk.Label(right, text="", bg=config.COLOR_GRIS, fg=config.COLOR_VERDE)
    msg.grid(row=3, column=0, columnspan=2, pady=6, sticky="w")

    nombre_seleccionado = {'old': None}

    def en_seleccion(evt):
        sel = listbox.curselection()
        if not sel:
            return
        nombre = listbox.get(sel[0])
        nombre_seleccionado['old'] = nombre
        entry = data.get(nombre, {})
        e_nombre.delete(0, tk.END)
        e_nombre.insert(0, entry.get('nombre', nombre))
        e_pobl.delete(0, tk.END)
        e_pobl.insert(0, str(entry.get('poblacion', '')))
        lineas_val = ', '.join(entry.get('lineas', [])) if entry.get('lineas') else ''
        e_lineas.delete(0, tk.END)
        e_lineas.insert(0, lineas_val)

    listbox.bind('<<ListboxSelect>>', en_seleccion)

    def guardar():
        old = nombre_seleccionado.get('old')
        if not old:
            msg.config(text="Seleccione una estación primero", fg=config.COLOR_ROJO)
            return
        new_name = e_nombre.get().strip()
        pobl_str = e_pobl.get().strip()
        lineas_str = e_lineas.get().strip()
        if not new_name:
            msg.config(text="El nombre no puede estar vacío", fg=config.COLOR_ROJO)
            return
        if not pobl_str.isdigit():
            msg.config(text="Población debe ser número", fg=config.COLOR_ROJO)
            return
        pobl = int(pobl_str)
        lineas = [l.strip() for l in lineas_str.split(',') if l.strip()]

        #Revisar si el nuevo nombre ya existe (y no es el mismo que el antiguo)
        data_local = leer_dict()
        #Remover antiguo si cambia nombre
        if old != new_name and old in data_local:
            data_local.pop(old, None)
        data_local[new_name] = {"nombre": new_name, "poblacion": pobl, "lineas": lineas}

        try:
            with open(archivo_estaciones, 'w', encoding='utf-8') as f:
                json.dump(data_local, f, indent=4, ensure_ascii=False)
            msg.config(text="Guardado correctamente", fg=config.COLOR_VERDE)
            #Refrescar lista
            listbox.delete(0, tk.END)
            for n in sorted(data_local.keys()):
                listbox.insert(tk.END, n)
            nombre_seleccionado['old'] = new_name
        except Exception as e:
            msg.config(text=f"Error guardando: {e}", fg=config.COLOR_ROJO)

    def borrar():
        old = nombre_seleccionado.get('old')
        if not old:
            msg.config(text="Seleccione una estación primero", fg=config.COLOR_ROJO)
            return
        data_local = leer_dict()
        if old in data_local:
            data_local.pop(old, None)
            try:
                with open(archivo_estaciones, 'w', encoding='utf-8') as f:
                    json.dump(data_local, f, indent=4, ensure_ascii=False)
                msg.config(text="Estación eliminada", fg=config.COLOR_VERDE)
                listbox.delete(0, tk.END)
                for n in sorted(data_local.keys()):
                    listbox.insert(tk.END, n)
                e_nombre.delete(0, tk.END)
                e_pobl.delete(0, tk.END)
                e_lineas.delete(0, tk.END)
                nombre_seleccionado['old'] = None
            except Exception as e:
                msg.config(text=f"Error borrando: {e}", fg=config.COLOR_ROJO)
        else:
            msg.config(text="Estación no encontrada", fg=config.COLOR_ROJO)

    btn_frame = tk.Frame(right, bg=config.COLOR_GRIS)
    btn_frame.grid(row=4, column=0, columnspan=2, pady=12, sticky="w")

    btn_save = tk.Button(btn_frame, text="Guardar cambios", command=guardar, bg=config.COLOR_VERDE, fg=config.COLOR_BLANCO, cursor="hand2")
    btn_save.pack(side=tk.LEFT, padx=8)

    btn_del = tk.Button(btn_frame, text="Borrar estación", command=borrar, bg=config.COLOR_ROJO, fg=config.COLOR_BLANCO, cursor="hand2")
    btn_del.pack(side=tk.LEFT, padx=8)

    def cerrar():
        editor.destroy()

    btn_close = tk.Button(right, text="Cerrar", command=cerrar, bg=config.COLOR_AZUL, fg=config.COLOR_BLANCO, cursor="hand2")
    btn_close.grid(row=5, column=0, columnspan=2, pady=10)


def pagina_edicion_trenes(ventana_actual):
    # Muestra la página de edición para trenes
    ventana_actual.withdraw()
    pagina = tk.Toplevel()
    pagina.title("Página de Edición - Trenes")
    pagina.geometry("640x360")
    pagina.configure(bg=config.COLOR_GRIS)

    titulo = tk.Label(
        pagina,
        text="Edición de Trenes",
        font=("Arial", 18, "bold"),
        bg=config.COLOR_GRIS,
        fg=config.COLOR_BLANCO
    )
    titulo.pack(pady=12)

    frame = tk.Frame(pagina, bg=config.COLOR_GRIS)
    frame.pack(expand=True)

    btn_editar = tk.Button(
        frame,
        text="Editar Tren",
        command=lambda: abrir_editor_tren(pagina),
        bg=config.COLOR_AZUL,
        fg=config.COLOR_BLANCO,
        font=("Arial", 12),
        cursor="hand2",
        padx=12,
        pady=8
    )
    btn_editar.pack(side=tk.LEFT, padx=20)

    btn_ver = tk.Button(
        frame,
        text="Ver Trenes",
        command=lambda: ver_trenes(pagina),
        bg=config.COLOR_VERDE,
        fg=config.COLOR_BLANCO,
        font=("Arial", 12),
        cursor="hand2",
        padx=12,
        pady=8
    )
    btn_ver.pack(side=tk.LEFT, padx=20)

    btn_crear = tk.Button(
        frame,
        text="Crear Tren",
        command=lambda: crear_tren(pagina),
        bg=config.COLOR_VERDE,
        fg=config.COLOR_BLANCO,
        font=("Arial", 12),
        cursor="hand2",
        padx=12,
        pady=8
    )
    btn_crear.pack(side=tk.LEFT, padx=20)

    def volver():
        pagina.destroy()
        ventana_actual.deiconify()

    btn_volver = tk.Button(
        pagina,
        text="Volver",
        command=volver,
        bg=config.COLOR_AZUL,
        fg=config.COLOR_BLANCO,
        font=("Arial", 12),
        cursor="hand2",
        padx=8,
        pady=6
    )
    btn_volver.pack(pady=12)


def cargar_trenes_desde_disco():
    archivo_trenes = os.path.join(ruta_raiz, "modelos", "trenes.json")
    if not os.path.exists(archivo_trenes):
        return []
    try:
        with open(archivo_trenes, 'r', encoding='utf-8') as f:
            contenido = json.load(f)
    except Exception as e:
        print(f"Error leyendo archivo de trenes: {e}")
        return []
    trenes = []
    for nombre, datos in contenido.items():
        try:
            velocidad = int(datos.get('velocidad', 0))
            ppv = int(datos.get('ppv', 0))
            ccv = int(datos.get('ccv', 0))
            trenes.append((nombre, velocidad, ppv, ccv))
        except Exception as e:
            print(f"Omitiendo entrada inválida {nombre}: {e}")
    return trenes


def ver_trenes(ventana_actual):
    ventana_actual.withdraw()
    ventana_lista = tk.Toplevel()
    ventana_lista.title("Lista de Trenes")
    ventana_lista.geometry("700x600")
    ventana_lista.configure(bg=config.COLOR_GRIS)

    titulo = tk.Label(
        ventana_lista,
        text="TRENES REGISTRADOS",
        font=("Arial", 24, "bold"),
        bg=config.COLOR_GRIS,
        fg=config.COLOR_BLANCO
    )
    titulo.pack(pady=30)

    frame_scroll = tk.Frame(ventana_lista, bg=config.COLOR_GRIS)
    frame_scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    texto = tk.Text(
        frame_scroll,
        font=("Courier", 11),
        bg=config.COLOR_NEGRO,
        fg=config.COLOR_BLANCO,
        wrap=tk.WORD
    )
    texto.pack(fill=tk.BOTH, expand=True)

    trenes = cargar_trenes_desde_disco()
    if trenes:
        for i, (nombre, velocidad, ppv, ccv) in enumerate(trenes, 1):
            texto.insert(tk.END, f"{i}. {nombre}\n")
            texto.insert(tk.END, f"   Velocidad: {velocidad}\n")
            texto.insert(tk.END, f"   Pasajeros/vagón: {ppv}\n")
            texto.insert(tk.END, f"   Cantidad vagones: {ccv}\n\n")
    else:
        texto.insert(tk.END, "No hay trenes registrados aún.\n")

    texto.config(state=tk.DISABLED)

    def volver():
        ventana_lista.destroy()
        ventana_actual.deiconify()

    boton_volver = tk.Button(
        ventana_lista,
        text="Volver",
        command=volver,
        bg=config.COLOR_AZUL,
        fg=config.COLOR_BLANCO,
        cursor="hand2"
    )
    boton_volver.pack(pady=20)


def abrir_editor_tren(parent):
    archivo_trenes = os.path.join(ruta_raiz, "modelos", "trenes.json")

    def leer_dict():
        if not os.path.exists(archivo_trenes):
            return {}
        try:
            with open(archivo_trenes, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error leyendo trenes: {e}")
            return {}

    data = leer_dict()

    editor = tk.Toplevel()
    editor.title("Editar Tren")
    editor.geometry("800x420")
    editor.configure(bg=config.COLOR_GRIS)

    left = tk.Frame(editor, bg=config.COLOR_GRIS)
    left.pack(side=tk.LEFT, fill=tk.Y, padx=12, pady=12)

    lb_label = tk.Label(left, text="Trenes:", bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO)
    lb_label.pack(anchor="w")

    listbox = tk.Listbox(left, width=30, height=20)
    listbox.pack(side=tk.LEFT, fill=tk.Y)

    scrollbar = tk.Scrollbar(left, orient=tk.VERTICAL, command=listbox.yview)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)

    nombres = sorted(data.keys())
    for n in nombres:
        listbox.insert(tk.END, n)

    right = tk.Frame(editor, bg=config.COLOR_GRIS)
    right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12, pady=12)

    tk.Label(right, text="Nombre:", bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO).grid(row=0, column=0, sticky="w")
    e_nombre = tk.Entry(right, width=40)
    e_nombre.grid(row=0, column=1, pady=6, sticky="w")

    tk.Label(right, text="Velocidad:", bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO).grid(row=1, column=0, sticky="w")
    e_vel = tk.Entry(right, width=20)
    e_vel.grid(row=1, column=1, pady=6, sticky="w")

    tk.Label(right, text="Pasajeros por vagón:", bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO).grid(row=2, column=0, sticky="w")
    e_ppv = tk.Entry(right, width=20)
    e_ppv.grid(row=2, column=1, pady=6, sticky="w")

    tk.Label(right, text="Cantidad vagones:", bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO).grid(row=3, column=0, sticky="w")
    e_ccv = tk.Entry(right, width=20)
    e_ccv.grid(row=3, column=1, pady=6, sticky="w")

    msg = tk.Label(right, text="", bg=config.COLOR_GRIS, fg=config.COLOR_VERDE)
    msg.grid(row=4, column=0, columnspan=2, pady=6, sticky="w")

    selected = {'old': None}

    def on_select(evt):
        sel = listbox.curselection()
        if not sel:
            return
        name = listbox.get(sel[0])
        selected['old'] = name
        entry = data.get(name, {})
        e_nombre.delete(0, tk.END)
        e_nombre.insert(0, entry.get('nombre', name))
        e_vel.delete(0, tk.END)
        e_vel.insert(0, str(entry.get('velocidad', '')))
        e_ppv.delete(0, tk.END)
        e_ppv.insert(0, str(entry.get('ppv', '')))
        e_ccv.delete(0, tk.END)
        e_ccv.insert(0, str(entry.get('ccv', '')))

    listbox.bind('<<ListboxSelect>>', on_select)

    def guardar():
        old = selected.get('old')
        if not old:
            msg.config(text="Seleccione un tren primero", fg=config.COLOR_ROJO)
            return
        new_name = e_nombre.get().strip()
        vel_str = e_vel.get().strip()
        ppv_str = e_ppv.get().strip()
        ccv_str = e_ccv.get().strip()
        if not new_name:
            msg.config(text="El nombre no puede estar vacío", fg=config.COLOR_ROJO)
            return
        if not (vel_str.isdigit() and ppv_str.isdigit() and ccv_str.isdigit()):
            msg.config(text="Velocidad/ppv/ccv deben ser números", fg=config.COLOR_ROJO)
            return
        vel = int(vel_str)
        ppv = int(ppv_str)
        ccv = int(ccv_str)

        data_local = leer_dict()
        if old != new_name and old in data_local:
            data_local.pop(old, None)
        data_local[new_name] = {"nombre": new_name, "velocidad": vel, "ppv": ppv, "ccv": ccv}
        try:
            with open(archivo_trenes, 'w', encoding='utf-8') as f:
                json.dump(data_local, f, indent=4, ensure_ascii=False)
            msg.config(text="Guardado correctamente", fg=config.COLOR_VERDE)
            listbox.delete(0, tk.END)
            for n in sorted(data_local.keys()):
                listbox.insert(tk.END, n)
            selected['old'] = new_name
        except Exception as e:
            msg.config(text=f"Error guardando: {e}", fg=config.COLOR_ROJO)

    def borrar():
        old = selected.get('old')
        if not old:
            msg.config(text="Seleccione un tren primero", fg=config.COLOR_ROJO)
            return
        data_local = leer_dict()
        if old in data_local:
            data_local.pop(old, None)
            try:
                with open(archivo_trenes, 'w', encoding='utf-8') as f:
                    json.dump(data_local, f, indent=4, ensure_ascii=False)
                msg.config(text="Tren eliminado", fg=config.COLOR_VERDE)
                listbox.delete(0, tk.END)
                for n in sorted(data_local.keys()):
                    listbox.insert(tk.END, n)
                e_nombre.delete(0, tk.END)
                e_vel.delete(0, tk.END)
                e_ppv.delete(0, tk.END)
                e_ccv.delete(0, tk.END)
                selected['old'] = None
            except Exception as e:
                msg.config(text=f"Error borrando: {e}", fg=config.COLOR_ROJO)
        else:
            msg.config(text="Tren no encontrado", fg=config.COLOR_ROJO)

    btn_frame = tk.Frame(right, bg=config.COLOR_GRIS)
    btn_frame.grid(row=5, column=0, columnspan=2, pady=12, sticky="w")

    btn_save = tk.Button(btn_frame, text="Guardar cambios", command=guardar, bg=config.COLOR_VERDE, fg=config.COLOR_BLANCO, cursor="hand2")
    btn_save.pack(side=tk.LEFT, padx=8)

    btn_del = tk.Button(btn_frame, text="Borrar tren", command=borrar, bg=config.COLOR_ROJO, fg=config.COLOR_BLANCO, cursor="hand2")
    btn_del.pack(side=tk.LEFT, padx=8)

    def cerrar():
        editor.destroy()

    btn_close = tk.Button(right, text="SCerrar", command=cerrar, bg=config.COLOR_AZUL, fg=config.COLOR_BLANCO, cursor="hand2")
    btn_close.grid(row=6, column=0, columnspan=2, pady=10)


def crear_tren(ventana_actual):
    """Abre ventana para crear un nuevo tren y lo guarda en modelos/trenes.json"""
    ventana_actual.withdraw()
    crear = tk.Toplevel()
    crear.title("Crear Tren")
    crear.geometry("520x320")
    crear.configure(bg=config.COLOR_GRIS)

    titulo = tk.Label(crear, text="CREAR TREN", font=("Arial", 18, "bold"), bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO)
    titulo.pack(pady=12)

    frame = tk.Frame(crear, bg=config.COLOR_GRIS)
    frame.pack(pady=8)

    tk.Label(frame, text="Nombre:", bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO).grid(row=0, column=0, sticky="w", padx=8, pady=6)
    e_nombre = tk.Entry(frame, width=30)
    e_nombre.grid(row=0, column=1, pady=6)

    tk.Label(frame, text="Velocidad:", bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO).grid(row=1, column=0, sticky="w", padx=8, pady=6)
    e_vel = tk.Entry(frame, width=20)
    e_vel.grid(row=1, column=1, pady=6)

    tk.Label(frame, text="Pasajeros/vagón:", bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO).grid(row=2, column=0, sticky="w", padx=8, pady=6)
    e_ppv = tk.Entry(frame, width=20)
    e_ppv.grid(row=2, column=1, pady=6)

    tk.Label(frame, text="Cantidad vagones:", bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO).grid(row=3, column=0, sticky="w", padx=8, pady=6)
    e_ccv = tk.Entry(frame, width=20)
    e_ccv.grid(row=3, column=1, pady=6)

    label_msg = tk.Label(crear, text="", bg=config.COLOR_GRIS)
    label_msg.pack(pady=6)

    def guardar_nuevo():
        nombre = e_nombre.get().strip()
        vel = e_vel.get().strip()
        ppv = e_ppv.get().strip()
        ccv = e_ccv.get().strip()
        if not nombre:
            label_msg.config(text="El nombre es obligatorio", fg=config.COLOR_ROJO)
            return
        if not (vel.isdigit() and ppv.isdigit() and ccv.isdigit()):
            label_msg.config(text="Velocidad/ppv/ccv deben ser números", fg=config.COLOR_ROJO)
            return
        datos = {"nombre": nombre, "velocidad": int(vel), "ppv": int(ppv), "ccv": int(ccv)}
        archivo_trenes = os.path.join(ruta_raiz, "modelos", "trenes.json")
        try:
            guardar_objetos(datos, archivo_trenes)
            label_msg.config(text=f"Tren '{nombre}' guardado.", fg=config.COLOR_VERDE)
        except Exception as e:
            label_msg.config(text=f"Error guardando: {e}", fg=config.COLOR_ROJO)

        #delay para ver mensaje
        e_nombre.delete(0, tk.END)
        e_vel.delete(0, tk.END)
        e_ppv.delete(0, tk.END)
        e_ccv.delete(0, tk.END)

    def volver():
        crear.destroy()
        ventana_actual.deiconify()

    btn_frame = tk.Frame(crear, bg=config.COLOR_GRIS)
    btn_frame.pack(pady=10)

    btn_guardar = tk.Button(btn_frame, text="Guardar Tren", command=guardar_nuevo, bg=config.COLOR_VERDE, fg=config.COLOR_BLANCO, cursor="hand2")
    btn_guardar.pack(side=tk.LEFT, padx=8)

    btn_volver = tk.Button(btn_frame, text="Volver", command=volver, bg=config.COLOR_AZUL, fg=config.COLOR_BLANCO, cursor="hand2")
    btn_volver.pack(side=tk.LEFT, padx=8)

def crear_estacion(ventana_actual):
    #Abre ventana nueva estación
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
    
    #Widget de texto con scrollbar
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
        bg=config.COLOR_AZUL,
        fg=config.COLOR_BLANCO,
        cursor="hand2",
        relief="raised",
        bd=6,
        highlightthickness=0,
        activebackground=config.COLOR_AZUL
    )
    #Font dedicada para botón volver, escalable
    back_btn_font = tkfont.Font(family="Arial", size=14, weight="bold")
    boton_volver.config(font=back_btn_font)

    #Reajustar tamaño fuente al redimensionar ventana
    def on_lista_resize(event):
        #Font proporcional a altura
        new_size = max(10, int(event.height * 0.03))
        back_btn_font.configure(size=new_size)

    boton_volver.pack(pady=20, ipadx=16, ipady=10)
    ventana_lista.bind('<Configure>', on_lista_resize)

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