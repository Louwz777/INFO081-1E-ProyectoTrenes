import sys
import os
import tkinter as tk    
from PIL import ImageTk, Image
from .. import settings as config


###Señala carpeta interfaz
ruta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ruta_raiz)
ruta_imagen = os.path.join(ruta_raiz, "images", "bg.png")


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
    ventana.mainloop()



if __name__ == "__main__":
    ventana_principal()