import sys
import os

# Project root (three levels up from this file)
ruta_raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

# Default background image path used by the main window
ruta_imagen = os.path.join(ruta_raiz, "interfaz", "images", "bg.png")
