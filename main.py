"""Compatibilidad: wrapper para ejecutar el entrypoint `src.main.main`.

Este archivo permite seguir ejecutando `python main.py` en la raíz durante
la transición. Recomendamos `python -m src.main`, pero este wrapper
invoca la implementación del paquete `src`.
"""

from src.main import main as _main


if __name__ == '__main__':
    _main()
