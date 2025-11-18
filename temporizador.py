"""Wrapper de compatibilidad: re-exporta funciones del temporizador desde `src.services`.

Funciones:
- `calcular_tiempo_estimado`
- `formato_tiempo`
"""

"""Raíz removida: importar funciones desde `src.services.temporizador`.

Importar desde la raíz ha sido descontinuado. Usa:

	from src.services.temporizador import calcular_tiempo_estimado, formato_tiempo

Contacta si necesitas compatibilidad temporal.
"""

raise RuntimeError("Import desde la raíz eliminado: usa 'from src.services.temporizador import calcular_tiempo_estimado, formato_tiempo'.")
