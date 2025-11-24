"""Compatibilidad: re-exportar funciones del temporizador desde `src.services.temporizador`.

Permite:

	from temporizador import calcular_tiempo_estimado, formato_tiempo

Se recomienda usar `from src.services.temporizador import ...`.
"""

from src.services.temporizador import calcular_tiempo_estimado, formato_tiempo

__all__ = ["calcular_tiempo_estimado", "formato_tiempo"]
