"""Módulo `src.models.estacion_cocina`.

Contiene la clase `EstacionCocina` que representa una estación de preparación.
Esqueleto con docstrings; implementar lógica posteriormente.
"""
from __future__ import annotations
from typing import List, Optional, Dict, Union

from .pedido import Pedido


class EstacionCocina:
    """Modelo de estación de cocina.

    Atributos sugeridos:
    - id: identificador de la estación
    - capacidad: 

    - cola: estructura para pedidos en espera
    - en_preparacion: lista/colección de pedidos actualmente en preparación
    """
    
    id: Union[str, int]
    capacidad: int
    cola: List[Pedido]
    en_preparacion: List[Pedido]

    def __init__(self, id: Union[str, int], capacidad: int = 1) -> None:
        """Inicializar estación.

        Salida esperada: instancia con `capacidad` definida y colas vacías.hñetd
        """
        self.id = id
        self.capacidad = capacidad
        self.cola = []
        self.en_preparacion = []
        
    def asignar_pedido(self, pedido: Pedido) -> bool:
        """Intentar asignar un pedido a la estación.

        Salida esperada: bool indicando si la asignación fue exitosa.
        """
        pedido.estado = 'EN_COLA' # Actualizar estado del pedido a EN_COLA
        if len(self.cola) + len(self.en_preparacion) < self.capacidad: # Verificar si hay capacidad disponible
            self.cola.append(pedido)# Agregar pedido a la cola append sirve para agregar un elemento al final de una lista
            return True
        return False

    def iniciar_preparacion(self) -> List[Pedido]:
        """Marcar pedidos que comienzan a prepararse.

        Salida esperada: lista de `Pedido` que pasaron a preparación.
    
        """
        pedidos_iniciados = [] # Lista para almacenar pedidos que inician preparación
        while self.cola and len(self.en_preparacion) < self.capacidad:
            pedido = self.cola.pop(0)  # Sacar el primer pedido de la cola pop sirve para eliminar y devolver un elemento de una lista, en este caso el primer elemento
            pedido.estado = 'EN_PREPARACION'  # Actualizar estado a EN_PREPARACION
            self.en_preparacion.append(pedido)  # Agregar a en_preparacion
            pedidos_iniciados.append(pedido)  # Agregar a la lista de iniciados
        return pedidos_iniciados

    def finalizar_pedido(self, pedido_id: Union[str, int]) -> bool:
        """Marcar un pedido como `LISTO`.

        Salida esperada: True si se finalizó y se actualizó el estado, False si no se encontró.
        """
        for pedido in self.en_preparacion:
            if pedido.id == pedido_id:
                pedido.estado = 'LISTO'  # Actualizar estado a LISTO
                self.en_preparacion.remove(pedido)  # Eliminar de en_preparacion
                return True
        return False

    def carga_actual(self) -> int:
        """Devolver la carga actual (en preparación + en cola).

        Salida esperada: int >= 0 representando número de pedidos gestionados por la estación.
        
        """
        Total_de_Pedidos = len(self.cola) + len(self.en_preparacion)
        return Total_de_Pedidos
    
    #Fucion agregada para validacion de capacidad
    def puede_aceptar_pedido(self, pedido: Pedido) -> bool:
        """Verificar si la estación puede aceptar un nuevo pedido.

        Salida esperada: True si hay capacidad para aceptar el pedido, False en caso contrario.
        """
        return (len(self.cola) + len(self.en_preparacion)) < self.capacidad