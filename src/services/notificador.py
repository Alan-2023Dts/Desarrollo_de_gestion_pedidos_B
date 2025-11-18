"""Módulo `src.services.notificador`.

Simula envíos de notificaciones al cliente. Define la interfaz y las salidas
esperadas; la implementación real vendrá después.
"""
from __future__ import annotations
from typing import Optional, Dict

from ..models.pedido import Pedido


class Notificador:
    """Simula un notificador con diferentes 'modos' (console, email, webhook).
    """

    def __init__(self, modo: str = 'console') -> None:
        """Inicializar notificador.

        Salida esperada: instancia con `modo` guardado.
        """
        raise NotImplementedError()

    def enviar(self, pedido: Pedido, evento: str, extra: Optional[Dict] = None) -> bool:
        """Enviar una notificación sobre `pedido` y `evento`.

        Salida esperada: True si la notificación se envió (o se simuló) correctamente,
        False en caso de fallo.
        """
        raise NotImplementedError()
