"""Módulo `notificador`.

Simula envíos de notificaciones al cliente. Aquí se define la interfaz y las
salidas esperadas; la implementación real (email/webhook) vendrá después.
"""
from __future__ import annotations
from typing import Optional, Dict

from pedido import Pedido


"""Raíz removida: importar `Notificador` desde `src.services.notificador`.

Importar desde la raíz ha sido descontinuado. Usa:

    from src.services.notificador import Notificador

Contacta si necesitas compatibilidad temporal.
"""

raise RuntimeError("Import desde la raíz eliminado: usa 'from src.services.notificador import Notificador'.")
#def __init__(self, modo: str = 'console') -> None: