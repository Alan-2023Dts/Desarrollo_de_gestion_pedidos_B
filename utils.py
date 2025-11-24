"""Compatibilidad: re-exportar utilidades desde `src.utils.utils`.

Permite hacer:

	from utils import generar_id, ahora_iso, validar_items

Se recomienda usar `from src.utils.utils import ...`.
"""

from src.utils.utils import generar_id, ahora_iso, validar_items

__all__ = ["generar_id", "ahora_iso", "validar_items"]
