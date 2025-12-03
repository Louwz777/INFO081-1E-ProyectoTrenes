import datetime as dt
from collections.abc import Callable
from typing import Any

from generadores import Generador


class GeneradorBatido(Generador):
    """Generador que produce clientes en ráfagas en intervalos regulares.

    En lugar de generar clientes uniformemente o constantemente cada minuto,
    este generador produce todos los clientes en intervalos fijos de tiempo (por ejemplo, cada 15 minutos).
    Fuera de estos intervalos, no se generan clientes.
    """

    import json
    import os

    # Load config
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        INTERVALO_BATIDA = config.get("intervalo_batida", 15)
    except Exception:
        INTERVALO_BATIDA = 15

    def generar_clientes(
        self,
        minutos: int,
        constructor: Callable[[int, dt.datetime], Any],
        update: bool = True,
    ) -> list[Any]:
        if update:
            self.current_datetime += dt.timedelta(minutes=minutos)

        # Número total de ráfagas en el día
        minutos_funcionamiento = self.minutos_de_funcionamiento()
        num_batidas = minutos_funcionamiento // self.INTERVALO_BATIDA
        clientes_por_batida = int(self.poblacion * 0.2 / num_batidas)

        clientes = []

        # Si el periodo actual contiene al menos una batida, generamos
        # Detectamos si ocurre una ráfaga dentro de 'minutos'
        inicio_minuto = (self.current_datetime.minute - minutos) % self.INTERVALO_BATIDA
        fin_minuto = self.current_datetime.minute % self.INTERVALO_BATIDA

        # Solo generamos clientes si el periodo incluye el inicio de una ráfaga
        if inicio_minuto > fin_minuto or (inicio_minuto == 0 and minutos >= self.INTERVALO_BATIDA):
            for _ in range(clientes_por_batida):
                val = self.rdm.randint(0, 2_000_000)
                cliente = constructor(val, self.current_datetime)
                clientes.append(cliente)

        # En los minutos donde no hay ráfaga, no se generan clientes
        return clientes

class GeneradorShake(Generador):
    INTERVALO_BATIDA = 15  # o cargar desde config como antes

    def __init__(self, poblacion, seed=123, fecha_inicial=dt.datetime(2025,1,1), hora_apertura=dt.time(7,0), hora_cierre=dt.time(20,0)):
        super().__init__(poblacion, seed, fecha_inicial, hora_apertura, hora_cierre)
        self.acumulador_minutos = 0  # acumula minutos desde la última batida

    def generar_clientes(self, minutos: int, constructor: Callable[[int, dt.datetime], Any], update: bool = True) -> list[Any]:
        if update:
            self.current_datetime += dt.timedelta(minutes=minutos)

        self.acumulador_minutos += minutos
        clientes = []

        # Cuántas ráfagas completas pasaron desde la última vez
        batidas_completas = int(self.acumulador_minutos // self.INTERVALO_BATIDA)
        if batidas_completas > 0:
            minutos_funcionamiento = self.minutos_de_funcionamiento()
            num_batidas = minutos_funcionamiento // self.INTERVALO_BATIDA
            clientes_por_batida = int(self.poblacion * 0.2 / num_batidas)

            for _ in range(batidas_completas):
                for _ in range(clientes_por_batida):
                    val = self.rdm.randint(0, 2_000_000)
                    clientes.append(constructor(val, self.current_datetime))

            # restamos los minutos ya usados en ráfagas
            self.acumulador_minutos %= self.INTERVALO_BATIDA

        return clientes