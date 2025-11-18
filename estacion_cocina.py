"""Wrapper de compatibilidad: exporta `EstacionCocina` desde `src.models`.

Re-export para compatibilidad con imports existentes durante la reorganización.
"""

"""Raíz removida: importar desde `src.models.estacion_cocina`.

Importar desde la raíz ha sido descontinuado. Usa:

	from src.models.estacion_cocina import EstacionCocina

Contacta si necesitas compatibilidad temporal.
"""

raise RuntimeError("Import desde la raíz eliminado: usa 'from src.models.estacion_cocina import EstacionCocina'.")
