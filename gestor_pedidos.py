"""Compatibilidad: re-exportar `GestorPedidos` desde `src.services.gestor_pedidos`.

Permite seguir importando `GestorPedidos` desde la raíz:

	from gestor_pedidos import GestorPedidos

Se recomienda usar `from src.services.gestor_pedidos import GestorPedidos`.
"""

from src.services.gestor_pedidos import GestorPedidos

__all__ = ["GestorPedidos"]
