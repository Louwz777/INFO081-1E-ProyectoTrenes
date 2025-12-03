# window.py keeps only the main window entrypoint. All other UI functions
# have been moved to `pages.py`. Shared paths are in `common.py`.
import sys
import os
import tkinter as tk
import tkinter.font as tkfont
from PIL import ImageTk, Image

# Ensure project root is on sys.path so running this file directly
# (python interfaz\ventanas\window.py) can import sibling packages.
ruta_raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

from interfaz.ventanas.ventana_simulacion import iniciar_simulacion
from interfaz.ventanas.common import ruta_imagen
from interfaz.ventanas.pages import (
    pagina_edicion,
    abrir_editor_estacion,
    pagina_edicion_trenes,
    crear_tren,
    crear_estacion,
    ver_estaciones,
    ver_trenes,
    cargar_estaciones_desde_disco,
    cargar_trenes_desde_disco,
)
from interfaz import settings as config

##################################################################################




def ventana_principal():
    ventana = tk.Tk()
    ventana.title("Simulador para operarios")
    ventana.geometry(f"{config.ANCHO_VENTANA}x{config.ALTO_VENTANA}")

    canvas = tk.Canvas(ventana, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    bg_normal = Image.open(ruta_imagen)
    bg_res = bg_normal.resize((config.ANCHO_VENTANA, config.ALTO_VENTANA), Image.LANCZOS)
    imagen_fondo = ImageTk.PhotoImage(bg_res)
    canvas.create_image(0, 0, anchor="nw", image=imagen_fondo)
    canvas.image = imagen_fondo

    def redibujar_fondo(event):
        if bg_normal:
            nueva_img = bg_normal.resize((event.width, event.height), Image.LANCZOS)
            imagen_fondo = ImageTk.PhotoImage(nueva_img)
            canvas.image = imagen_fondo
            canvas.create_image(0, 0, anchor="nw", image=imagen_fondo)

    canvas.bind("<Configure>", redibujar_fondo)

    base_height = config.ALTO_VENTANA if hasattr(config, 'ALTO_VENTANA') else 600
    base_font_size = max(8, int(base_height * 0.016))
    btn_font = tkfont.Font(family="Arial", size=base_font_size)

    relw = 0.22
    relh = 0.14

    label_semilla = tk.Label(ventana, text="Semilla (0-10000):", bg=config.COLOR_BLANCO, fg=config.COLOR_GRIS, font=btn_font)
    label_semilla.place(relx=0.2, rely=0.65, anchor="center")

    entrada_semilla = tk.Entry(ventana, font=btn_font, bg="white", fg="black")
    entrada_semilla.place(relx=0.2, rely=0.75, anchor="center", relwidth=0.11, relheight=0.035)

    boton = tk.Button(
        ventana,
        text="INICIAR SIMULACIÓN",
        command=lambda: iniciar_simulacion(ventana, entrada_semilla),
        bg=config.COLOR_BLANCO,
        fg=config.COLOR_GRIS,
        font=btn_font,
        cursor="hand2",
    )
    boton.place(relx=0.2, rely=0.88, anchor="center", relwidth=relw, relheight=relh)

    boton_trenes = tk.Button(
        ventana,
        text="EDICIÓN TRENES",
        command=lambda: pagina_edicion_trenes(ventana),
        bg=config.COLOR_AZUL,
        fg=config.COLOR_BLANCO,
        font=btn_font,
        cursor="hand2",
    )
    boton_trenes.place(relx=0.5, rely=0.88, anchor="center", relwidth=relw, relheight=relh)

    boton_pagina = tk.Button(
        ventana,
        text="EDICIÓN ESTACIONES",
        command=lambda: pagina_edicion(ventana),
        bg=config.COLOR_AZUL,
        fg=config.COLOR_BLANCO,
        font=btn_font,
        cursor="hand2",
    )
    boton_pagina.place(relx=0.8, rely=0.88, anchor="center", relwidth=relw, relheight=relh)

    def on_resize(event):
        new_size = max(8, int(event.height * 0.016))
        btn_font.configure(size=new_size)

    ventana.bind('<Configure>', on_resize)
    ventana.mainloop()
if __name__ == "__main__":
    ventana_principal()