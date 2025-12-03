# window.py solamente contiene la ventana principal. Las otras ventanas
# se encuentran en archivos separados dentro de la carpeta ventanas. Se modularizó
# de esta forma para mejorar la legibilidad y facilitar el mantenimiento.
import sys
import os
import tkinter as tk
import tkinter.font as tkfont
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

    boton = tk.Button(
        ventana,
        text="INICIAR SIMULACIÓN",
        command=lambda: iniciar_simulacion(ventana, entrada_semilla),
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
        bg=config.COLOR_AZUL,
        fg=config.COLOR_BLANCO,
        font=btn_font,
        cursor="hand2",
    )
    boton_pagina.place(relx=config.BUTTON_ESTACIONES_POS[0], rely=config.BUTTON_ESTACIONES_POS[1], anchor="center", relwidth=config.BUTTON_RELWIDTH, relheight=config.BUTTON_RELHEIGHT)

    def on_resize(event):
        new_size = max(8, int(event.height * 0.016))
        btn_font.configure(size=new_size)

    ventana.bind('<Configure>', on_resize)
    ventana.mainloop()
if __name__ == "__main__":
    ventana_principal()