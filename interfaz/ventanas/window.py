import sys
import os
import tkinter as tk
import sys
import os

from PIL import ImageTk, Image

###Señala carpeta interfaz
ruta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ruta_raiz)
from interfaz import settings as config



def iniciar_simulacion():  #####AGREGAR AL PROGRAMA PRINCIPAL PARA INICIARLO DESDE EL BOTÓN
    print("ACCIÓN")

def ventana_principal():
    ###Inicio desarrollo ventanas
    ventana = tk.Tk()
    ventana.title("Simulador para operarios")
    ventana.geometry(f"{config.ANCHO_VENTANA}x{config.ALTO_VENTANA}")
    ventana.configure(bg=config.COLOR_GRIS)

    boton = tk.Button(
        ventana,
        text="INICIAR SIMULACIÓN",
        command=iniciar_simulacion,
        bg=config.COLOR_BLANCO,
        fg=config.COLOR_GRIS,
        font=("Arial", 14),
        width=30,   
        height=3     
    )
    boton.place(relx=0.5, rely=0.9, anchor="center", width=300, height=100)
    ventana.mainloop()