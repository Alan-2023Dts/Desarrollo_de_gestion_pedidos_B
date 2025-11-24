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

    Atributos:
    - id: Identificador único del pedido (str|int)
    - items: Lista de diccionarios con keys: name, qty, prep_time_min (opcional)
    - estado: Estado actual (PENDIENTE, EN_PREPARACION, LISTO, ENTREGADO, CANCELADO)
    - tiempo_estimado_min: Estimación en minutos (int o None)
    - timestamp_creado: datetime de creación
    - estacion_id: id de estación asignada o None
    """

    
    ESTADOS_VALIDOS = ['PENDIENTE', 'EN_COLA', 'EN_PREPARACION', 'LISTO', 'ENTREGADO', 'CANCELADO']
    TRANSICIONES_VALIDAS = {
        'PENDIENTE': ['EN_COLA', 'EN_PREPARACION', 'CANCELADO'],
        'EN_COLA': ['EN_PREPARACION', 'CANCELADO'],
        'EN_PREPARACION': ['LISTO', 'CANCELADO'],
        'LISTO': ['ENTREGADO'],
        'ENTREGADO': [],
        'CANCELADO': []
    }
        
    
    def __init__(self, id: Union[str, int], items: List[Dict], cliente_info: Optional[Dict] = None) -> None:
        # Se define un parámetro base que determinará la tolerancia de los elementos
        """Crear un Pedido.

        Comportamiento esperado:
        - Inicializa id, items (lista copia), cliente_info.
        - Setea estado = 'PENDIENTE' y timestamp_creado = ahora.
        - tiempo_estimado_min inicialmente None hasta que temporizador lo calcule.

        Ejemplo:
        >>> Pedido('PED-1', [{'name':'Taco','qty':2}])

        Returns: None (construye el objeto). Si items no es válido, lanzar ValueError.
        """
        if not isinstance(items, list):
            raise ValueError("Items debe ser una lista")
        self.id = id
        norm_items: List[Dict] = []
        for it in items:
            if not isinstance(it, dict) or 'name' not in it or 'qty' not in it:
                raise ValueError("Cada item debe ser dict con 'name' y 'qty'")
            name = it['name']
            qty = it['qty']
            if not isinstance(name, str) or not isinstance(qty, int) or qty <= 0:
                raise ValueError("Item inválido: 'name' str y 'qty' int>0")
            prep = int(it.get('prep_time_min', 5))
            price = round(float(it.get('price', 0.0)), 2)
            norm_items.append({'name': name, 'qty': qty, 'prep_time_min': prep, 'price': price})
        self.items = norm_items
        self.cliente_info = dict(cliente_info) if cliente_info else None
        self.estado = 'PENDIENTE'
        self.tiempo_estimado_min = None
        self.timestamp_creado = datetime.now()
        self.estacion_id = None
        self._timestamps_estado: Dict[str, datetime] = {'PENDIENTE': self.timestamp_creado} # Para registrar los timestamps de cada estado


    def update_estado(self, nuevo_estado: str) -> None:
        # Del parámetro base, surge la necesidad de implementar estados de venta (Valida si el estado es real)
        """Actualizar el estado del pedido.

        Reglas esperadas:
        - Solo permitir transiciones válidas: PENDIENTE -> EN_PREPARACION -> LISTO -> ENTREGADO
          (y CANCELADO desde PENDIENTE o EN_PREPARACION).
        - Actualizar estado y devolver None.
        - Registrar (internamente) timestamp opcional de cambio (no obligatorio).

        Ejemplo:
        >>> pedido.update_estado('EN_PREPARACION')

        Raises:
            ValueError: si nuevo_estado es inválido o la transición no está permitida.
        """
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {nuevo_estado}. Debe ser uno de: {', '.join(self.ESTADOS_VALIDOS)}")

        if self.estado not in self.TRANSICIONES_VALIDAS or nuevo_estado not in self.TRANSICIONES_VALIDAS[self.estado]:
            raise ValueError(f"Transición inválida: No se puede pasar de {self.estado} a {nuevo_estado}")

        self.estado = nuevo_estado
        if not hasattr(self, '_timestamps_estado'): # Verificación extra de robustez
            self._timestamps_estado = {}
        self._timestamps_estado[nuevo_estado] = datetime.now()
        
        print(f"Estado actualizado a {self.estado} en {self._timestamps_estado[nuevo_estado]}")


    def add_item(self, item: Dict) -> None:
        """Añadir un ítem al pedido.

        Comportamiento esperado:
        - Validar que item contiene al menos name y qty (qty > 0).
        - Si un item con el mismo name ya existe, acumular qty o añadir nuevo
          según política del equipo (aquí documentamos que se suma qty).
        - No calcular tiempos aquí: el temporizador es responsable de actualizar
          tiempo_estimado_min.

        Ejemplo:
        >>> pedido.add_item({'name':'Agua','qty':2})

        Returns: None. En caso de entrada inválida, lanzar ValueError.
        """
        if not isinstance(item, dict) or 'name' not in item or 'qty' not in item:
            raise ValueError("Item debe ser un diccionario con 'name' y 'qty'")
        if not isinstance(item['qty'], int) or item['qty'] <= 0:
            raise ValueError("La cantidad (qty) debe ser un entero mayor que cero")

        existing_item = next((i for i in self.items if i['name'] == item['name']), None)
        if existing_item:
            existing_item['qty'] += item['qty']
        else:
            self.items.append(item)
        
    def remove_item(self, item_name: str) -> bool:
        """Remover un ítem por nombre.

        Comportamiento esperado:
        - Buscar item por name. Si no existe, devolver False.
        - Si existe, eliminarlo (o decrementar qty si se desea) y devolver True.

        Ejemplo:
        >>> removed = pedido.remove_item('Agua')
        >>> if removed:
        ...     print('Item eliminado')

        Returns:
            bool: True si se eliminó, False si no se encontró.
        """
        for i, item in enumerate(self.items):
            if item['name'] == item_name:
                del self.items[i]
                return True
        return False
    
    
    
    def total_price(self) -> float:
        """Calcular total del pedido (suma qty * price por ítem)."""
        total = 0.0
        for it in getattr(self, 'items', []):
            qty = int(it.get('qty', 0))
            price = float(it.get('price', 0.0))
            total += qty * price
        return round(total, 2)

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
        data = {
            'id': self.id,
            'items': self.items,
            'estado': self.estado,
            'tiempo_estimado_min': self.tiempo_estimado_min,
            'timestamp_creado': self.timestamp_creado.isoformat() if hasattr(self, 'timestamp_creado') else None,
            'estacion_id': self.estacion_id,
            'cliente_info': self.cliente_info,
            'total_price': self.total_price()
        }
        return data