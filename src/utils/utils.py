"""Módulo `src.utils.utils` con utilidades.

Funciones helper para generar ids, timestamps y validaciones.
"""
from __future__ import annotations
from typing import Dict, Any
from datetime import datetime


def generar_id(prefix: str = '') -> str:
    """Generar un id único legible para un nuevo pedido.

    Salida esperada: cadena única (ejemplo: 'PED-20251118-0001').
    """
    # Generación simple basada en timestamp UTC
    ts = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    return f"{prefix}{ts}"


def ahora_iso() -> str:
    """Devolver timestamp actual en formato ISO-8601.

    Salida esperada: string ISO, ejemplo: '2025-11-18T12:34:56'.
    """
    return datetime.utcnow().isoformat()


def validar_items(items: list) -> bool:
    """Validar estructura básica de la lista de items.

    Salida esperada: True si la estructura es válida, False en caso contrario.
    """
    if not isinstance(items, list):
        return False
    for it in items:
        if not isinstance(it, dict):
            return False
        if 'name' not in it or 'qty' not in it:
            return False
        try:
            if int(it.get('qty', 0)) <= 0:
                return False
        except Exception:
            return False
    return True
