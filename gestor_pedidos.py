"""Wrapper de compatibilidad: exporta `GestorPedidos` desde `src.services`.

Re-export para compatibilidad con imports existentes durante la reorganización.
"""

"""Raíz removida: importar desde `src.services.gestor_pedidos`.

Importar desde la raíz ha sido descontinuado. Usa:

	from src.services.gestor_pedidos import GestorPedidos

Contacta si necesitas compatibilidad temporal.
"""

raise RuntimeError("Import desde la raíz eliminado: usa 'from src.services.gestor_pedidos import GestorPedidos'.")
