import sys
import os

#Ruta raiz
ruta_raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

#Path imagen de fondo
ruta_imagen = os.path.join(ruta_raiz, "interfaz", "images", "bg.png")
