"""Módulo `src.models.estacion_cocina`.

Contiene la clase `EstacionCocina` que representa una estación de preparación.
Esqueleto con docstrings; implementar lógica posteriormente.
"""
from __future__ import annotations
from typing import List, Optional, Dict, Union

from .pedido import Pedido


class EstacionCocina:
    """Modelo de estación de cocina.

    Atributos sugeridos:
    - id: identificador de la estación
    - capacidad: número de pedidos que puede preparar en paralelo
    - cola: estructura para pedidos en espera
    - en_preparacion: lista/colección de pedidos actualmente en preparación
    """

    def __init__(self, id: Union[str, int], capacidad: int = 1) -> None:
        """Inicializar estación.

        Salida esperada: instancia con `capacidad` definida y colas vacías.
        """
        raise NotImplementedError()

    def asignar_pedido(self, pedido: Pedido) -> bool:
        """Intentar asignar un pedido a la estación.

        Salida esperada: bool indicando si la asignación fue exitosa.
        """
        raise NotImplementedError()

    def iniciar_preparacion(self) -> List[Pedido]:
        """Marcar pedidos que comienzan a prepararse.

        Salida esperada: lista de `Pedido` que pasaron a preparación.
        """
        raise NotImplementedError()

    def finalizar_pedido(self, pedido_id: Union[str, int]) -> bool:
        """Marcar un pedido como `LISTO`.

        Salida esperada: True si se finalizó y se actualizó el estado, False si no se encontró.
        """
        raise NotImplementedError()

    def carga_actual(self) -> int:
        """Devolver la carga actual (en preparación + en cola).

        Salida esperada: int >= 0 representando número de pedidos gestionados por la estación.
        """
        raise NotImplementedError()
