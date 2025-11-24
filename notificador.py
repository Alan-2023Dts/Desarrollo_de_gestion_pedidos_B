"""Compatibilidad: re-exportar `Notificador` desde `src.services.notificador`.

Permite seguir haciendo `from notificador import Notificador` desde la raíz.
Se recomienda usar `from src.services.notificador import Notificador`.
"""

from src.services.notificador import Notificador

__all__ = ["Notificador"]