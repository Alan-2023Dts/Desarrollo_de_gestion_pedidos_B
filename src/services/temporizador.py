"""Módulo `src.services.temporizador`.

Funciones responsables de calcular tiempos estimados y formatearlos.
Contiene firmas y docstrings que explican valores de retorno esperados.
"""
from __future__ import annotations
from typing import Optional

from ..models.pedido import Pedido
from ..models.estacion_cocina import EstacionCocina


def calcular_tiempo_estimado(pedido: Pedido, estacion: Optional[EstacionCocina] = None) -> int:
    """Calcular tiempo estimado total para completar un pedido en minutos.

    Salida esperada: entero > 0 con minutos estimados.
    """
    raise NotImplementedError()


def formato_tiempo(minutos: int) -> str:
    """Devolver representación legible del tiempo.

    Ejemplos de salida esperada:
    - 25 -> "25 min"
    - 65 -> "1h 5min"

    Salida esperada: str legible.
    """
    raise NotImplementedError()
