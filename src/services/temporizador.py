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
    minutos = 0
    for item in pedido.items:
        prep_time = item.get('prep_time_min', 0) # Obtener tiempo de preparación por unidad
        qty = item.get('qty', 1) # Obtener cantidad de unidades
        minutos += prep_time * qty # Sumar al tiempo total
    return minutos

def formato_tiempo(minutos: int) -> str:
    """Devolver representación legible del tiempo.

    Ejemplos de salida esperada:
    - 25 -> "25 min"
    - 65 -> "1h 5min"

    Salida esperada: str legible.
    """
    #El parametro minutos es un entero que representa la cantidad de minutos a formatear y se obtiene desde la funcion calcular_tiempo_estimado
    horas = minutos // 60 # Calcular horas completas
    mins = minutos % 60 # Calcular minutos restantes
    if horas > 0: # Si hay horas completas
        return f"{horas}h {mins}min" if mins > 0 else f"{horas}h" #si no hay minutos restantes solo mostrar horas
    else:
        return f"{mins} min" #en caso contrario solo mostrar minutos
