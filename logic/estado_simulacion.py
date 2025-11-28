"""
Módulo para el manejo del estado de la simulación.
"""

class EstadoSimulacion:
    """
    Clase que representa el estado actual de la simulación.
    """
    def __init__(self, hora_actual=0):
        """
        Inicializa el estado de la simulación con la hora actual.
        Args:
            hora_actual (int): La hora actual de la simulación.
        """
        self.hora_actual = hora_actual

    def __str__(self):
        return f"EstadoSimulacion(hora_actual={self.hora_actual})"
