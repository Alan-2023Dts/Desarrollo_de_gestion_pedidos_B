"""Compatibilidad: re-exportar `EstacionCocina` desde `src.models.estacion_cocina`.

Permite seguir importando `EstacionCocina` desde la raíz:

	from estacion_cocina import EstacionCocina

Se recomienda usar `from src.models.estacion_cocina import EstacionCocina`.
"""

from src.models.estacion_cocina import EstacionCocina

__all__ = ["EstacionCocina"]
