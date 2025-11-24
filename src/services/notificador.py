"""Módulo `src.services.notificador`.

Simula envíos de notificaciones al cliente. Define la interfaz y las salidas
esperadas; la implementación real vendrá después.
"""
from __future__ import annotations
from typing import Optional, Dict

from ..models.pedido import Pedido


class Notificador:
    """Simula un notificador con diferentes 'modos' (console, email, webhook).
    """

    def __init__(self, modo: str = 'console') -> None:
        """Inicializar notificador.

        Salida esperada: instancia con `modo` guardado.
        """
        self.modo = modo
        

    def enviar(self, pedido: Pedido, evento: str, extra: Optional[Dict] = None) -> bool:
        """Enviar una notificación sobre `pedido` y `evento`.

        Salida esperada: True si la notificación se envió (o se simuló) correctamente,
        False en caso de fallo.
        """
        try:
            print(f"[Notificador-{self.modo}] Evento: {evento} para Pedido ID: {pedido.id}")

            items = getattr(pedido, 'items', []) or []
            if items:
                print("---- TICKET ----")
                running = 0.0
                for it in items:
                    name = it.get('name', 'N/A')
                    qty = int(it.get('qty', 1))
                    price = float(it.get('price', 0.0))
                    subtotal = qty * price
                    running += subtotal
                    print(f"  {name} x{qty}  @ {price:.2f}  = {subtotal:.2f}")
                total = pedido.total_price() if hasattr(pedido, 'total_price') else running
                print("-----------------")
                print(f"TOTAL: {total:.2f}")
                if getattr(pedido, 'cliente_info', None):
                    print(f"Cliente: {pedido.cliente_info}")
                print("-----------------")
            else:
                print("(No hay items para ticket)")
            return True
        except Exception as e:
            print(f"[Notificador] Error al enviar notificación: {e}")
            return False
