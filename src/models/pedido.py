"""Modulo `src.models.pedido`.

Este archivo define la interfaz de la entidad `Pedido`. Cada método incluye
una descripción clara de lo que debe hacer, qué debe devolver y un ejemplo de
uso. Este archivo es un esqueleto: los métodos lanzan `NotImplementedError`.

Concepto general:
- Un `Pedido` encapsula datos y reglas triviales sobre un pedido de cocina.
- La lógica de negocio (asignación, cálculo de tiempos) la proveen servicios
    como `GestorPedidos` y `temporizador`.

Ejemplo de uso (pseudocódigo):

from src.models.pedido import Pedido

items = [{'name':'Pizza','qty':1,'prep_time_min':12}]
pedido = Pedido(id='PED-1', items=items, cliente_info={'telefono':'600111222'})
pedido.update_estado('EN_PREPARACION')
pedido.add_item({'name':'Coca', 'qty':1})
data = pedido.as_dict()

"""
from __future__ import annotations
from typing import List, Dict, Optional, Union
from datetime import datetime


class Pedido:
    """Representa un pedido.

    Atributos públicos sugeridos:
    - id: Identificador único del pedido (str|int)
    - items: Lista de diccionarios con keys: name, qty, prep_time_min (opcional)
    - estado: Estado actual (PENDIENTE, EN_PREPARACION, LISTO, ENTREGADO, CANCELADO)
    - tiempo_estimado_min: Estimación en minutos (int o None)
    - timestamp_creado: datetime de creación
    - estacion_id: id de estación asignada o None
    """

    def __init__(self, id: Union[str, int], items: List[Dict], cliente_info: Optional[Dict] = None) -> None:
        """Crear un `Pedido`.

        Comportamiento esperado:
        - Inicializa `id`, `items` (lista copia), `cliente_info`.
        - Setea `estado = 'PENDIENTE'` y `timestamp_creado = ahora`.
        - `tiempo_estimado_min` inicialmente `None` hasta que `temporizador` lo calcule.

        Ejemplo:
        >>> Pedido('PED-1', [{'name':'Taco','qty':2}])

        Returns: None (construye el objeto). Si `items` no es válido, lanzar `ValueError`.
        """
        raise NotImplementedError()

    def update_estado(self, nuevo_estado: str) -> None:
        """Actualizar el estado del pedido.

        Reglas esperadas:
        - Solo permitir transiciones válidas: PENDIENTE -> EN_PREPARACION -> LISTO -> ENTREGADO
          (y CANCELADO desde PENDIENTE o EN_PREPARACION).
        - Actualizar `estado` y devolver `None`.
        - Registrar (internamente) timestamp opcional de cambio (no obligatorio).

        Ejemplo:
        >>> pedido.update_estado('EN_PREPARACION')

        Raises:
            ValueError: si `nuevo_estado` es inválido o la transición no está permitida.
        """
        raise NotImplementedError()

    def add_item(self, item: Dict) -> None:
        """Añadir un ítem al pedido.

        Comportamiento esperado:
        - Validar que `item` contiene al menos `name` y `qty` (qty > 0).
        - Si un item con el mismo `name` ya existe, acumular `qty` o añadir nuevo
          según política del equipo (aquí documentamos que se suma `qty`).
        - No calcular tiempos aquí: el `temporizador` es responsable de actualizar
          `tiempo_estimado_min`.

        Ejemplo:
        >>> pedido.add_item({'name':'Agua','qty':2})

        Returns: None. En caso de entrada inválida, lanzar `ValueError`.
        """
        raise NotImplementedError()

    def remove_item(self, item_name: str) -> bool:
        """Remover un ítem por nombre.

        Comportamiento esperado:
        - Buscar item por `name`. Si no existe, devolver False.
        - Si existe, eliminarlo (o decrementar qty si se desea) y devolver True.

        Ejemplo:
        >>> removed = pedido.remove_item('Agua')
        >>> if removed:
        ...     print('Item eliminado')

        Returns:
            bool: True si se eliminó, False si no se encontró.
        """
        raise NotImplementedError()

    def as_dict(self) -> Dict:
        """Devolver una representación serializable del pedido.

        Salida esperada: diccionario con todos los atributos relevantes, por ejemplo:

        {
            'id': 'PED-1',
            'items': [{'name':'Pizza','qty':1,'prep_time_min':12}],
            'estado': 'PENDIENTE',
            'tiempo_estimado_min': None,
            'timestamp_creado': '2025-11-18T12:34:56',
            'estacion_id': None,
            'cliente_info': {...}
        }

        Este método facilita la serialización a JSON para APIs o almacenamiento.
        """
        raise NotImplementedError()
