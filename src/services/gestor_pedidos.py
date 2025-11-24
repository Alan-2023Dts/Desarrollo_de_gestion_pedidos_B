"""Módulo `src.services.gestor_pedidos`.

Contiene la clase `GestorPedidos` para crear, almacenar y asignar pedidos.
Esqueleto: firmas y docstrings que describen salidas esperadas.
"""
from __future__ import annotations
from typing import Dict, Optional, List, Union

from ..models.pedido import Pedido
from ..models.estacion_cocina import EstacionCocina


class GestorPedidos:
    """Orquesta la vida de los pedidos y las estaciones.

    Mantiene estructuras en memoria:
    - pedidos: dict[id, Pedido]
    - estaciones: dict[id, EstacionCocina]
    """
    pedidos: dict[Union[str, int], Pedido]
    estaciones: dict[Union[str, int], EstacionCocina]
    

    def __init__(self) -> None:
        """Inicializar estructuras internas.

        Salida esperada: instancia con `pedidos` y `estaciones` vacías.
        
        """
        self.pedidos: dict = {} #Esto sirve para inicializar el diccionario de pedidos
        self.estaciones: dict = {} #Esto sirve para inicializar el diccionario de estaciones
        #raise NotImplementedError() # Inicializar dicts vacíos

    def crear_pedido(self, items: List[Dict], cliente_info: Optional[Dict] = None) -> Pedido: #
        """Crear y registrar un nuevo pedido.

        Salida esperada: instancia `Pedido` registrada en `self.pedidos`.
        
        """
        # Generación de ID legible: PED-0001, PED-0002, ...
        new_id = f"PED-{len(self.pedidos) + 1:04d}"
        new_pedido = Pedido(id=new_id, items=items, cliente_info=cliente_info)
        self.pedidos[new_id] = new_pedido
        return new_pedido

    def cancelar_pedido(self, pedido_id: Union[str, int]) -> bool:
        """Cancelar un pedido si es permitido.

        Salida esperada: True si se canceló correctamente, False si no existe o no se puede cancelar.
        
        """
        pedido = self.pedidos.get(pedido_id)  # Obtener el pedido por id
        if pedido  and pedido.estado in ['PENDIENTE', 'EN_PREPARACION']: # Verificar si existe y si se puede cancelar
            pedido.update_estado('CANCELADO')  # Actualizar estado a CANCELADO
            return True
        return False  # Devolver False si no se pudo cancelar
 

    def asignar_a_estacion(self, pedido_id: Union[str, int], estacion_id: Union[str, int]) -> bool:
        """Intentar asignar un pedido a una estación concreta.

        Salida esperada: True si la asignQQQación fue exitosa, False en caso contrario.
        """
        pedido = self.pedidos.get(pedido_id)# Obtener el pedido por id
        estacion = self.estaciones.get(estacion_id)# Obtener la estación por id
        if pedido and estacion and estacion.puede_aceptar_pedido(pedido): # Verificar existencia y capacidad
            estacion.asignar_pedido(pedido)  # Asignar pedido a estación
            return True
        return False # Devolver False si no se pudo asignar
    

    def obtener_pedido(self, pedido_id: Union[str, int]) -> Optional[Pedido]: 
        """Devolver el `Pedido` por id o None si no existe.

        Salida esperada: `Pedido` o `None`.
        """
        return self.pedidos.get(pedido_id)  # Devolver el pedido o None si no existe
        
        

    def listar_pedidos(self, estado: Optional[str] = None) -> List[Pedido]:
        """Listar pedidos, opcionalmente filtrando por `estado`.

        Salida esperada: lista de instancias `Pedido`.
        """
        if estado is None: # Devolver todos los pedidos si no hay filtro con filtro nos referimos a que si no se especifica ningun estado
            return list(self.pedidos.values())
        else:
            return [pedido for pedido in self.pedidos.values() if pedido.estado == estado]