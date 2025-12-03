# window.py solamente contiene la ventana principal. Las otras ventanas
# se encuentran en archivos separados dentro de la carpeta ventanas. Se modularizó
# de esta forma para mejorar la legibilidad y facilitar el mantenimiento.
import sys
import os
import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox
from PIL import Image, ImageTk

# Asegura que window.py este en el path para que
# (python interfaz\ventanas\window.py) pueda ejecutarse sin errores
ruta_raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

from interfaz.ventanas.common import ruta_imagen
from interfaz.ventanas.ventana_simulacion import iniciar_simulacion
from interfaz.ventanas.pages import _pagina_edicion_impl, pagina_edicion_trenes
from interfaz import settings as config
from modelos.clases import cargar_objetos, tren, estacion

##################################################################################




def ventana_principal():
    ventana = tk.Tk()
    ventana.title("Simulador para operarios")
    ventana.state('zoomed')  # Fullscreen on Windows
    ventana.configure(bg=config.COLOR_GRIS)

    # --- Main menu background (bg.png) ---
    canvas = tk.Canvas(ventana, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    try:
        bg_normal = Image.open(ruta_imagen)
    except Exception:
        bg_normal = None

    def redibujar_fondo(event):
        if bg_normal:
            nueva_img = bg_normal.resize((event.width, event.height), Image.LANCZOS)
            imagen_fondo = ImageTk.PhotoImage(nueva_img)
            canvas.image = imagen_fondo
            canvas.delete("all")
            canvas.create_image(0, 0, anchor="nw", image=imagen_fondo)

    #Fondo inicial
    if bg_normal:
        w = ventana.winfo_screenwidth()
        h = ventana.winfo_screenheight()
        bg_res = bg_normal.resize((w, h), Image.LANCZOS)
        imagen_fondo = ImageTk.PhotoImage(bg_res)
        canvas.create_image(0, 0, anchor="nw", image=imagen_fondo)
        canvas.image = imagen_fondo
        canvas.bind("<Configure>", redibujar_fondo)

    base_height = ventana.winfo_screenheight()
    base_font_size = max(8, int(base_height * config.BASE_FONT_MULTIPLIER))
    btn_font = tkfont.Font(family="Arial", size=base_font_size)

    #Boton salir
    def salir():
        ventana.quit()
    
    boton_exit = tk.Button(
        ventana,
        text="SALIR",
        command=salir,
        bg=config.COLOR_ROJO,
        fg=config.COLOR_BLANCO,
        font=btn_font,
        cursor="hand2",
    )
    boton_exit.place(relx=config.EXIT_BUTTON_RELX, rely=config.EXIT_BUTTON_RELY, anchor="ne", relwidth=config.EXIT_BUTTON_RELWIDTH, relheight=config.EXIT_BUTTON_RELHEIGHT)

    #Pantalla para los seeds
    menu_semilla = tk.Frame(ventana, bg=config.COLOR_BLANCO, relief=tk.RAISED, bd=3)
    menu_semilla.place(relx=config.MENU_FRAME_RELX, rely=config.MENU_FRAME_RELY, anchor="center", relwidth=config.MENU_FRAME_RELWIDTH, relheight=config.MENU_FRAME_RELHEIGHT)

    label_semilla = tk.Label(menu_semilla, text="Semilla (0-10000):", bg=config.COLOR_BLANCO, fg=config.COLOR_GRIS, font=btn_font)
    label_semilla.pack(pady=(8, 4))

    entrada_semilla = tk.Entry(menu_semilla, font=btn_font, bg="white", fg="black")
    entrada_semilla.pack(pady=(4, 8), padx=12, fill=tk.BOTH, expand=True)

    def seleccionar_modo_inicio(parent, entrada_semilla):
        """Open a modal asking the user to choose default or custom data files for the run."""
        dlg = tk.Toplevel(parent)
        dlg.title("Modo de inicio")
        dlg.geometry("420x160")
        dlg.transient(parent)
        dlg.configure(bg=config.COLOR_BLANCO)
        dlg.grab_set()

        lbl = tk.Label(dlg, text="Seleccione modo de inicio:", font=("Arial", 12, "bold"), bg=config.COLOR_BLANCO)
        lbl.pack(pady=(16,8))

        frame = tk.Frame(dlg, bg=config.COLOR_BLANCO)
        frame.pack(pady=8)

        def mostrar_confirmacion(ruta_tr, ruta_es):
            dlg.destroy()
            
            try:
                lista_trenes = cargar_objetos(ruta_tr, tren)
                lista_estaciones = cargar_objetos(ruta_es, estacion)
            except Exception as e:
                messagebox.showerror("Error", f"Error cargando archivos:\n{e}")
                return

            conf = tk.Toplevel(parent)
            conf.title("Confirmar Inicio")
            conf.state('zoomed')
            conf.configure(bg=config.COLOR_GRIS)

            tk.Label(conf, text="Confirmar datos de simulación", font=("Arial", 20, "bold"), bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO).pack(pady=20)

            lists_frame = tk.Frame(conf, bg=config.COLOR_GRIS)
            lists_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            frame_trenes = tk.Frame(lists_frame, bg=config.COLOR_GRIS)
            frame_trenes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
            tk.Label(frame_trenes, text="Trenes a cargar:", font=("Arial", 14, "bold"), bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO).pack(anchor="w")
            
            listbox_trenes = tk.Listbox(frame_trenes, font=("Courier", 10))
            listbox_trenes.pack(fill=tk.BOTH, expand=True, pady=5)
            for t in lista_trenes:
                listbox_trenes.insert(tk.END, f"{t.nombre} (Vel: {t.velocidad_max}, Cap: {t.capacidad()})")

            frame_estaciones = tk.Frame(lists_frame, bg=config.COLOR_GRIS)
            frame_estaciones.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
            tk.Label(frame_estaciones, text="Estaciones a cargar:", font=("Arial", 14, "bold"), bg=config.COLOR_GRIS, fg=config.COLOR_BLANCO).pack(anchor="w")
            
            listbox_estaciones = tk.Listbox(frame_estaciones, font=("Courier", 10))
            listbox_estaciones.pack(fill=tk.BOTH, expand=True, pady=5)
            for e in lista_estaciones:
                listbox_estaciones.insert(tk.END, f"{e.nombre} (Pobl: {e.poblacion})")

            btn_frame = tk.Frame(conf, bg=config.COLOR_GRIS)
            btn_frame.pack(pady=20)

            def confirmar():
                conf.destroy()
                iniciar_simulacion(parent, entrada_semilla, ruta_trenes=ruta_tr, ruta_estaciones=ruta_es)

            def cancelar():
                conf.destroy()

            tk.Button(btn_frame, text="CONFIRMAR E INICIAR", command=confirmar, bg=config.COLOR_VERDE, fg=config.COLOR_BLANCO, font=("Arial", 14, "bold"), padx=20, pady=10).pack(side=tk.LEFT, padx=20)
            tk.Button(btn_frame, text="CANCELAR", command=cancelar, bg=config.COLOR_ROJO, fg=config.COLOR_BLANCO, font=("Arial", 14, "bold"), padx=20, pady=10).pack(side=tk.LEFT, padx=20)

        def inicio_default():
            ruta_tr = os.path.join(ruta_raiz, "modelos", "trenes_default.json")
            ruta_es = os.path.join(ruta_raiz, "modelos", "estaciones_default.json")
            mostrar_confirmacion(ruta_tr, ruta_es)

        def inicio_personalizado():
            ruta_tr = os.path.join(ruta_raiz, "modelos", "trenes.json")
            ruta_es = os.path.join(ruta_raiz, "modelos", "estaciones.json")
            mostrar_confirmacion(ruta_tr, ruta_es)

        btn_default = tk.Button(frame, text="Inicio por defecto", command=inicio_default, bg=config.COLOR_AZUL, fg=config.COLOR_BLANCO, width=16, cursor="hand2")
        btn_default.pack(side=tk.LEFT, padx=12)

        btn_personal = tk.Button(frame, text="Inicio personalizado", command=inicio_personalizado, bg=config.COLOR_VERDE, fg=config.COLOR_BLANCO, width=16, cursor="hand2")
        btn_personal.pack(side=tk.LEFT, padx=12)

    boton = tk.Button(
        ventana,
        text="INICIAR SIMULACIÓN",
        command=lambda: seleccionar_modo_inicio(ventana, entrada_semilla),
        bg=config.COLOR_BLANCO,
        fg=config.COLOR_GRIS,
        font=btn_font,
        cursor="hand2",
    )
    boton.place(relx=config.BUTTON_SIMULACION_POS[0], rely=config.BUTTON_SIMULACION_POS[1], anchor="center", relwidth=config.BUTTON_RELWIDTH, relheight=config.BUTTON_RELHEIGHT)

    boton_trenes = tk.Button(
        ventana,
        text="EDICIÓN TRENES",
        command=lambda: pagina_edicion_trenes(ventana),
        bg=config.COLOR_AZUL,
        fg=config.COLOR_BLANCO,
        font=btn_font,
        cursor="hand2",
    )
    boton_trenes.place(relx=config.BUTTON_TRENES_POS[0], rely=config.BUTTON_TRENES_POS[1], anchor="center", relwidth=config.BUTTON_RELWIDTH, relheight=config.BUTTON_RELHEIGHT)

    boton_pagina = tk.Button(
        ventana,
        text="EDICIÓN ESTACIONES",
        command=lambda: _pagina_edicion_impl(ventana),
        bg=config.COLOR_VERDE,
        fg=config.COLOR_BLANCO,
        font=btn_font,
        cursor="hand2",
    )
    boton_pagina.place(relx=config.BUTTON_ESTACIONES_POS[0], rely=config.BUTTON_ESTACIONES_POS[1], anchor="center", relwidth=config.BUTTON_RELWIDTH, relheight=config.BUTTON_RELHEIGHT)

    # Boton configuracion generador
    from interfaz.ventanas.ventana_config_gen import ventana_configuracion_generador
    boton_gen = tk.Button(
        ventana,
        text="CONFIGURAR GENERADOR",
        command=lambda: ventana_configuracion_generador(ventana),
        bg=config.COLOR_ROJO,
        fg=config.COLOR_BLANCO,
        font=btn_font,
        cursor="hand2",
    )
    # Place it below the other buttons, or adjust layout. 
    # Current buttons are at RELY 0.5, 0.6, 0.7 (approx based on config).
    # I'll check config values or just place it manually for now.
    # Assuming config has positions, I'll place it slightly lower.
    boton_gen.place(relx=0.8, rely=0.75, anchor="center", relwidth=0.10, relheight=0.10)

    def on_resize(event):
        new_size = max(8, int(event.height * 0.016))
        btn_font.configure(size=new_size)

    ventana.bind('<Configure>', on_resize)
    ventana.mainloop()
if __name__ == "__main__":
    ventana_principal()