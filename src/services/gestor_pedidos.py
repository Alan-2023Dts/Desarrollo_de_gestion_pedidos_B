"""Módulo `src.services.gestor_pedidos`.

Contiene la clase `GestorPedidos` para crear, almacenar y asignar pedidos.
Esqueleto: firmas y docstrings que describen salidas esperadas.
"""
from __future__ import annotations
from typing import Dict, Optional, List, Union

from ..models.pedido import Pedido
from ..models.estacion_cocina import EstacionCocina


class GestorPedidos:
    """Orquesta la vida de los pedidos y las estaciones.

    Mantiene estructuras en memoria:
    - pedidos: dict[id, Pedido]
    - estaciones: dict[id, EstacionCocina]
    """

    def __init__(self) -> None:
        """Inicializar estructuras internas.

        Salida esperada: instancia con `pedidos` y `estaciones` vacías.
        """
        raise NotImplementedError()

    def crear_pedido(self, items: List[Dict], cliente_info: Optional[Dict] = None) -> Pedido:
        """Crear y registrar un nuevo pedido.

        Salida esperada: instancia `Pedido` registrada en `self.pedidos`.
        """
        raise NotImplementedError()

    def cancelar_pedido(self, pedido_id: Union[str, int]) -> bool:
        """Cancelar un pedido si es permitido.

        Salida esperada: True si se canceló correctamente, False si no existe o no se puede cancelar.
        """
        raise NotImplementedError()

    def asignar_a_estacion(self, pedido_id: Union[str, int], estacion_id: Union[str, int]) -> bool:
        """Intentar asignar un pedido a una estación concreta.

        Salida esperada: True si la asignación fue exitosa, False en caso contrario.
        """
        raise NotImplementedError()

    def obtener_pedido(self, pedido_id: Union[str, int]) -> Optional[Pedido]:
        """Devolver el `Pedido` por id o None si no existe.

        Salida esperada: `Pedido` o `None`.
        """
        raise NotImplementedError()

    def listar_pedidos(self, estado: Optional[str] = None) -> List[Pedido]:
        """Listar pedidos, opcionalmente filtrando por `estado`.

        Salida esperada: lista de instancias `Pedido`.
        """
        raise NotImplementedError()
