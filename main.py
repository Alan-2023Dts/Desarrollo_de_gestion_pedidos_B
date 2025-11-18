"""Wrapper de compatibilidad: re-exporta `main` desde `src.main`.

Al ejecutar `python main.py` en la raíz, esto intentará invocar
`src.main.main()` (actualmente placeholder). Mantener este wrapper evita cambios
inmediatos en los scripts de ejecución existentes.
"""

"""Raíz removida: ejecutar el entrypoint desde el paquete `src`.

En lugar de ejecutar `python main.py` en la raíz, usa el módulo de paquete:

    python -m src.main

Esto evita problemas de imports relativos y garantiza que Python trate `src`
como paquete.
"""

raise RuntimeError("Ejecución desde la raíz descontinuada: usa 'python -m src.main'.")
