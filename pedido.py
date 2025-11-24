"""Compatibilidad: re-exportar `Pedido` desde `src.models.pedido`.

Este wrapper permite seguir haciendo `from pedido import Pedido` desde
scripts o entornos que aún importen desde la raíz del repositorio.
Preferimos importaciones explícitas desde `src.*`, pero este wrapper
facilita compatibilidad hacia atrás.
"""

from src.models.pedido import Pedido

__all__ = ["Pedido"]
